import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import googleapiclient.discovery

# Replace this with the URL of the YouTube video you want to get data for
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Extract the video ID from the URL
video_id = video_url.split("?v=")[1]

# Authenticate with the YouTube API
creds = Credentials.from_authorized_user_info(info=None)
service = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

# Call the YouTube API to get data for the video
video_response = service.videos().list(part="snippet,statistics", id=video_id).execute()

# Print the basic data for the video
video_data = video_response["items"][0]
print(f"Video title: {video_data['snippet']['title']}")
print(f"Video description: {video_data['snippet']['description']}")
print(f"Video view count: {video_data['statistics']['viewCount']}")
print(f"Video like count: {video_data['statistics']['likeCount']}")
print(f"Video dislike count: {video_data['statistics']['dislikeCount']}")
