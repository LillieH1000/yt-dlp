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


class PixabaySoundMusicIE(PixabayBaseIE):
    _VALID_URL = r'https?://(?:www\.)?pixabay\.com/(?:music|sound-effects)/(?:[^/?#]+-)?(?P<id>\d+)'
    _TESTS = [
        # Music
        {
            'url': 'https://pixabay.com/music/future-bass-no-copyright-music-537751/',
            'info_dict': {
                'id': '537751',
                'ext': 'mp3',
                'thumbnail': r're:^https?://.*\.(?:png|jpg)',
                'description': 'md5:45435d2ca9aba2167f98c8ed61ec105a',
                'title': 'No Copyright Music by SigmaMusicArt| Royalty-free Music',
            },
        },
        # Sound Effect
        {
            'url': 'https://pixabay.com/sound-effects/film-special-effects-calm-inspiring-technology-logo-short-version-518993/',
            'info_dict': {
                'id': '518993',
                'ext': 'mp3',
                'thumbnail': r're:^https?://.*\.(?:png|jpg)',
                'description': 'md5:9d3ae9314a08fa7c1ebfef797abd5068',
                'title': 'Calm Inspiring Technology Logo (Short Version) by AleXZavesa| Royalty-free Music',
            },
        },
        # Sound Effect - no thumbnail
        {
            'url': 'https://pixabay.com/sound-effects/musical-relaxing-guitar-loop-v5-245859/',
            'info_dict': {
                'id': '245859',
                'ext': 'mp3',
                'description': 'md5:64136651e70263d7fc965fe8a0d61435',
                'title': 'Relaxing Guitar Loop V5 by IdoBerg| Royalty-free Music',
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
