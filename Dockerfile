FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python-is-python3 \
    python3-django \
    python3-django-cors-headers \
    python3-pandas \
    python3-whitenoise \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY ./backend /app/backend
COPY ./frontend/dist /app/frontend/dist

WORKDIR /app/backend

RUN mkdir -p staticfiles temp_csv_files

RUN apt-get update && apt install -y \
    libjs-jquery \
    python3-waitress \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "csvtool_backend.wsgi:application"]
