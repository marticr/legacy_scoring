FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for Qt
RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1-mesa-glx \
    libegl1-mesa \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libglib2.0-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxcb-cursor0 \
    libxcb-util1 \
    '^libxcb.*-dev' \
    libx11-xcb-dev \
    libglu1-mesa-dev \
    libxrender-dev \
    libxi-dev \
    libxkbcommon-dev \
    libxkbcommon-x11-0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV QT_QPA_PLATFORM=xcb
ENV DISPLAY=:99
ENV QT_DEBUG_PLUGINS=1

# Create startup script
RUN echo '#!/bin/bash\n\
    Xvfb :99 -screen 0 1024x768x16 &\n\
    sleep 1\n\
    python src/main.py' > /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8080

CMD ["/app/start.sh"]