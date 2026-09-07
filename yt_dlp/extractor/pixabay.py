from .common import InfoExtractor
from ..utils import url_or_none
from ..utils.traversal import require, traverse_obj


class PixabayBaseIE(InfoExtractor):
    def _get_page_props(self, url, video_id):
        webpage = self._download_webpage(url, video_id)
        return self._search_nextjs_data(webpage, video_id)['props']['pageProps']

    @staticmethod
    def _get_playback_url(data):
        return traverse_obj(data, (
            'playback', lambda _, v: v['canUse'] == 'true',
            'url', {url_or_none}, any, {require('playback URL')}))

class PixabayMusicIE(PixabayBaseIE):
    _VALID_URL = r'https?://www\.globalplayer\.com/music/(?P<id>\w+)'
    _TESTS = [{
        'url': 'https://pixabay.com/music/future-bass-no-copyright-music-537751/',
        'info_dict': {
            'id': '2JsSZ7Gm2uP',
            'ext': 'mp4',
            'thumbnail': 'md5:d4498af48e15aae4839ce77b97d39550',
            'description': 'md5:6a9f063c67c42f218e42eee7d0298bfd',
            'title': 'Treble Malakai Bayoh sings a sublime Handel aria at Classic FM Live',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        meta = self._get_page_props(url, video_id)['videoData']

        return {
            'id': video_id,
            **traverse_obj(meta, {
                'url': ('url', {url_or_none}),
                'thumbnail': ('image', 'url', {url_or_none}),
                'description': ('description', {str}),
                'title': ('title', {str}),
            }),
        }
