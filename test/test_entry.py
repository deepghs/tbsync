import os
import platform

import pytest
from hbutils.random import random_sha1_with_timestamp
from hbutils.testing import simulate_entry

from tbsync.config.meta import __VERSION__
from tbsync.entry import cli
from test.testings import get_testfile


@pytest.fixture()
def hf_space_repo(hf_client):
    repository = f'narugo/test_space_{random_sha1_with_timestamp()}'
    hf_client.create_repo(repo_id=repository, repo_type='space', exist_ok=True, private=True, space_sdk='docker')
    try:
        yield repository
    finally:
        hf_client.delete_repo(repo_id=repository, repo_type='space')


@pytest.mark.unittest
class TestEntry:
    def test_version(self):
        r = simulate_entry(cli, ['tbsync', '-v'])
        assert r.exitcode == 0
        assert 'tbsync' in r.stdout.lower()
        assert __VERSION__ in r.stdout.lower()

    def test_init(self, hf_filesystem, hf_client):
        repo = f'narugo/test_repo_init_{random_sha1_with_timestamp()}'

        r = simulate_entry(cli, ['tbsync', 'init', '-r', repo, '-t', 'This is The Title'])
        try:
            assert r.exitcode == 0

            root_items = [
                os.path.relpath(item['name'], start=f'spaces/{repo}/')
                for item in hf_filesystem.ls(f'spaces/{repo}/')
            ]
            assert set(root_items) == \
                   {'requirements.txt', 'Dockerfile', 'runs', '.gitignore', 'README.md', '.gitattributes'}

            req_lines = hf_filesystem.read_text(f'spaces/{repo}/requirements.txt').strip().splitlines(keepends=False)
            assert len(req_lines) == 1
            assert req_lines[0] == 'tensorboard'

            dockerfile_text = hf_filesystem.read_text(f'spaces/{repo}/Dockerfile')
            assert f'python:{platform.python_version()}' in dockerfile_text
            runs_items = [
                os.path.relpath(item['name'], start=f'spaces/{repo}/runs')
                for item in hf_filesystem.ls(f'spaces/{repo}/runs')
            ]
            assert runs_items == ['.keep']

            readme_text = hf_filesystem.read_text(f'spaces/{repo}/README.md')
            assert 'title: This is The Title' in readme_text
            assert 'license: mit' in readme_text
            assert 'app_port: 6006' in readme_text
        finally:
            hf_client.delete_repo(repo_id=repo, repo_type='space')

    def test_upload(self, hf_space_repo, hf_filesystem):
        r = simulate_entry(cli, ['tbsync', 'sync', '-r', hf_space_repo, '-d', get_testfile('resnet18-safe')])
        assert r.exitcode == 0

        runs_dir = f'spaces/{hf_space_repo}/runs'
        runs_items = hf_filesystem.ls(runs_dir)
        assert len(runs_items) == 1
        assert runs_items[0]['name'] == f'{runs_dir}/resnet18-safe'

        log_dir = f'{runs_dir}/resnet18-safe'
        log_items = hf_filesystem.ls(log_dir)
        assert len(log_items) == 1
        assert log_items[0]['name'] == \
               f'{runs_dir}/resnet18-safe/events.out.tfevents.1679394658.local-VirtualBox.606867.0'
        assert log_items[0]['size'] == os.path.getsize(
            get_testfile('resnet18-safe', 'events.out.tfevents.1679394658.local-VirtualBox.606867.0'))

    def test_upload_with_name(self, hf_space_repo, hf_filesystem):
        r = simulate_entry(cli, [
            'tbsync', 'sync',
            '-r', hf_space_repo,
            '-d', get_testfile('resnet18-safe'),
            '-n', 'custom_name',
        ])
        assert r.exitcode == 0

        runs_dir = f'spaces/{hf_space_repo}/runs'
        runs_items = hf_filesystem.ls(runs_dir)
        assert len(runs_items) == 1
        assert runs_items[0]['name'] == f'{runs_dir}/custom_name'

        log_dir = f'{runs_dir}/custom_name'
        log_items = hf_filesystem.ls(log_dir)
        assert len(log_items) == 1
        assert log_items[0]['name'] == \
               f'{runs_dir}/custom_name/events.out.tfevents.1679394658.local-VirtualBox.606867.0'
        assert log_items[0]['size'] == os.path.getsize(
            get_testfile('resnet18-safe', 'events.out.tfevents.1679394658.local-VirtualBox.606867.0'))

    def test_upload_with_anonymous(self, hf_space_repo, hf_filesystem):
        r = simulate_entry(cli, [
            'tbsync', 'sync',
            '-r', hf_space_repo,
            '-d', get_testfile('resnet18-safe'),
            '-A',
        ])
        assert r.exitcode == 0

        runs_dir = f'spaces/{hf_space_repo}/runs'
        runs_items = hf_filesystem.ls(runs_dir)
        assert len(runs_items) == 1
        assert runs_items[0]['name'] == f'{runs_dir}/resnet18-safe'

        log_dir = f'{runs_dir}/resnet18-safe'
        log_items = hf_filesystem.ls(log_dir)
        assert len(log_items) == 1
        assert log_items[0]['name'] == \
               f'{runs_dir}/resnet18-safe/events.out.tfevents.1679394658.' \
               f'b35a08c6339993b6b13a72e18d0f5a607160c61d6efc462f7c9e8c0b.606867.0'
        assert log_items[0]['size'] == os.path.getsize(
            get_testfile('resnet18-safe', 'events.out.tfevents.1679394658.local-VirtualBox.606867.0'))
