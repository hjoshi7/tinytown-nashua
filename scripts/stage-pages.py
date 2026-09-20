#!/usr/bin/env python3
"""Stage the existing Nashua miniature for its GitHub Pages project URL."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tinytown.deploy import build

PAGE_URL = 'https://hjoshi7.github.io/tinytown-nashua/'


def main():
    output = build('nashua', root=ROOT)
    document = (output / 'index.html').read_text()
    # Run before upstream reads URL options. Explicit visitor choices are retained.
    defaults = '''
  <script>
    {
      const url = new URL(location.href);
      if (!url.searchParams.has('stream')) url.searchParams.set('stream', '1');
      if (!url.searchParams.has('focus')) {
        url.searchParams.set('focus', '32285517');
        if (!url.searchParams.has('dist')) url.searchParams.set('dist', '450');
      }
      document.documentElement.dataset.pagesView = url.searchParams.get('tiles') === '1' ? 'debug' : 'public';
      history.replaceState(null, '', url);
    }
  </script>
  <style>html[data-pages-view="public"] #stream-debug { display: none; }</style>
'''
    if document.count('<head>') != 1:
        raise RuntimeError('Expected one viewer head element')
    document = document.replace('<head>', '<head>' + defaults, 1)
    # Project Pages lives below /tinytown-nashua/, not at the account root.
    for icon in ('favicon.ico', 'favicon.png', 'favicon.svg', 'apple-touch-icon.png'):
        document = document.replace(f'href="/{icon}"', f'href="./{icon}"')
    document = document.replace('content="/social-preview.jpg', f'content="{PAGE_URL}social-preview.jpg')
    document = document.replace('</head>', f'<link rel="canonical" href="{PAGE_URL}" />\n</head>', 1)
    (output / 'index.html').write_text(document)
    (output / '.nojekyll').write_text('')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    (output / 'deployment.json').write_text(json.dumps({'source_commit': revision, 'site': 'nashua'}, indent=2) + '\n')
    print(output)


if __name__ == '__main__':
    main()
