#!../venv/bin/python 
# -*- coding: utf-8 -*- 

import snowboydecoder
import sys
import signal
import speech_recognition as sr
import os
import time
import subprocess
from pixels import Pixels
# import apa102
from enum import Enum
import argparse
from gtts import gTTS
import ss_request
import device
import action

ss = ss_request.ss_request('0926825012', '123456789')

import requests
from xml.etree import ElementTree

# This code is required for Python 2.7
try: input = raw_input
except NameError: pass

subscription_key = '4252f4a4b5d447ffbd035d951e3f413f'

class TextToSpeech(object):
    def __init__(self, subscription_key, text):
        self.subscription_key = subscription_key
        self.tts = text
#input("What would you like to convert to speech: ")
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'vi-vn')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'vi-VN')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (vi-VN, AN)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open('out-tts.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

interrupted = False

class Player(Enum):
    Snowp = 1
    APlay = 2
    Mocp = 3
    NoPlay = 4

list_device = []
list_device.append(device.device(1, [u'đèn phòng khách'], '11E9367B8CC09C6EAFAB0050560121C8', 1, action.action.ON_OFF))
list_device.append(device.device(1, [u'đèn nhà bếp', u'đèn phòng bếp', u'đèn nhà ăn'], '11E9367B8CC09C6EAFAB0050560121C8', 2, action.action.ON_OFF))
list_device.append(device.device(1, [u'đèn phòng ngủ'], '11E9367B8CC09C6EAFAB0050560121C8', 3, action.action.ON_OFF))
list_device.append(device.device(3, [u'tất cả đèn', u'tắt cả đèn'], ['11E9367B8CC09C6EAFAB0050560121C8', '11E9367B8CC09C6EAFAB0050560121C8', '11E9367B8CC09C6EAFAB0050560121C8'], [1, 2, 3], action.action.ON_OFF))

# class voice_command:
#     def __init__(self, cmd, response, accept_error, device_id, num_pad, status):
#         self.cmd = cmd
#         self.response = response
#         self.accept_error = accept_error
#         self.device_id = device_id
#         self.num_pad = num_pad
#         self.status = status

# list_command = []
# list_command.append(voice_command(u'bật đèn nhà bếp', u'đèn nhà bếp đã bật', 0, '11E9367B8CC09C6EAFAB0050560121C8', 1, 1))
# list_command.append(voice_command(u'tắt đèn nhà bếp', u'đèn nhà bếp đã tắt', 0, '11E9367B8CC09C6EAFAB0050560121C8', 1, 0))
# list_command.append(voice_command(u'bật đèn phòng khách', u'đèn phòng khách đã bật', 0, '11E9367B8CC09C6EAFAB0050560121C8', 2, 1))
# list_command.append(voice_command(u'tắt đèn phòng khách', u'đèn phòng khách đã tắt', 0, '11E9367B8CC09C6EAFAB0050560121C8', 2, 0))
# list_command.append(voice_command(u'bật đèn phòng ngủ', u'đèn phòng ngủ đã bật', 0, '11E9367B8CC09C6EAFAB0050560121C8', 3, 1))
# list_command.append(voice_command(u'tắt đèn phòng ngủ', u'đèn phòng ngủ đã tắt', 0, '11E9367B8CC09C6EAFAB0050560121C8', 3, 0))
# list_command.append(voice_command(u'bật tất cả đèn', u'tất cả đèn đã bật', 1, ['11E9367B8CC09C6EAFAB0050560121C8', '11E9367B8CC09C6EAFAB0050560121C8', '11E9367B8CC09C6EAFAB0050560121C8'], [1, 2, 3], [1, 1, 1]))
# list_command.append(voice_command(u'tắt tất cả đèn', u'tất cả đèn đã tắt', 1, ['11E9367B8CC09C6EAFAB0050560121C8', '11E9367B8CC09C6EAFAB0050560121C8', '11E9367B8CC09C6EAFAB0050560121C8'], [1, 2, 3], [0, 0, 0]))

SnowboyModel = '../Python3/resources/models/snowboy.umdl'   ### PROBABLY DIFFERENT on other systems ###
lang = 'vi-VN'                         
player = Player.Snowp
sleepTime = 0.01
silentCountThreshold = 5
recordingTimeout = 100
detectedSignal = 3

def voice_response(text_response):
    print('voice response: ' + text_response.encode('utf8'))
    app = TextToSpeech(subscription_key, text_response)
    app.get_token()
    app.save_audio()
    pixels.speak()
    os.system('aplay out-tts.wav')

def audioRecorderCallback(fname):
    pixels.think()
    print("converting audio to text")
    r = sr.Recognizer()
    with sr.AudioFile(fname) as source:
        audio = r.record(source)  # read the entire audio file
    # recognize speech using Google Speech Recognition
    check_error = False
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio, language=lang)
        print(result.encode('utf-8'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        check_error = True
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        check_error = True

    if player != Player.NoPlay:
        print('Playing recorded message in file "{}" with ')
        if player == Player.Mocp:
           print('mocp')
           subprocess.run(["mocp", "-l", fname], shell=False, check=True)        
        elif player == Player.APlay:
           print('aplay')
           subprocess.run(["aplay", "-c", "1", "-f", "S16_LE", "-r", "16000", fname], shell=True, check=True)
        else:
        #    print('snowboydecoder.play_audio_file()')
        #    snowboydecoder.play_audio_file(fname)
            if check_error != True:
                result = result.lower()
                for dev in list_device:
                    for dev_name in dev.name:
                        if dev_name in result:
                            if dev.action_type == action.action.ON_OFF:
                                if result.find(action.on_off.on) != -1:
                                    if dev.n_element == 1:
                                        ss.switcher_control(dev.id, dev.num_pad, 1)
                                    else:
                                        for e_index in range(len(dev.id)):
                                            ss.switcher_control(dev.id[e_index], dev.num_pad[e_index], 1)
                                    voice_response(dev_name + u' đã ' + action.on_off.on)
                                elif result.find(action.on_off.off) != -1:
                                    if dev.n_element == 1:
                                        ss.switcher_control(dev.id, dev.num_pad, 0)
                                    else:
                                        for e_index in range(len(dev.id)):
                                            ss.switcher_control(dev.id[e_index], dev.num_pad[e_index], 0)
                                    voice_response(dev_name + u' đã ' + action.on_off.off)


                # for i in range(n_command):
                #     if len(list_command[i].cmd) != len(result.lower()):
                #         continue
                #     counter = 0
                #     result = result.lower()
                #     for c in range(len(list_command[i].cmd)):
                #         if list_command[i].cmd[c] != result[c]:
                #             counter += 1
                #     print('counter: ' + str(counter))   
                #     if counter <= list_command[i].accept_error:
                #         # func_exec[i]()
                #         # ap.show()
                #         if type(list_command[i].device_id) != str and len(list_command[i].device_id) > 1:
                #             for c in range(len(list_command[i].device_id)):
                #                 ss.switcher_control(list_command[i].device_id[c], list_command[i].num_pad[c], list_command[i].status[c])
                #         else:
                #             ss.switcher_control(list_command[i].device_id, list_command[i].num_pad, list_command[i].status)
                #         app = TextToSpeech(subscription_key, list_command[i].response)
                #         app.get_token()
                #         app.save_audio()
                #         pixels.speak()
                #         os.system('aplay out-tts.wav')
                        # print(voice_cmd[i].encode('utf8'))
                        # tts = gTTS(respond_text[i], lang='vi')
                        # tts.save("out-tts.mp3")
                        # os.system('mpg123 out-tts.mp3') 
    
    os.remove(fname)
    os.system('aplay resources/dong.wav')
    pixels.off()
    print('\nListening... Press Ctrl+C to exit')


def detectedCallback():
  if detectedSignal > 2:
      snowboydecoder.play_audio_file()
  if detectedSignal > 1:
      pixels.listen()
  if detectedSignal > 0:    
      print('yes...')

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

players = ['snowp', 'aplay', 'mocp', 'none']
parser = argparse.ArgumentParser(description='demo5.py', usage=
  './%(prog)s [-l <LANG>] [-m <MODEL>] [-p {splay, aplay}] [-s <SLEEP>] [-c <COUNT>] [-r <TIMEOUT>] [-d {0,1,2,3}]')
parser.add_argument('-l', '--lang', type=str,  help="Spoken language (default 'en-US')")
parser.add_argument('-m', '--model', type=str, help='Snowboy hotword model file')
parser.add_argument('-p', '--player', type=str.lower, choices=players, help=
  "Player of recorded command, 'snowp' for snowboydecoder.play_audio_file, 'aplay' for ALSA aplay, 'mocp' for Music On Console player and 'none' for none")
parser.add_argument('-s', '--sleep', type=float, help='sleep_time (default 0.01)')
parser.add_argument('-c', '--count', type=int, help='silent_count_threshold (default 15)')
parser.add_argument('-r', '--record', type=int, help='recording_timeout (default 100)')
parser.add_argument('-d', '--detected', type=int, help='Detected signal: 0 - none, >0 - print yes, >1 - add pixels, >2 - add ding') 

args = parser.parse_args()

if args.model:
    SnowboyModel = args.model

if args.lang:
    lang = args.lang

if args.player:
    if args.player == 'none':
        player = Player.NoPlay
    elif args.player == 'aplay':
        player = Player.APlay
    elif args.player == 'mocp':
        player = Player.Mocp

if args.sleep:
    sleepTime = args.sleep

if args.count:
    silentCountThreshold = args.count
    
if args.record:
    recordingTimeout = args.record
    
if args.detected != None:
    detectedSignal = args.detected

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

pixels = Pixels()
detector = snowboydecoder.HotwordDetector(SnowboyModel, sensitivity=0.38)

print('Snowboy model file: ', SnowboyModel)
print('Spoken language: ', lang)

if args.player == Player.NoPlay:
    print('Do not play recorded command')
else:
    print('Play recorded command with ')
    if player == Player.APlay:
        print('aplay')
    elif player == Player.Mocp:
        print('mocp')
    else:     
        print('snowboydecoder.play_audio_file')

print('sleep_time:', sleepTime)
print('silent_count_threshold:', silentCountThreshold)
print('recording_timeout:', recordingTimeout)

signal = ''
if detectedSignal > 2:
    signal = '+ play ding'
if detectedSignal > 1:
    signal = '+ pixels ' + signal
if detectedSignal > 0:
    signal = 'print "yes" ' + signal
if detectedSignal < 1:
    signal = 'none'
print('hotword detected signal: ({}) '.format(detectedSignal), signal)

print('\nListening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=sleepTime,
               silent_count_threshold=silentCountThreshold,
               recording_timeout=recordingTimeout)

detector.terminate()
pixels.off()
time.sleep(1)


