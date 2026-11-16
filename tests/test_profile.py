import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from render_profile import outputs, validate
from collect_languages import RefreshError, collect, selected_repositories


class ProfileTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))
        self.config = {'owner': self.data['handle'], 'repositories': ['allowed', 'secret-project'], 'exclude': ['secret project']}

    def metadata(self, name='allowed', **changes):
        return dict({'name': name, 'owner': {'login': self.data['handle']}, 'private': True, 'fork': False, 'archived': False}, **changes)

    def test_exclusion_precedes_all_network_requests(self):
        seen = []
        def get(path):
            seen.append(path)
            return {'Python': 400} if path.endswith('/languages') else self.metadata()
        candidate = collect(self.data, self.config, get, '2026-11-16')
        self.assertEqual(candidate['snapshot']['languages'], {'Python': 400})
        self.assertEqual(candidate['snapshot']['repository_count'], 1)
        self.assertEqual(len(seen), 2)
        self.assertTrue(all('secret' not in path for path in seen))

    def test_exclusion_normalizes_case_punctuation_and_suffixes(self):
        self.config['repositories'] = ['allowed', 'SECRET_Project-backend', 'secret.project', 'secret-project']
        self.assertEqual(selected_repositories(self.config), ['allowed'])

    def test_partial_failure_preserves_input(self):
        original = copy.deepcopy(self.data)
        self.config['repositories'] = ['allowed', 'unavailable']
        def get(path):
            if 'unavailable' in path:
                raise RefreshError('fetch: GitHub HTTP 404; candidate unchanged')
            return {'Python': 400} if path.endswith('/languages') else self.metadata()
        with self.assertRaises(RefreshError):
            collect(self.data, self.config, get, '2026-11-16')
        self.assertEqual(self.data, original)

    def test_empty_response_does_not_fake_statistics(self):
        with self.assertRaisesRegex(RefreshError, 'no eligible language data'):
            collect(self.data, self.config, lambda p: {} if p.endswith('/languages') else self.metadata(), '2026-11-16')

    def test_duplicates_and_missing_exclusions_rejected(self):
        for repos, exclude in [(['allowed', 'Allowed'], ['secret']), (['allowed'], [])]:
            with self.subTest(repos=repos, exclude=exclude), self.assertRaises(RefreshError):
                selected_repositories(dict(self.config, repositories=repos, exclude=exclude))

    def test_private_payload_fields_rejected(self):
        for location in ('root', 'project', 'snapshot'):
            data = copy.deepcopy(self.data)
            item = data if location == 'root' else data['projects'][0] if location == 'project' else data['snapshot']
            item['raw_repository'] = 'private-material'
            with self.subTest(location=location), self.assertRaises(ValueError):
                validate(data)

    def test_invalid_counts_and_identity_rejected(self):
        for count in (-1, 0, 1.5, True, float('nan'), float('inf')):
            data = copy.deepcopy(self.data)
            data['snapshot']['languages'] = {'Python': count}
            with self.subTest(count=count), self.assertRaises(ValueError):
                validate(data)
        self.data['handle'] = 'user/../other'
        with self.assertRaises(ValueError):
            validate(self.data)

    def test_markup_injection_and_links_rejected(self):
        for value in ('<script>alert(1)</script>', '[click](https://example.com)', 'user@example.com', 'line\nbreak'):
            self.data['bio'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(self.data)

    def test_escaping_and_deterministic_rendering(self):
        self.data['name'] = 'A & B'
        first, second = outputs(self.data), outputs(copy.deepcopy(self.data))
        self.assertEqual(first, second)
        self.assertIn('A &amp; B', first['assets/workshop-dark.svg'])
        for path, content in first.items():
            self.assertNotIn('{{', content, path)
            if path.endswith('.svg'):
                ET.fromstring(content)

    def test_generated_assets_match_snapshot(self):
        for path, content in outputs(self.data).items():
            self.assertEqual((ROOT / path).read_text(encoding='utf-8'), content, path)

    def test_static_and_reduced_motion_available(self):
        files = outputs(self.data)
        for tone in ('dark', 'light'):
            self.assertNotIn('animation:', files[f'assets/workshop-static-{tone}.svg'])
            self.assertIn('prefers-reduced-motion:reduce', files[f'assets/workshop-{tone}.svg'])

    def test_preview_local_image_targets_exist(self):
        paths = []
        class Images(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'img':
                    paths.append(dict(attrs)['src'])
        Images().feed(outputs(self.data)['preview/index.html'])
        self.assertTrue(paths)
        for path in paths:
            self.assertTrue((ROOT / 'preview' / path).resolve().is_file())


if __name__ == '__main__':
    unittest.main()
