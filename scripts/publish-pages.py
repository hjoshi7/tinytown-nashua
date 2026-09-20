#!/usr/bin/env python3
"""Publish the staged website to gh-pages without switching the source checkout."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def git(*args, **kwargs):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, **kwargs).strip()


def main():
    if git('status', '--porcelain'):
        raise SystemExit('Commit source changes before publishing.')
    if git('remote', 'get-url', '--push', 'origin') != 'https://github.com/hjoshi7/tinytown-nashua.git':
        raise SystemExit('origin must point to the Nashua repository.')
    source = git('rev-parse', 'HEAD')
    subprocess.run([sys.executable, str(ROOT / 'scripts/stage-pages.py')], cwd=ROOT, check=True)
    remote = subprocess.run(['git', 'ls-remote', '--exit-code', 'origin', 'refs/heads/gh-pages'],
                            cwd=ROOT, capture_output=True, text=True)
    parents = []
    if remote.returncode == 0:
        subprocess.run(['git', 'fetch', 'origin', 'refs/heads/gh-pages:refs/remotes/origin/gh-pages'], cwd=ROOT, check=True)
        parents = ['-p', git('rev-parse', 'refs/remotes/origin/gh-pages')]
    elif remote.returncode != 2:
        raise SystemExit(remote.stderr)
    with tempfile.TemporaryDirectory(prefix='nashua-pages-') as temporary:
        environment = {**os.environ, 'GIT_INDEX_FILE': str(Path(temporary) / 'index')}
        base = ['git', '--git-dir=' + str(ROOT / '.git'), '--work-tree=' + str(ROOT / 'dist/nashua'),
                '-c', 'core.sparseCheckout=false', '-c', 'core.sparseCheckoutCone=false']
        subprocess.run(base + ['read-tree', '--empty'], cwd=ROOT, env=environment, check=True)
        subprocess.run(base + ['add', '--all'], cwd=ROOT / 'dist/nashua', env=environment, check=True)
        tree = subprocess.check_output(base + ['write-tree'], cwd=ROOT, env=environment, text=True).strip()
    deployment = git('commit-tree', tree, *parents, input=f'Publish Nashua from {source}\n')
    # Normal push: a concurrent publication is rejected rather than overwritten.
    subprocess.run(['git', 'push', 'origin', deployment + ':refs/heads/gh-pages'], cwd=ROOT, check=True)
    print('Published deployment commit:', deployment)
    print('Source commit:', source)


if __name__ == '__main__':
    main()
