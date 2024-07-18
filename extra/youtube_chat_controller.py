from googleapiclient.discovery import build
import json
import os

from dotenv import load_dotenv

load_dotenv()

# APIキーを設定
API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# YouTube APIクライアントを構築
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

# ライブ配信のビデオIDを設定
VIDEO_ID = 'czixo226_kw'

def chat_list():
    # ライブ配信の詳細情報を取得
    video_response = youtube.videos().list(
        part='liveStreamingDetails',
        id=VIDEO_ID
    ).execute()

    live_chat_id = video_response['items'][0]['liveStreamingDetails']['activeLiveChatId']

    # ライブチャットメッセージを取得
    chat_response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part='snippet,authorDetails',
        maxResults=2000
    ).execute()

    return [{'etag': item['etag'], 'message': item['snippet']['displayMessage']} for item in chat_response['items']]
    # # チャットメッセージを表示
    # for item in chat_response['items']:
    #     author = item['authorDetails']['displayName']
    #     message = item['snippet']['displayMessage']
    #     print(f'{author}: {message}')
