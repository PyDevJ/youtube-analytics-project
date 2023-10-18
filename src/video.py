import os
from googleapiclient.discovery import build


class Video:
    """Получает статистику видео по его id."""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id  # id видео
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id).execute()
        self.video_title: str = video_response['items'][0]['snippet']['title']  # название видео
        self.link = f"https://www.youtube.com/watch?v={video_id}"  # ссылка на видео
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']  # количество просмотров
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']  # количество лайков

    def __str__(self):
        """Возвращает название видео"""
        return self.video_title


class PLVideo(Video):
    """Дочерний класс от 'Video' использующий 'id плейлиста'."""
    def __init__(self, video_id, id_playlist):
        """Инициализируется  'id видео' и 'id плейлиста'."""
        super().__init__(video_id)
        self.id_playlist = id_playlist
