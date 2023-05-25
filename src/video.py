import json
import os

from googleapiclient.discovery import build

from src.channel import Channel


class Video:
    api_key = os.environ['api_key']

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        response = self.get_video_info(video_id)

        try:
            video_info = response['items'][0]
            self.id_channel = video_info['id']
            self.title = video_info['snippet']['title']
            self.url = f"https://www.youtube.com/channel/{video_info}"
            self.quality_views = video_info['statistics']['viewCount']
            self.quality_likes = video_info['statistics']['likeCount']
        except Exception:
            self.id_channel = video_id
            self.title = None
            self.url = None
            self.views_count = None
            self.like_count = None
            print(f"Не найден канал по данному id: {video_id}")
            # raise Exception(f"Не найден канал по данному id: {video_id}")

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_video_info(cls, video_id):
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        return youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                     id=video_id
                                     ).execute()


class PLVideo(Video):
    def __init__(self, video_id, id_playlist):
        super().__init__(video_id)
        self.id_second = id_playlist

        response = self.get_video_info(video_id)

        if response.get('items'):
            video_info = response['items'][0]
            self.id_channel = video_info['id']
            self.title = video_info['snippet']['title']
            self.url = f"https://www.youtube.com/channel/{video_info}"
            self.quality_views = video_info['statistics']['viewCount']
            self.quality_likes = video_info['statistics']['likeCount']
        else:
            raise Exception(f"Не найден канал по данному id: {video_id}")
