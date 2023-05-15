import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.environ['api_key']

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel_info = {}
        self.channel = self.get_channel(self.channel_id)
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.quality_subscribers = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.quality_views = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.quality_subscribers + other.quality_subscribers

    def __sub__(self, other):
        return self.quality_subscribers - other.quality_subscribers

    def __lt__(self, other):
        return self.quality_subscribers < other.quality_subscribers

    def __le__(self, other):
        return self.quality_subscribers <= other.quality_subscribers

    def __gt__(self, other):
        return self.quality_subscribers > other.quality_subscribers

    def __ge__(self, other):
        return self.quality_subscribers >= other.quality_subscribers


    @classmethod
    def get_channel(cls, channel_id):
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        return youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.info_youtube()
        print(self.channel_info)

    def info_youtube(self) -> None:
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.channel_info = json.dumps(channel, indent=2, ensure_ascii=False)

    def to_json(self, filename):
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'quality_subscribers': self.quality_subscribers,
            'video_count': self.video_count,
            'quality_views': self.quality_views,
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
