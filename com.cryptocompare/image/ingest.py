#!/bin/env/python
# This script fetches data from https://min-api.cryptocompare.com/documentation
# Data is only intended for demonstrative purposes and should not be used for any purposes
# that fall outside of the CryptoCompare's free tier license agreement
# https://www.cryptocompare.com/api-licence-agreement/
import requests
import time
import datetime
import logging
import sys
import os
import json

MIN_START_TIME = int(datetime.datetime(2010, 1, 1).timestamp())
MAX_LIMIT = 2000
TIME_OFFSET = 120  # TODO: Find a better way to filter out partial results

class TierLimit(Exception):
    pass

logger = logging.getLogger()

# See: https://min-api.cryptocompare.com/documentation?key=Historical&cat=dataHistominute
def get_pair_ohlcv(from_symbol, to_symbol, api_key, level="minute", to_time=None, limit=MAX_LIMIT):
    params = dict(
        fsym=from_symbol,
        tsym=to_symbol,
        limit=limit
    )

    if to_time is not None:
        params["toTs"] = to_time

    resp = requests.get(
        f"https://min-api.cryptocompare.com/data/v2/histo{level}",
        params=params
    )
    resp.raise_for_status()
    data = resp.json()

    try:
        if data["Response"] == "Error" and data.get("ParamWithError") == "toTs":
            raise TierLimit()

        assert data["Response"] == "Success"
        assert data["Data"]["Aggregated"] == False
        assert isinstance(data["Data"]["Data"], list)
    except TierLimit:
        raise
    except:
        raise Exception(f"Unexpected response: {data}")

    logger.info(
        "Got %s data points time_min=%s, time_max=%s", 
        len(data["Data"]["Data"]),
        min(r["time"] for r in data["Data"]["Data"]),
        max(r["time"] for r in data["Data"]["Data"]),
    )

    return data


# Pulls data with highest available resolution under the free tier
def get_pair_ohlcv_max_res(from_symbol, to_symbol, from_time, api_key):
    level = "minute"
    result = None
    to_time = int(datetime.datetime.now().timestamp()) - TIME_OFFSET

    logger.info(
        "Fetching data for interval: (%s, %s]", 
        from_time,
        to_time,
    )

    while True:
        try:
            data = get_pair_ohlcv(
                from_symbol=from_symbol, 
                to_symbol=to_symbol,
                to_time=to_time,
                level=level,
                api_key=api_key,
            )
        except TierLimit:
            logger.info("Tier limit encountered at to_time=%s - switching to hourly data", to_time)
            level = "hour"
            continue

        # API returns all zero response when no data exists any more
        if max(r["close"] for r in data["Data"]["Data"]) == 0.0:
            data["Data"]["Data"] = []

        # Filter results older than from_time
        data["Data"]["Data"] = [
            r for r in data["Data"]["Data"]
            if r["time"] > from_time and r["time"] < to_time
        ]

        if result is None:
            result = data
        else:
            result["Data"]["TimeFrom"] = min(result["Data"]["TimeFrom"], data["Data"]["TimeFrom"])
            result["Data"]["TimeTo"] = max(result["Data"]["TimeTo"], data["Data"]["TimeTo"])
            result["Data"]["Data"].extend(data["Data"]["Data"])
        
        if len(data["Data"]["Data"]) == 0:
            break
        
        to_time = min(r["time"] for r in data["Data"]["Data"])

    result["Data"]["Data"].sort(key=lambda i: i["time"])

    logger.info(
        "Fetched %s data points in time interval: [%s, %s]", 
        len(result["Data"]["Data"]),
        result["Data"]["TimeFrom"],
        result["Data"]["TimeTo"],
    )

    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

    # api_key = os.environ["CRYPTOCOMPARE_API_KEY"]
    api_key = None

    last_modified = os.environ["ODF_LAST_MODIFIED"]
    new_last_modified_path = os.environ["ODF_NEW_LAST_MODIFIED_PATH"]

    if last_modified:
        last_modified = int(datetime.datetime.strptime(
            last_modified, "%Y-%m-%dT%H:%M:%S%z",
        ).timestamp())
    else:
        last_modified = 0

    result = get_pair_ohlcv_max_res(
        from_symbol="ETH",
        to_symbol="USD",
        from_time=last_modified,
        api_key=api_key,
    )

    for t in result["Data"]["Data"]:
        print(json.dumps(t))

    if len(result["Data"]["Data"]) != 0:
        with open(new_last_modified_path, 'w') as f:
            f.write(
                datetime.datetime.utcfromtimestamp(
                    result["Data"]["TimeTo"]
                ).isoformat() + "Z"
            )
