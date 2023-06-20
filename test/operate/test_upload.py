import os.path

import pytest
from hbutils.random import random_sha1_with_timestamp

from tbsync.operate import upload_log_directory
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
class TestOperateUpload:
    def test_upload_log_directory_native(self, hf_space_repo, hf_filesystem):
        upload_log_directory(
            hf_space_repo,
            get_testfile('resnet18-safe'),
        )

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

    def test_upload_log_directory_with_name(self, hf_space_repo, hf_filesystem):
        upload_log_directory(
            hf_space_repo,
            get_testfile('resnet18-safe'),
            name='custom_name'
        )

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

    def test_upload_log_directory_with_anonymous(self, hf_space_repo, hf_filesystem):
        upload_log_directory(
            hf_space_repo,
            get_testfile('resnet18-safe'),
            anonymous=True
        )

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
