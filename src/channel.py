import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube/channels/{self.__channel_id}"
        self.subscriber_count = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel['items'][0]['statistics']['viewCount'])

    def __str__(self):
        """Магический метод возвращающий название и ссылку на канал."""
        return f"{self.title} {self.url}"

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Класс-метод возвращающий объект для работы с YouTube API."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, file_json):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        json_data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }
        with open(file_json, 'w', encoding="utf-8") as f:
            f.write(json.dumps(json_data, ensure_ascii=False, indent=4))

    def __add__(self, other):
        """Складывает два канала по количеству подписчиков"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Вычитает из первого канала количество подписчиков второго канала"""
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        """Сравнивает больше или нет количество подписчиков первого канала со вторым, возвращает 'bool'."""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """Сравнивает больше или равно количество подписчиков первого канала со вторым, возвращает 'bool'."""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """Сравнивает меньше или нет количество подписчиков первого канала со вторым, возвращает 'bool'."""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """Сравнивает меньше или равно количество подписчиков первого канала со вторым, возвращает 'bool'."""
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """Сравнивает равно ли количество подписчиков первого канала со вторым, возвращает 'bool'."""
        return self.subscriber_count == other.subscriber_count
