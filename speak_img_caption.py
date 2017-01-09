# coding: utf-8
import time
import os
import requests
import wave
import pygame
import time
import cv2
from scorer_sdk.Scorer import Scorer
import xml.etree.ElementTree as ET

# Create SCORER SDK object
scorer=Scorer("Task")

# Note: The way to get api key:
# Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions
# Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0
# Here you have to paste your primary key
CV_KEY = ""
TRANSLATOR_KEY = ""

# Set file paths
WAV_FILE = "./tmp.wav"
IMG_FILE = "./image.jpg"
DIC_FILE = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
VOICE_FILE = "/usr/share/hts-voice/mei/mei_normal.htsvoice"


def save_camera_image(img_file_path):
    scorer.poll()
    frame = scorer.get_frame()
    bgr = frame.get_bgr()
    cv2.imwrite(img_file_path, bgr)


def caption_stored_image(img_file_path):
    _url =　"https://api.projectoxford.ai/vision/v1.0/analyze/"
    json = None
    data = open(img_file_path, "rb").read()
    headers = dict()
    headers["Ocp-Apim-Subscription-Key"] = CV_KEY
    headers["Content-Type"] = "application/octet-stream"
    params = { "visualFeatures" : "Description"}

    try: 
        response = requests.request("POST", _url, json=json, data=data, headers=headers, params=params)
        result = response.json()
        return result
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def get_access_token(access_key):
    access_token_url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {"Ocp-Apim-Subscription-Key": access_key}
    res = requests.request("POST", access_token_url, headers=headers)
    return res.text


def get_translation(caption, access_token):
    headers = {"Accept": "application/xml",
               "Authorization": "Bearer " + access_token}
    params = {"from": "en-us", "to": "ja-jp",
              "maxTranslations":1000,
              "text": caption}
    translator_url = "https://api.microsofttranslator.com/v2/http.svc/GetTranslations"
    res = requests.request("POST", translator_url, headers=headers, params=params)
    return extract_transleted_text(res.text)


def extract_transleted_text(xml_string):
    parsed = ET.fromstring(xml_string)
    return parsed[1][0][4].text


def create_audio_file(caption, voice_file, dic_file, wav_file):
    os.system("echo "%s" | open_jtalk -m %s -x %s -ow %s" % (caption, voice_file, dic_file, wav_file))


def play_audio(wav_file_path):
    audio_info = get_audio_info(wav_file_path)
    pygame.mixer.init(frequency=audio_info["frame_rate"])
    pygame.mixer.music.load(wav_file_path)
    pygame.mixer.music.play(1)
    time.sleep(audio_info["time"])   
    pygame.mixer.music.stop()  


def get_audio_info(wav_file_path):
    wf = wave.open(wav_file_path , "r")
    audio_info = dict()
    audio_info["frame_rate"] = wf.getframerate()
    audio_info["frame_num"] =  wf.getframerate()
    audio_info["time"] = float(wf.getnframes()) / wf.getframerate()
    return audio_info


def main():
    print("Save camera image")
    save_camera_image(IMG_FILE)

    print("Caption the image")
    caption = caption_stored_image(IMG_FILE)
    print("Caption: " + caption)

    print ("Connect to server to get the access token")
    access_token = get_access_token(TRANSLATOR_KEY)
    print ("Access Token: " + access_token)

    print ("Translate the caption from English to Japanese")
    transleted_caption = get_translation(caption, access_token)
    print("Translated text: " + transleted_caption)

    print ("Create audio file")
    create_audio_file(transleted_caption, VOICE_FILE, DIC_FILE, WAV_FILE)

    print("Play caption audio")
    play_audio("blank.wav")
    play_audio(WAV_FILE)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)
