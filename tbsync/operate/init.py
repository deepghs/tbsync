import datetime
import os
import pathlib
import platform
import random
import re
from typing import Optional

import emoji as emoji_
from ditk import logging
from emoji.unicode_codes import get_emoji_unicode_dict
from hbutils.string import env_template
from hbutils.system import TemporaryDirectory
from huggingface_hub import CommitOperationAdd

from ..client import get_huggingface_client

try:
    from typing import Literal
except (ImportError, ModuleNotFoundError):
    from typing_extensions import Literal

from ..template import TEMPLATE_FILES

VALID_COLORS = ["red", "yellow", "green", "blue", "indigo", "purple", "pink", "gray"]
ColorTyping = Literal["red", "yellow", "green", "blue", "indigo", "purple", "pink", "gray"]

VALID_LICENCES = [
    "openrail",
    "bigscience-openrail-m",
    "creativeml-openrail-m",
    "bigscience-bloom-rail-1.0",
    "bigcode-openrail-m",
    "afl-3.0",
    "apache-2.0",
    "artistic-2.0",
    "bsl-1.0",
    "bsd",
    "bsd-2-clause",
    "bsd-3-clause",
    "bsd-3-clause-clear",
    "c-uda",
    "cc",
    "cc0-1.0",
    "cc-by-2.0",
    "cc-by-2.5",
    "cc-by-3.0",
    "cc-by-4.0",
    "cc-by-sa-3.0",
    "cc-by-sa-4.0",
    "cc-by-nc-2.0",
    "cc-by-nc-3.0",
    "cc-by-nc-4.0",
    "cc-by-nd-4.0",
    "cc-by-nc-nd-3.0",
    "cc-by-nc-nd-4.0",
    "cc-by-nc-sa-2.0",
    "cc-by-nc-sa-3.0",
    "cc-by-nc-sa-4.0",
    "cdla-sharing-1.0",
    "cdla-permissive-1.0",
    "cdla-permissive-2.0",
    "wtfpl",
    "ecl-2.0",
    "epl-1.0",
    "epl-2.0",
    "eupl-1.1",
    "agpl-3.0",
    "gfdl",
    "gpl",
    "gpl-2.0",
    "gpl-3.0",
    "lgpl",
    "lgpl-2.1",
    "lgpl-3.0",
    "isc",
    "lppl-1.3c",
    "ms-pl",
    "mit",
    "mpl-2.0",
    "odc-by",
    "odbl",
    "openrail++",
    "osl-3.0",
    "postgresql",
    "ofl-1.1",
    "tii-falcon-llm",
    "ncsa",
    "unlicense",
    "zlib",
    "pddl",
    "lgpl-lr",
    "deepfloyd-if-license",
    "unknown",
    "other",
]

_RANDOM_EMOJIS = [
    value for key, value in get_emoji_unicode_dict('en').items()
    if len(value) == 1 and 'chart' in key
]


def init_tb_space_to_local(repository: str, output_dir: str,
                           title: Optional[str] = None, emoji: Optional[str] = None,
                           licence: str = "mit", port: int = 6006,
                           python_version: Optional[str] = None, tensorboard_version: Optional[str] = None,
                           from_color: Optional[ColorTyping] = None, to_color: Optional[ColorTyping] = None):
    logging.info(f'Creating repository config file at {output_dir!r} ...')

    words = re.split(r'[\W_]+', repository.split('/')[-1])
    title = title or ' '.join([wd.capitalize() for wd in words])
    emoji = emoji_.emojize(emoji or random.choice(_RANDOM_EMOJIS))
    from_color = from_color or random.choice(VALID_COLORS)
    to_color = to_color or random.choice(VALID_COLORS)
    python_version = python_version or platform.python_version()

    args = {
        'title': title,
        'emoji': emoji,
        'from_color': from_color,
        'to_color': to_color,
        'python_version': python_version,
        'tb_req': 'tensorboard' if not tensorboard_version else f'tensorboard=={tensorboard_version}',
        'licence': licence,
        'port': port,
    }

    os.makedirs(output_dir, exist_ok=True)
    for file, local_file in TEMPLATE_FILES:
        with open(local_file, 'r', encoding='utf-8') as if_:
            text = if_.read()
            env = {**os.environ, **{f'tbsync_{key}': value for key, value in args.items()}}

            with open(os.path.join(output_dir, file), 'w', encoding='utf-8') as of_:
                of_.write(env_template(text, env))

    runs_dir = os.path.join(output_dir, 'runs')
    os.makedirs(runs_dir, exist_ok=True)
    pathlib.Path(os.path.join(runs_dir, '.keep')).touch()


def init_tb_space(repository: str, title: Optional[str] = None, emoji: Optional[str] = None,
                  private: bool = False, licence: str = "mit", port: int = 6006,
                  python_version: Optional[str] = None, tensorboard_version: Optional[str] = None,
                  from_color: Optional[ColorTyping] = None, to_color: Optional[ColorTyping] = None):
    with TemporaryDirectory() as td:
        init_tb_space_to_local(repository, td, title, emoji, licence, port,
                               python_version, tensorboard_version, from_color, to_color)

        hf = get_huggingface_client()
        logging.info(f'Try creating repository {repository!r} ...')
        hf.create_repo(repo_id=repository, repo_type='space', exist_ok=True, private=private, space_sdk='docker')
        logging.info(f'Setting repository {repository!r}\'s visibility ...')
        hf.update_repo_visibility(repo_id=repository, repo_type='space', private=private)

        uploads = []
        for root, dirs, files in os.walk(td):
            for file in files:
                absfile = os.path.join(root, file)
                relfile = os.path.relpath(absfile, td)
                uploads.append(CommitOperationAdd(relfile, absfile))

        logging.info('Uploading files ...')
        current_time = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
        hf.create_commit(
            repo_id=repository, repo_type='space',
            operations=uploads,
            commit_message=f'Init repository {repository} via tbsync, on {current_time}'
        )
