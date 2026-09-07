from .common import InfoExtractor
from ..utils import url_or_none
from ..utils.traversal import traverse_obj


class PixabayBaseIE(InfoExtractor):
    # Cookie header is required or the request will 403
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://pixabay.com/',
        'Cookie': 'is_human=1;',
    }

    def _get_audio_info(self, url, video_id):
        webpage = self._download_webpage(url, video_id, headers=self._headers)
        info = self._search_json_ld(webpage, video_id, expected_type='AudioObject')

        return traverse_obj(info, {
            'url': ('url', {url_or_none}),
            'thumbnail': ('thumbnails', 0, 'url', {url_or_none}),
            'description': ('description', {str}),
            'title': ('title', {str}),
        })

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
