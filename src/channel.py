import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('YT_API_KEY')
    api_key1 = os.environ['api_key']

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel_info = {}

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.info_youtube()
        print(self.channel_info)

    def info_youtube(self) -> None:
        youtube = build('youtube', 'v3', developerKey=Channel.api_key1)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        # playlist_id = 'PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb'
        # playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
        #                                                part='contentDetails',
        #                                                maxResults=50,
        #                                                ).execute()
        # video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        # video_response = youtube.videos().list(part='contentDetails,statistics',
        #                                        id=','.join(video_ids)
        #                                        ).execute()
        # for video in video_response['items']:
        #     # YouTube video duration is in ISO 8601 format
        #     iso_8601_duration = video['contentDetails']['duration']
        #     duration = isodate.parse_duration(iso_8601_duration)
        #     print(duration)

        self.channel_info = json.dumps(channel, indent=2, ensure_ascii=False)