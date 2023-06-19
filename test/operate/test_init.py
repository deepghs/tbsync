import os
import pathlib
import platform

import pytest
from hbutils.random import random_sha1_with_timestamp
from hbutils.testing import isolated_directory

from tbsync.operate import init_tb_space_to_local, init_tb_space


@pytest.mark.unittest
class TestOperateInit:
    def test_init_tb_space_to_local(self):
        with isolated_directory():
            init_tb_space_to_local('deepghs/example_repo_233', '.')
            assert set(os.listdir('.')) == \
                   {'requirements.txt', 'Dockerfile', 'runs', '.gitignore', 'README.md', '.gitattributes'}

            req_lines = pathlib.Path('requirements.txt').read_text().strip().splitlines(keepends=False)
            assert len(req_lines) == 1
            assert req_lines[0] == 'tensorboard'

            dockerfile_text = pathlib.Path('Dockerfile').read_text()
            assert f'python:{platform.python_version()}' in dockerfile_text
            assert os.listdir('runs') == ['.keep']

            readme_text = pathlib.Path('README.md').read_text()
            assert 'title: Example Repo 233' in readme_text
            assert 'license: mit' in readme_text
            assert 'app_port: 6006' in readme_text

    def test_tb_space_with_args(self):
        with isolated_directory():
            init_tb_space_to_local(
                'deepghs/example_repo_233', '.',
                title='This is The Title', python_version='3.10.1',
                tensorboard_version='2.3.3',
            )
            assert set(os.listdir('.')) == \
                   {'requirements.txt', 'Dockerfile', 'runs', '.gitignore', 'README.md', '.gitattributes'}

            req_lines = pathlib.Path('requirements.txt').read_text().strip().splitlines(keepends=False)
            assert len(req_lines) == 1
            assert req_lines[0] == 'tensorboard==2.3.3'

            dockerfile_text = pathlib.Path('Dockerfile').read_text()
            assert f'python:3.10.1' in dockerfile_text
            assert os.listdir('runs') == ['.keep']

            readme_text = pathlib.Path('README.md').read_text()
            assert 'title: This is The Title' in readme_text
            assert 'license: mit' in readme_text
            assert 'app_port: 6006' in readme_text

    def test_init_tb_space(self, hf_filesystem, hf_client):
        repo = f'narugo/example_repo_233_{random_sha1_with_timestamp()}'

        init_tb_space(repo, 'This is The Title')
        try:
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
