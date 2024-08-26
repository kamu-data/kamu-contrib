import json
import datetime
import os
import requests
import sys


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


per_page = int(os.environ.get("MAX_PAGE", "100"))
channel_id = os.environ.get("CHANNEL_ID")
playlist_id = os.environ.get("PLAYLIST_ID")
api_key = os.environ["YOUTUBE_API_KEY"]

if channel_id is None and playlist_id is None:
    raise Exception("Specify either CHANNEL_ID or PLAYLIST_ID")

# If playlist is not specified - obtain the id of "uploads" playlist for the channel
if playlist_id is None:
    resp = requests.get(
        f"https://www.googleapis.com/youtube/v3/channels?part=statistics,contentDetails&id={channel_id}&key={api_key}&maxResults={per_page}" 
    )
    resp.raise_for_status()
    results = resp.json()
    playlist_id = results["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# List all videos in the upload playlist
video_details = {}
page_token = ""
while True:
    resp = requests.get(
        f"https://www.googleapis.com/youtube/v3/playlistItems",
        params = {
            "part": "id,snippet,contentDetails",
            "playlistId": playlist_id,
            "key": api_key,
            "pageToken": page_token,
            "maxResults": per_page,
        }
    )

    resp.raise_for_status()
    records = resp.json()

    # Append list of all videos in the channel playlist
    for item in records["items"]:
        if 'videoId' in item["contentDetails"]:
            video_id = item["contentDetails"]["videoId"]
            video_details[video_id] = {
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"],
                "channel_id": item["snippet"]["channelId"],
                "channel_title": item["snippet"]["channelTitle"],
                "video_owner_channel_id": item["snippet"]["videoOwnerChannelId"],
                "video_owner_channel_title": item["snippet"]["videoOwnerChannelTitle"],
            }

    if not records.get("nextPageToken", None):
        break

    page_token = records["nextPageToken"] # Youtube pagination works with page tokens

#now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")

# Obtaining video statistics for each item in the video list
for video_id, details in video_details.items():
    resp = requests.get(
        f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}"
    )
    # Response includes {"viewCount", "likeCount", "favoriteCount", "commentCount"}
    stats = {key: int(value) for key, value in resp.json()["items"][0]["statistics"].items()}
    #stats["timestamp"] = now
    print(json.dumps({
        "video_id": video_id,
        "title": details["title"],
        "published_at": details["published_at"],
        "channel_id": details["channel_id"],
        "channel_title": details["channel_title"],
        "video_owner_channel_id": details["video_owner_channel_id"],
        "video_owner_channel_title": details["video_owner_channel_title"],
        "view_count": stats["viewCount"],
        "like_count": stats["likeCount"],
        "comment_count": stats["commentCount"],
        "favorite_count": stats["favoriteCount"],
    }))
