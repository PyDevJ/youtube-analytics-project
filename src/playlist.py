import datetime
import isodate
from src.channel import Channel


class PlayList(Channel):
    """Класс для плейлиста из ютуб который инициализируется _id_ плейлиста."""

    def __init__(self, id_playlist: str):
        self.id_playlist = id_playlist
        self.title = self.get_playlist_title()
        self.url = "https://www.youtube.com/playlist?list=" + self.id_playlist

    def get_playlist_info(self):
        """Получает данные по видеороликам в плейлисте по его id."""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.id_playlist,
                                                                  part='contentDetails,snippet',
                                                                  maxResults=50,).execute()
        return playlist_videos

    def get_playlist_title(self):
        """Получает название плейлиста."""
        playlist_title = ""
        channel_id = self.get_playlist_info()["items"][0]["snippet"]["channelId"]
        playlists = self.get_service().playlists().list(channelId=channel_id, part='snippet',
                                                        maxResults=50).execute()
        for playlist in playlists["items"]:
            if self.id_playlist == playlist["id"]:
                playlist_title = playlist["snippet"]["title"]
                break
        return playlist_title
        # print(playlist_title)

    def get_video_playlist(self):
        """Получает все id видеороликов из плейлиста и выводит длительности видеороликов."""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                self.get_playlist_info()['items']]
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)).execute()
        return video_response

    @property
    def total_duration(self):
        """возвращает суммарную длительность плейлиста"""
        total_time = []
        result_time = 0
        for video in self.get_video_playlist()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time.append(duration)
            result_time = sum(total_time, datetime.timedelta())
        return result_time

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)."""
        video_likes = []
        most_liked_video = ""
        for likes in self.get_video_playlist()["items"]:
            video_likes.append(int(likes["statistics"]["likeCount"]))
        max_likes_video = max(video_likes)
        for likes in self.get_video_playlist()["items"]:
            if int(likes["statistics"]["likeCount"]) == max_likes_video:
                most_liked_video = "https://youtu.be/" + likes["id"]
        return most_liked_video
