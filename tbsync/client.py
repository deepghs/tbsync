import os
from functools import lru_cache

from huggingface_hub import HfApi, HfFileSystem


@lru_cache()
def get_huggingface_client() -> HfApi:
    return HfApi(token=os.environ.get('HF_TOKEN'))


@lru_cache()
def get_huggingface_filesystem() -> HfFileSystem:
    return HfFileSystem(token=os.environ.get('HF_TOKEN'))
