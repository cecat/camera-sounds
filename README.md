# Camera-sounds add-on for Home Assistant
CeC
July 2024

# This is under development - not even a beta yet 

##nothing to see here...

---


Analyze sound characteristics from microphones on remote cameras 
to detect sound types (conversations, music, lawnmower). The add-on
does not keep recordings nor can it detect what is being said - it is
only using a python library (librosa) to extract MFCCs
(Mel-frequency cepstral coefficients), which are numerical
characteristics useful for classifying sound type.
This add-on has only been tested on Amcrest
cameras so it's far from proven.

This is an experimental add-on, not yet working!

## Add the add-on's repo  to your Home Assistant

[![Open your Home Assistant instance and show the add-on store.](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)

Add this repo:
```
https://github.com/cecat/CeC-HA-Addons.git
```

## To Configure this Addon

0. This addon assumes you are running a MQTT broker already. This code
has (only) been tested with the open source
[Mosquitto broker](https://github.com/home-assistant/addons/tree/master/mosquitto) 
from the *Official add-ons* repository.

1. Create a file, *cameravolume.yaml* with specifics regarding your MQTT broker address,
MQTT username and password, and RTSP feeds. These will be the same feeds you use
in Frigate (if you use Frigate), which may have embedded credentials
(so treat this as a secrets file). If you want to report less frequently than
every 60s you can change the *stats_interval* value in this file.  This configuration
file will look something like below. Put this file into */config*.

```
mqtt:
  host: "x.x.x.x"
  port: 1883
  topic_prefix: "HA/sensor"
  client_id: "camvolume"
  user: "mymqttusernameforcamvol"
  password: "mymqttpasswordforcamvol"
  stats_interval: 30
cameras:
  doorfrontcam:
    ffmpeg:
      inputs:
      - path: "rtsp://user:password@x.x.x.x:554/cam/realmonitor?channel=1&subtype=1"
  frontyardcam:
    ffmpeg:
      inputs:
      - path: "rtsp://user:password@x.x.x.x:554/cam/realmonitor?channel=1&subtype=1"
```



