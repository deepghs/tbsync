import datetime
import glob
import os
import re
from typing import Optional

from ditk import logging
from hbutils.encoding import sha3
from huggingface_hub import CommitOperationAdd

from ..client import get_huggingface_client

_LOG_FILE_GLOB = 'events.out.tfevents.*'
_LOG_FILE_PATTERN = re.compile(r'^events\.out\.tfevents\.(?P<timestamp>\d+)\.(?P<machine>[^.]+)\.(?P<extra>[\s\S]+)$')


def upload_log_directory(repository: str, logdir, name: Optional[str] = None, anonymous: bool = False):
    name = name or os.path.basename(os.path.abspath(logdir))

    hf = get_huggingface_client()
    uploads = []
    for logfile in glob.glob(os.path.join(logdir, _LOG_FILE_GLOB)):
        matching = _LOG_FILE_PATTERN.fullmatch(os.path.basename(logfile))
        assert matching, f'Log file {logfile!r}\'s name not match with pattern {_LOG_FILE_PATTERN.pattern}.'

        timestamp = matching.group('timestamp')
        machine = matching.group('machine')
        if anonymous:
            machine = sha3(machine.encode(), n=224)
        extra = matching.group('extra')

        final_name = f'events.out.tfevents.{timestamp}.{machine}.{extra}'
        file_in_repo = f'runs/{name}/{final_name}'
        uploads.append(CommitOperationAdd(file_in_repo, logfile))
        logging.info(f'Scanned {logfile!r} --> {file_in_repo!r}')

    logging.info('Uploading log files ...')
    current_time = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')
    hf.create_commit(
        repo_id=repository, repo_type='space',
        operations=uploads,
        commit_message=f'Upload tensorboard log {name!r} via tbsync, on {current_time}'
    )
