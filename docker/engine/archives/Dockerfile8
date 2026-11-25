FROM python:trixie

ENV FLASK_APP=events_app \
    FLASK_DEBUG=True \
    RUNTIME_MODE=dev

RUN groupadd -g 1000 app \
    && useradd -d /app -u 1000 -g app -s /bin/bash app

WORKDIR /app

COPY flask/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY flask .

COPY docker/engine/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

RUN chown -R app:app /app

USER app
EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]

#CMD ["tail", "-f", "/dev/null"]
