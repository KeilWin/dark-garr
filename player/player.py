import pprint
from typing import Union


from discord import FFmpegPCMAudio
from yandex_music import Client


class Player:
    _token: str
    _client: Client

    def __init__(self, token, save_path='./music/track.mp3'):
        self._save_path = save_path
        self._token = token
        self._client = Client(self._token).init()
        self._queue = list()

    def get_test(self, query):
        return self._client.search(query).best.fetch_track().download(self._save_path)

    def search_track(self, query):
        tracks = self._client.search(query, type_='track').tracks
        if len(tracks.results) > 0:
            tracks.results[0].download(self._save_path)
            return True
        else:
            return None

def test():
    p = Player('y0_AgAAAABR_IOqAAG8XgAAAADT4iyVI7IhvWkSQbeEOnizGu7fAh6uEr4')
    track = p.search_track('number one')
    pprint.pprint(track)


if __name__ == '__main__':
    test()
