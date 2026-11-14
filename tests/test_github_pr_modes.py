import contextlib
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

BIN = Path(__file__).resolve().parents[1] / 'plugins/github/bin'
sys.path.insert(0, str(BIN))
import _gh

URL = 'https://github.com/example/project/pull/12'
PR = {'html_url': URL, 'title': 'A change', 'state': 'open', 'body': 'Details',
      'head': {'ref': 'topic', 'repo': {'clone_url': 'https://example.test/repo', 'name': 'project'}, 'label': 'example:topic'},
      'base': {'label': 'example:main'}, 'labels': [], 'user': {'login': 'author'}}


class PullRequestModesTest(unittest.TestCase):
    def run_script(self, name, data):
        output = io.StringIO()
        with patch('sys.stdin', io.StringIO(json.dumps(data))), contextlib.redirect_stdout(output):
            runpy.run_path(str(BIN / (name + '.py')), run_name='__main__')
        return output.getvalue()

    def test_starter_publishes_distinct_mode_links(self):
        with patch.object(_gh, 'api', return_value=PR):
            result = json.loads(self.run_script('github-pr-starter', {'arg': URL}))
        self.assertNotIn('links', result)
        self.assertEqual(result['modes']['contribution']['links'], {'github.pull_request': URL})
        self.assertEqual(result['modes']['fork']['links'], {'github.forked_pull_request': URL})

    def test_manifest_gates_and_manual_linker(self):
        manifest = json.loads((BIN.parent / 'plugin.json').read_text())
        components = {c['name']: c for c in manifest['components']}
        self.assertEqual(manifest['version'], '1.3.0')
        self.assertNotIn('discover', components['github-pr-linker'])
        self.assertTrue(components['github-issue-linker']['discover']['automatic'])
        for mode, key in [('pr', 'github.pull_request'), ('forked-pr', 'github.forked_pull_request')]:
            for kind in ('description', 'comments', 'diff'):
                c = components[f'github-{mode}-{kind}-importer']
                self.assertEqual(c['inputs'], ['link:' + key])
                self.assertEqual(c['on'], [{'event': 'start:finalized'}])

    def test_importers_write_separate_equivalent_context(self):
        def api(endpoint, accept='application/vnd.github+json'):
            return 'diff content\n' if accept.endswith('diff') else PR
        with tempfile.TemporaryDirectory() as tmp, patch.object(_gh, 'api', side_effect=api), patch.object(_gh, 'paginate', return_value=[]):
            for prefix, key, folder in [('pr', 'github.pull_request', 'pull-request'), ('forked-pr', 'github.forked_pull_request', 'forked-pull-request')]:
                for kind in ('description', 'comments', 'diff'):
                    self.run_script(f'github-{prefix}-{kind}-importer', {'inputs': {key: URL}, 'output_dir': tmp})
            base = Path(tmp) / 'context/github'
            for filename in ('description.md', 'comments.md', 'changes.diff'):
                self.assertEqual((base / 'pull-request' / filename).read_text(), (base / 'forked-pull-request' / filename).read_text())
            self.assertIn('# A change (#12)', (base / 'forked-pull-request/description.md').read_text())
            self.assertEqual((base / 'forked-pull-request/changes.diff').read_text(), 'diff content\n')


if __name__ == '__main__':
    unittest.main()
