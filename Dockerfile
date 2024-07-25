ARG BUILD_FROM
FROM $BUILD_FROM

# Install basic dependencies and build tools
RUN apk add --no-cache ffmpeg python3 py3-pip build-base musl-dev gcc libsndfile-dev pkgconfig python3-dev

# Create a virtual environment
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade pip

# Install Python packages separately to identify issues
RUN /venv/bin/pip install --upgrade paho-mqtt
RUN /venv/bin/pip install --upgrade PyYAML
RUN /venv/bin/pip install --upgrade librosa
RUN /venv/bin/pip install --upgrade soundfile

# Copy data for add-on
COPY run.sh /
COPY get_mfcc.py /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

