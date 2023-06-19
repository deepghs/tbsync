import os

import pytest
from huggingface_hub import HfFileSystem, HfApi


@pytest.fixture(scope='session')
def hf_filesystem():
    return HfFileSystem(token=os.environ.get('HF_TOKEN'))


@pytest.fixture(scope='session')
def hf_client():
    return HfApi(token=os.environ.get('HF_TOKEN'))
