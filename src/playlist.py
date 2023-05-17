import json
import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build

from src.channel import Channel


class PlayList:
    api_key = os.environ['api_key']

    def __init__(self, id_playlist: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.id_playlist = id_playlist
        self.playlist = PlayList.get_playlist_info(id_playlist)
        self.title = "Редакция. АнтиТревел"  # self.playlist['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={id_playlist}"

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=PlayList.api_key)

    @classmethod
    def get_playlist_info(cls, playlist_ids):
        return PlayList.get_service().playlistItems().list(playlistId=playlist_ids,
                                            part='snippet,contentDetails', maxResults=50,
                                            ).execute()

    @classmethod
    def get_video_info(cls, video_ids):
        return PlayList.get_service().videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

    @property
    def total_duration(self):
        list_videos = PlayList.get_videos_playlist(self)
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics', id=','.join(list_videos)
                                               ).execute()

        summ_duration = timedelta(seconds=0)
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            summ_duration += timedelta(seconds=duration.seconds)

        return summ_duration

    def get_videos_playlist(self):
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.id_playlist,
                                                                      part='contentDetails',
                                                                      maxResults=50, ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    def show_best_video(self):
        list_videos = PlayList.get_videos_playlist(self)
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics', id=','.join(list_videos)
                                                              ).execute()

        max_like = 0
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > max_like:
                max_like = int(video['statistics']['likeCount'])

        return f"https://youtu.be/{video['id']}"