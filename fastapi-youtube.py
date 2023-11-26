from fastapi import FastAPI
import uvicorn
from googleapiclient.discovery import build
from pprint import pprint # es para imprimir el JSON limpiamente
import time
from datetime import datetime

app = FastAPI()

API_KEY= 'YOUR API KEY'

'''This object allows you to interact with the youyube interface,
 I left it here so as not to repeat it in all the functions'''
youtube = build('youtube', 'v3', developerKey=API_KEY)

'''The following function provides a way to get the ID of a YouTube channel given its URL.
 It can handle both URLs with custom usernames and direct URLs to the channel,
   returning the corresponding channel ID.'''
def channel_id_function(url:str):
  if '@' in url:
      username = url.split('@')[-1]
      request_url = youtube.search().list(part='snippet', type='channel', q=username).execute()
      channel_id = request_url['items'][0]['snippet']['channelId']

  elif '/channel/' in url:
      channel_id = url.split('/')[-1]
  return channel_id


'''This function obtains information about a YouTube channel
   when it receives the video URL'''
@app.get('/get_channel_data')
def get_channel_data(url:str):

    channel_id = channel_id_function(url)

    request = youtube.channels().list(part='statistics, snippet', id=channel_id).execute()
 
    channel_title = request['items'][0]['snippet'].get('title', None)
    custom_url = f"https://www.youtube.com/{request['items'][0]['snippet']['customUrl']}"
    id_url = f"https://www.youtube.com/channel/{request['items'][0]['id']}"
    description = request['items'][0]['snippet'].get('description', None)
    subscriber_count = request['items'][0]['statistics'].get('subscriberCount', None)
    video_count = request['items'][0]['statistics'].get('videoCount', None)
    view_count_general = request['items'][0]['statistics'].get('viewCount')
    
    return {
        'channel title': channel_title,
        'custom url': custom_url,
        'id url': id_url,
        'description': description,
        'subscriber count': subscriber_count,
        'video count': video_count,
        'view count': view_count_general,
    }

'''This function obtains information about a video from a YouTube channel
   when it receives the URL of the video'''
@app.get('/get_video_data')
def get_video_data(url:str):

    video_id = url.split('v=')[-1]
    #I check for additional parameters in the URL after video id.
    #If there are one or more additional parameters I delete them
    if '&' in video_id:
        video_id = video_id.split('&')[0]
    
    video_response = youtube.videos().list(
        part = 'snippet, statistics',
        id = video_id,
        ).execute()

    title = video_response['items'][0]['snippet'].get('title')
    published_at = video_response['items'][0]['snippet'].get('publishedAt', None)
    description = video_response['items'][0]['snippet'].get('description', None)
    category_id = video_response['items'][0]['snippet'].get('categoryId', None)
    view_count = video_response['items'][0]['statistics'].get('viewCount', None)
    comment_count = video_response['items'][0]['statistics'].get('commentCount', None)
    like_count = video_response['items'][0]['statistics'].get('likeCount', None)
    view_count = video_response['items'][0]['statistics'].get('viewCount', None)
    Consultation_date = datetime.now().strftime("%Y-%m-%d")

    category_response = youtube.videoCategories().list(
        part = 'snippet',
        id = category_id,
        ).execute()

    category = category_response['items'][0]['snippet'].get('title', None)

    return {
        'url': f'https://www.youtube.com/watch?v={video_id}',
        'title': title,
        'published at' : published_at,
        'description': description,
        'view count': view_count,
        'comment count': comment_count,
        'like count': like_count,
        'category': category,
        'Consultation date': Consultation_date,
    }

'''This function obtains information
   from all the videos on a YouTube channel.'''
@app.get('/get_channel_videos')
def get_channel_videos(url: str):

    channel_id = channel_id_function(url)

    videos = []
    next_page_token = None

    '''This loop retrieves a list of video IDs from a YouTube channel
       and handles pagination of results using page tokens (next_page_token).
       This loop will run until there are no more pages of results to retrieve.'''
    while True:
        video_response = youtube.search().list(
            part='id',
            channelId=channel_id,
            maxResults=50,  # Maximum value allowed
            pageToken=next_page_token
        ).execute()

        videos.extend(video_response.get('items', []))
        next_page_token = video_response.get('nextPageToken')

        if not next_page_token:
            break

    #I extract the id of each video and store it
    #  in the variable videos_ids
    videos_ids = []
    for item in videos:
        try:
            # I don't use "get" because I don't need it to return "None" in case "videoId" is not found.
            videos_ids.append(item['id']['videoId']) 
        except: pass
    
    #I store the information of each video in videos_list
    videos_list = []
    for video_id in videos_ids:
        video_list = get_video_data(video_id)
        videos_list.append(video_list)
        time.sleep(0.01)


    return videos_list
