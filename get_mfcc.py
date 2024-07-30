import subprocess
import paho.mqtt.client as mqtt
import time
import yaml
import os
import librosa
import numpy as np
import io
import logging

# Set up detailed logging
logging.basicConfig(level=logging.INFO)  # Change to INFO to reduce verbosity
logger = logging.getLogger(__name__)

# Reduce Numba logging verbosity
numba_logger = logging.getLogger('numba')
numba_logger.setLevel(logging.WARNING)  # Change to WARNING to reduce verbosity

logger.info("Add-on Started.")

# Load user configuration from /config/camerasounds.yaml
config_path = '/config/camerasounds.yaml'
if not os.path.exists(config_path):
    logger.error(f"Configuration file {config_path} does not exist.")
    raise FileNotFoundError(f"Configuration file {config_path} does not exist.")

with open(config_path) as f:
    config = yaml.safe_load(f)

# Extract MQTT settings from user config
mqtt_settings = config.get('mqtt', {})
mqtt_host = mqtt_settings.get('host')
mqtt_port = mqtt_settings.get('port')
mqtt_topic_prefix = mqtt_settings.get('topic_prefix')
mqtt_client_id = mqtt_settings.get('client_id')
mqtt_username = mqtt_settings.get('user')
mqtt_password = mqtt_settings.get('password')
mqtt_stats_interval = mqtt_settings.get('stats_interval', 60)

# Log the MQTT settings being used
logger.info(f"MQTT settings: host={mqtt_host}, port={mqtt_port}, topic_prefix={mqtt_topic_prefix}, client_id={mqtt_client_id}, user={mqtt_username}\n")

# Extract camera settings from user config
camera_settings = config.get('cameras', {})

# MQTT connection setup
mqtt_client = mqtt.Client(client_id=mqtt_client_id, protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(mqtt_username, mqtt_password)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info("Connected to MQTT broker")
    else:
        logger.error("Failed to connect to MQTT broker")

mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(mqtt_host, mqtt_port, 60)
    mqtt_client.loop_start()
except Exception as e:
    logger.error(f"Failed to connect to MQTT broker: {e}")

# Function to extract MFCCs
def get_mfccs(rtsp_url, duration=10):
    command = [
        'ffmpeg',
        '-y',
        '-i', rtsp_url,
        '-t', str(duration),
        '-f', 'wav',
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '1',
        'pipe:1'
    ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        logger.error(f"FFmpeg error: {stderr.decode('utf-8')}")
        return None

    with io.BytesIO(stdout) as f:
        y, sr = librosa.load(f, sr=44100)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        return mfccs.mean(axis=1)

# Sample interval
sample_interval = 60  # Sample every 60 seconds

# Main Loop
while True:
    for camera_name, camera_config in camera_settings.items():
        rtsp_url = camera_config['ffmpeg']['inputs'][0]['path']
        mfccs = get_mfccs(rtsp_url, duration=10)

        if mfccs is not None:
            if mqtt_client.is_connected():
                try:
                    mfccs_str = ','.join(map(str, mfccs))
                    result = mqtt_client.publish(
                        f"{mqtt_topic_prefix}/{camera_name}_mfccs",
                        mfccs_str
                    )
                    result.wait_for_publish()

                    if result.rc == mqtt.MQTT_ERR_SUCCESS:
                        logger.info(f"Published MFCCs for {camera_name}: {mfccs_str}")
                    else:
                        logger.error(f"Failed to publish MQTT message for MFCCs, return code: {result.rc}")
                except Exception as e:
                    logger.error(f"Failed to publish MQTT message: {e}")
            else:
                logger.error("MQTT client is not connected. Skipping publish.")
        else:
            logger.error(f"Failed to extract MFCCs for {camera_name}")
    time.sleep(sample_interval)

