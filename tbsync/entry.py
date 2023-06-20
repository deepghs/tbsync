import platform
from functools import partial
from typing import Optional

import click
from ditk import logging

from .operate import init_tb_space, upload_log_directory
from .operate.init import ColorTyping, VALID_LICENCES, VALID_COLORS
from .utils import GLOBAL_CONTEXT_SETTINGS
from .utils import print_version as _origin_print_version

print_version = partial(_origin_print_version, 'tbsync')


@click.group(context_settings={**GLOBAL_CONTEXT_SETTINGS})
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Utils with gchar.")
def cli():
    pass  # pragma: no cover


@cli.command('init', context_settings={**GLOBAL_CONTEXT_SETTINGS},
             help='Initialize huggingface space repository.')
@click.option('-r', '--repository', 'repository', type=str, required=True,
              help='Repository on huggingface.', show_default=True)
@click.option('-t', '--title', 'title', type=str, default=None,
              help='Title of the repository, capitalized repository name will be used if not given.')
@click.option('-e', '--emoji', 'emoji', type=str, default=None,
              help='Emoji to use for repository, see emoji library for details. '
                   'Random emoji will be used when not given.')
@click.option('-p', '--private', 'private', is_flag=True, type=bool, default=False,
              help='Create private repository.', show_default=True)
@click.option('-l', '--licence', 'licence', type=click.Choice(VALID_LICENCES), default='mit',
              help='Licence for repository.', show_default=True)
@click.option('--port', 'port', type=int, default=6006,
              help='Port of tensorboard in space.', show_default=True)
@click.option('-P', '--python_version', 'python_version', type=str, default=platform.python_version(),
              help='Version of python to use.', show_default=True)
@click.option('-T', '--tensorboard_version', 'tensorboard_version', type=str, default=None,
              help='Version of tensorboard to use.', show_default=True)
@click.option('--from_color', 'from_color', type=click.Choice(VALID_COLORS), default=None,
              help='From color of space block. Random color will be used when not given.')
@click.option('--to_color', 'to_color', type=click.Choice(VALID_COLORS), default=None,
              help='To color of space block. Random color will be used when not given.')
def init(repository: str, title: Optional[str] = None, emoji: Optional[str] = None,
         private: bool = False, licence: str = "mit", port: int = 6006,
         python_version: Optional[str] = None, tensorboard_version: Optional[str] = None,
         from_color: Optional[ColorTyping] = None, to_color: Optional[ColorTyping] = None):
    logging.try_init_root(logging.INFO)
    init_tb_space(
        repository, title, emoji, private, licence, port,
        python_version, tensorboard_version, from_color, to_color
    )


@cli.command('sync', context_settings={**GLOBAL_CONTEXT_SETTINGS},
             help='Upload log file to huggingface space repository.')
@click.option('-r', '--repository', 'repository', type=str, required=True,
              help='Repository on huggingface.', show_default=True)
@click.option('-d', '--directory', 'logdir',
              type=click.Path(file_okay=False, dir_okay=True, exists=True), required=True,
              help='Directory of tensorboard logs, '
                   'should contain \'events.out.tfevents\' files.',
              show_default=True)
@click.option('-n', '--name', 'name', type=str, default=None,
              help='Name of the log directory on space. '
                   'Directory name will be used when not given',
              show_default=True)
@click.option('-A', '--anonymous', 'anonymous', is_flag=True, type=bool, default=False,
              help='Hide the local machine\'s name when uploading.', show_default=True)
def sync(repository: str, logdir, name: Optional[str] = None, anonymous: bool = False):
    logging.try_init_root(logging.INFO)
    upload_log_directory(repository, logdir, name, anonymous)
