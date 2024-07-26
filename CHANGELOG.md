# Changelog

## 1.2.5
- fixed python errors

## 1.2.4
- fixed build issues, but it still takes a few min so be patient on the install

## 1.2.3
- not finding python:3.12-slim-buster as base, trying python:3.12-slim

## 1.2.2
- fix build issue

## 1.2.1
- go to a multi-stage docker build to deal with the oh so many dependencies of librosa

## 1.2.0
- try again to use Librosa

## 1.1.8
- another typo error in py script

## 1.1.7
- typo error in py script

## 1.1.6
- switch to ShortTermFeatures in pyAudioAnalysis

## 1.1.5
- another missing import

## 1.1.4
- another attempt at getting build to complete

## 1.1.3
- fix get_mfcc.py imports for pyAudioAnalysis

## 1.1.2
- fix build issues by switching to python:3.11-slim as the base image (rather than HA base image)

## 1.1.1
- attempt to build PyAudioAnalysis

## 1.1.0
- abandon Librosa due to overly complex dependencies. Switch to PyAudioAnalysis

## 1.0.a
- new Dockerfile to debug install errors

## 1.0.9
- mod get_mfcc.py to fix reporting

## 1.0.8
- mod Dockerfile to address librosa dependencies issues

## 1.0.7
- mod Dockerfile to add some missing librosa dependencies

## 1.0.6
- mod Dockerfile to fix python lib issue (librosa)

## 1.0.5
- try again to fix python lib issue (librosa)

## 1.0.4
- fix python lib issue (librosa)

## 1.0.3
- fix python mqtt connect errors

## 1.0.2
- initial python script to extract mfcc's

## 1.0.1
- using 1.f.x as the initial setup dev, then will switch to 1.1.x when something is actually running.

## 1.0.1
- basic running add-on
