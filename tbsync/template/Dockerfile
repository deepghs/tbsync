FROM python:${tbsync_python_version}

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$$PATH

WORKDIR $$HOME/app

COPY --chown=user . $$HOME/app

EXPOSE     ${tbsync_port}
ENTRYPOINT []
CMD        ["tensorboard", "--logdir", "runs", "--bind_all", "--port", "${tbsync_port}"]
