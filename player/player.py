import pprint
from typing import Union


from discord import FFmpegPCMAudio
from yandex_music import Client


from player import errors

class Player:
    _token: str
    _client: Client

    @property
    def playlist(self):
        return self._playlist

    def __init__(self, token, save_path='./music/track.mp3'):
        self._save_path = save_path
        self._token = token
        self._client = Client(self._token).init()
        self._queue = list()

        self._playlist = list()

    def get_test(self, query):
        return self._client.search(query).best.fetch_track().download(self._save_path)

    def search_track(self, query):
        tracks = self._client.search(query, type_='track').tracks
        if tracks is None or len(tracks.results) == 0:
            raise errors.SearchNoFindError
        return tracks.results   # [0].download(self._save_path)

    def download_track(self, track):
        track.download(self._save_path)

    def _get_album(self, id_: int):
        album = self._client.albums_with_tracks(id_)
        volumes = album.volumes
        self._playlist = volumes[0]
        return volumes[0]

    def _get_playlist(self, link: str):
        playlist = self._client.playlists_list(link)
        self._playlist = playlist  # заглушка

    def get_next(self):
        if len(self._playlist) == 0:
            raise errors.PlaylistEmptyError()
        track = self._playlist.pop(0)
        self.download_track(track)
        return track

    def link_eater(self, link: str):
        """
        https://music.yandex.ru/users/isermak/playlists/1025
        https://music.yandex.ru/album/5231367
        :param link:
        :return:
        """
        if 'https://music.yandex.ru/' not in link:
            raise errors.LinkInvalidError()
        if link[24:29] == 'album':
            return self._get_album(int(link[30:]))
        if link[24:29] == 'users':
            self._get_playlist(link)


def test():
    p = Player('y0_AgAAAABR_IOqAAG8XgAAAADT4iyVI7IhvWkSQbeEOnizGu7fAh6uEr4')
    p.link_eater('https://music.yandex.ru/album/3657221')


if __name__ == '__main__':
    test()
