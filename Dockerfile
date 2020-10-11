FROM python:3.8-alpine as base
FROM base as builder
WORKDIR /build
COPY requirements.txt .
RUN apk add --no-cache mariadb-dev mariadb-client build-base libressl-dev musl-dev libffi-dev && pip3 wheel -r requirements.txt

FROM base as prod
COPY --from=builder /build /wheels
RUN apk add --no-cache mariadb-client mariadb-dev && pip install -U pip \
    && pip install --no-cache-dir \
    -r /wheels/requirements.txt \
    -f /wheels \
    && rm -rf /wheels
WORKDIR /app
COPY . .
CMD ["python3", "bot.py"]