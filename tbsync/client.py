import os
from functools import lru_cache

from huggingface_hub import HfApi


@lru_cache()
def get_huggingface_client() -> HfApi:
    return HfApi(token=os.environ.get('HF_TOKEN'))
