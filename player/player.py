import asyncio
import pprint
from typing import Union


from discord import FFmpegPCMAudio
from yandex_music import Client, ClientAsync


from player import errors
# import errors

class Player:
    _token: str
    _client: ClientAsync
    _username: dict

    @property
    def playlist(self):
        return self._playlist

    def __init__(self, token, save_path='./music/track.mp3'):
        self._save_path = save_path
        self._token = token
        self._loop = asyncio.get_event_loop()
        self._client = self._loop.run_until_complete(ClientAsync(self._token).init())
        self._queue = list()
        self._username = {
            'ksayr23': 1119477303,
            'isermak': 1375503274,
        }

        self._playlist = list()

    async def get_test(self, query):
        return (await self._client.search(query)).best.fetch_track().download(self._save_path)

    async def search_track(self, query):
        tracks = (await self._client.search(query, type_='track')).tracks
        if tracks is None or len(tracks.results) == 0:
            raise errors.SearchNoFindError
        return tracks.results   # [0].download(self._save_path)

    async def download_track(self, track):
        return await track.download_async(self._save_path)

    async def _get_album(self, id_: int):
        album = await self._client.albums_with_tracks(id_)
        volumes = album.volumes
        self._playlist = list()
        for v in volumes:
            self._playlist.extend(v)
        return volumes[0]

    async def _get_playlist(self, link: str):
        parts = link.split('/')
        username = parts[0]
        if username not in self._username:
            raise errors.PlaylistEmptyError()
        playlist_id = parts[-1]
        playlist = await (await self._client.playlists_list(f'{self._username[username]}:{playlist_id}'))[0].fetch_tracks_async()
        self._playlist = [await track.fetch_track_async() for track in playlist]
        return self._playlist

    def get_next(self):
        if len(self._playlist) == 0:
            raise errors.PlaylistEmptyError()
        track = self._playlist.pop(0)
        self.download_track(track)
        return track

    async def link_eater(self, link: str):
        """
        https://music.yandex.ru/users/isermak/playlists/1025
        https://music.yandex.ru/album/5231367
        :param link:
        :return:
        """
        if 'https://music.yandex.ru/' not in link:
            raise errors.LinkInvalidError()
        if link[24:29] == 'album':
            return await self._get_album(int(link[30:]))
        if link[24:29] == 'users':
            return await self._get_playlist(link[30:])
        raise errors.LinkInvalidError()


def test():
    p = Player('y0_AgAAAABR_IOqAAG8XgAAAADT4iyVI7IhvWkSQbeEOnizGu7fAh6uEr4')
    p.link_eater('https://music.yandex.ru/users/ksayr23/playlists/1005')


if __name__ == '__main__':
    test()
