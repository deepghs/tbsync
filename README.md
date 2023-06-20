# tbsync

[![PyPI](https://img.shields.io/pypi/v/tbsync)](https://pypi.org/project/tbsync/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tbsync)
![Loc](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/narugo1992/69c61702892a7c14b2aa26f6c676a220/raw/loc.json)
![Comments](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/narugo1992/69c61702892a7c14b2aa26f6c676a220/raw/comments.json)

[![Code Test](https://github.com/deepghs/tbsync/workflows/Code%20Test/badge.svg)](https://github.com/deepghs/tbsync/actions?query=workflow%3A%22Code+Test%22)
[![Package Release](https://github.com/deepghs/tbsync/workflows/Package%20Release/badge.svg)](https://github.com/deepghs/tbsync/actions?query=workflow%3A%22Package+Release%22)
[![codecov](https://codecov.io/gh/deepghs/tbsync/branch/main/graph/badge.svg?token=XJVDP4EFAT)](https://codecov.io/gh/deepghs/tbsync)

![GitHub Org's stars](https://img.shields.io/github/stars/deepghs)
[![GitHub stars](https://img.shields.io/github/stars/deepghs/tbsync)](https://github.com/deepghs/tbsync/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/deepghs/tbsync)](https://github.com/deepghs/tbsync/network)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/deepghs/tbsync)
[![GitHub issues](https://img.shields.io/github/issues/deepghs/tbsync)](https://github.com/deepghs/tbsync/issues)
[![GitHub pulls](https://img.shields.io/github/issues-pr/deepghs/tbsync)](https://github.com/deepghs/tbsync/pulls)
[![Contributors](https://img.shields.io/github/contributors/deepghs/tbsync)](https://github.com/deepghs/tbsync/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/deepghs/tbsync)](https://github.com/deepghs/tbsync/blob/master/LICENSE)

Sync tools for tensorboard logs

Here is an [online demo](https://huggingface.co/spaces/narugo/tbsync_demo) of a space build with `tbsync`.

## Installation

You can simply install it with `pip` command line from the official PyPI site.

```shell
pip install tbsync
```

For more information about installation, you can refer
to [Installation](https://deepghs.github.io/tbsync/main/tutorials/installation/index.html).

## Quick Start

### Initialize Huggingface Space

Create a space repository on Hugging Face with the command below to start TensorBoard. Prior to this, you can log in
using `huggingface-cli` or authenticate by setting the `HF_TOKEN` environment variable.

```shell
tbsync init -r myuser/my_hf_space
```

More usage can be viewed with `tbsync init --help`

```text
Usage: tbsync init [OPTIONS]

  Initialize huggingface space repository.

Options:
  -r, --repository TEXT           Repository on huggingface.  [required]
  -t, --title TEXT                Title of the repository, capitalized
                                  repository name will be used if not given.
  -e, --emoji TEXT                Emoji to use for repository, see emoji
                                  library for details. Random emoji will be
                                  used when not given.
  -p, --private                   Create private repository.
  -l, --licence [openrail|bigscience-openrail-m|creativeml-openrail-m|bigscience-bloom-rail-1.0|bigcode-openrail-m|afl-3.0|apache-2.0|artistic-2.0|bsl-1.0|bsd|bsd-2-clause|bsd-3-clause|bsd-3-clause-clear|c-uda|cc|cc0-1.0|cc-by-2.0|cc-by-2.5|cc-by-3.0|cc-by-4.0|cc-by-sa-3.0|cc-by-sa-4.0|cc-by-nc-2.0|cc-by-nc-3.0|cc-by-nc-4.0|cc-by-nd-4.0|cc-by-nc-nd-3.0|cc-by-nc-nd-4.0|cc-by-nc-sa-2.0|cc-by-nc-sa-3.0|cc-by-nc-sa-4.0|cdla-sharing-1.0|cdla-permissive-1.0|cdla-permissive-2.0|wtfpl|ecl-2.0|epl-1.0|epl-2.0|eupl-1.1|agpl-3.0|gfdl|gpl|gpl-2.0|gpl-3.0|lgpl|lgpl-2.1|lgpl-3.0|isc|lppl-1.3c|ms-pl|mit|mpl-2.0|odc-by|odbl|openrail++|osl-3.0|postgresql|ofl-1.1|tii-falcon-llm|ncsa|unlicense|zlib|pddl|lgpl-lr|deepfloyd-if-license|unknown|other]
                                  Licence for repository.  [default: mit]
  --port INTEGER                  Port of tensorboard in space.  [default:
                                  6006]
  -P, --python_version TEXT       Version of python to use.  [default: 3.8.1]
  -T, --tensorboard_version TEXT  Version of tensorboard to use.
  --from_color [red|yellow|green|blue|indigo|purple|pink|gray]
                                  From color of space block. Random color will
                                  be used when not given.
  --to_color [red|yellow|green|blue|indigo|purple|pink|gray]
                                  To color of space block. Random color will
                                  be used when not given.
  -h, --help                      Show this message and exit.
```

### Upload Tensorboard Log To Space

Upload the `tfevents` files from the local TensorBoard log path to the Hugging Face space repository using the command
below. Prior to this, initialize with the `sync init` command.

```shell
tbsync upload -r myuser/my_hf_space -d /path/to/tb/log

```

After the upload is complete, Hugging Face space will be rebuilt. Once the rebuild is finished, the TensorBoard log can
be viewed in the space.

More usage can be viewed with `tbsync sync --help`

```text
Usage: tbsync sync [OPTIONS]

  Upload log file to huggingface space repository.

Options:
  -r, --repository TEXT      Repository on huggingface.  [required]
  -d, --directory DIRECTORY  Directory of tensorboard logs, should contain
                             'events.out.tfevents' files.  [required]
  -n, --name TEXT            Name of the log directory on space. Directory
                             name will be used when not given
  -A, --anonymous            Hide the local machine's name when uploading.
  -h, --help                 Show this message and exit.
```

