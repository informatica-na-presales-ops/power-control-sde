FROM python:3.11.0b3-alpine3.15

RUN /usr/sbin/adduser -g python -D python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

COPY --chown=python:python requirements.txt /home/python/power-control-sde/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/power-control-sde/requirements.txt

ENV PATH="/home/python/venv/bin:${PATH}" \
    PYTHONUNBUFFERED="1" \
    TZ="America/Los_Angeles"

LABEL org.opencontainers.image.authors="William Jackson <wjackson@informatica.com>" \
      org.opencontainers.image.source="https://github.com/informatica-na-presales-ops/power-control-sde"

COPY --chown=python:python power-control-sde.py /home/python/power-control-sde/power-control-sde.py

ENTRYPOINT ["/home/python/venv/bin/python", "/home/python/power-control-sde/power-control-sde.py"]
