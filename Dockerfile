FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends\
    python3 \
    python3-django \
    python3-django-cors-headers \
    python3-pandas \
    python3-venv \
    python3-whitenoise \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @vue/cli

WORKDIR /app
COPY ./backend /app/backend
COPY ./frontend /app/frontend

EXPOSE 8000

CMD ["bash"]