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
    _VALID_URL = r'https?://(?:www\.)?pixabay\.com/music/(?:[^/?#]+-)?(?P<id>\d+)'
    _TESTS = [{
        'url': 'https://pixabay.com/music/future-bass-no-copyright-music-537751/',
        'info_dict': {
            'id': '537751',
            'ext': 'mp3',
            'thumbnail': r're:^https?://.*\.png',
            'description': 'md5:45435d2ca9aba2167f98c8ed61ec105a',
            'title': 'No Copyright Music by SigmaMusicArt| Royalty-free Music',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        info = self._get_audio_info(url, video_id)
        
        return {
            'id': video_id,
            'vcodec': 'none',
            **info,
        }
