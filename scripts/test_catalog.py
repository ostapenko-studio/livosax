"""Check generated pages, book attribution, links and structured metadata."""
import json
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    def test_catalog_pages(self):
        videos = json.loads((ROOT / 'videos.json').read_text())
        self.assertEqual(len(videos), len({v['id'] for v in videos}))
        self.assertEqual(len(videos), len({v['slug'] for v in videos}))
        home = (ROOT / 'dist/index.html').read_text()
        for v in videos:
            with self.subTest(video=v['id']):
                self.assertGreater(v['seconds'], 0)
                self.assertIn('/videos/' + v['slug'] + '/', home)
                page = (ROOT / 'dist/videos' / v['slug'] / 'index.html').read_text()
                self.assertIn('https://www.youtube-nocookie.com/embed/' + v['id'], page)
                schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', page).group(1))
                video = next(n for n in schema['@graph'] if n['@type'] == 'VideoObject')
                self.assertEqual(video['name'], v['title'])
                self.assertEqual(video['duration'], f"PT{v['seconds']}S")
                notes = page.split('<section class="piece-notes">')[1].split('</section>')[0]
                if 'artist' in v:
                    self.assertIn(v['artist'], notes)
                    self.assertIn(v['book'], notes)
                    self.assertNotIn('Essential Elements', notes)
                    self.assertNotIn('<dt>Exercise</dt>', notes)
                else:
                    self.assertIn('<dt>Exercise</dt>', notes)
                    self.assertIn('Essential Elements', notes)
        self.assertEqual(home.count('class="video-card"'), len(videos))
        self.assertEqual(home.count('class="book-collection"'), 3)
        urls = ET.parse(ROOT / 'dist/sitemap.xml').findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        self.assertEqual(len(urls), len(videos) + 1)


if __name__ == '__main__':
    unittest.main()
