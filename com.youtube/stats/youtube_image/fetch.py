import json
import datetime
import os
import requests

per_page = int(os.environ.get("MAX_PAGE", "100"))
channel_id = os.environ["CHANNEL_ID"]
api_key = os.environ["YOUTUBE_API_KEY"]

# Get all uploaded videos of given channel ID
resp = requests.get(
    f"https://www.googleapis.com/youtube/v3/channels?part=statistics,contentDetails&id={channel_id}&key={api_key}&maxResults={per_page}" 
)

results = resp.json()
playlist_id = results["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"] # Obtain the id of uploads playlist

# Create a list of videos in the upload playlist
video_list = []
page_token = ""
while True:
    resp = requests.get(
        f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails,id&playlistId={playlist_id}&key={api_key}&pageToken={page_token}&maxResults={per_page}"
    )

    resp.raise_for_status()

    records = resp.json()

    # Append list of all videos in the channel playlist
    for item in records["items"]:
        if 'videoId' in item["contentDetails"]:
            video_list.append(item["contentDetails"]["videoId"])

    if not records.get("nextPageToken", None):
        break

    page_token = records["nextPageToken"] # Youtube pagination works with page tokens

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
# Obtaining video statistics for each item in the video list
for video in video_list:
    resp = requests.get(
        f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video}&key={api_key}"
    )
    # Response includes {"viewCount", "likeCount", "favoriteCount", "commentCount"}
    stats = {key: int(value) for key, value in resp.json()["items"][0]["statistics"].items()}
    stats["video_id"] = video
    #stats["timestamp"] = now
    print(json.dumps(stats))


