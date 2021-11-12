#!/usr/bin/python3
import sys
import pip
import requests
import os
import json
import playsound
from gtts import gTTS
import speech_recognition as sr
import sounddevice as sd
import soundfile
from scipy.io.wavfile import write
from sys import stdin, stdout

class csomagkezelo:
    def fuggosegTelepites(self, fuggosegek):
        for csomagnev in fuggosegek:
            if hasattr(pip, 'main'):
                pip.main(['install', csomagnev])
            else:
                pip._internal.main(['install', csomagnev])
    def fuggosegTorles(self, fuggosegek):
        for csomagnev in fuggosegek:
            if hasattr(pip, 'main'):
                pip.main(['uninstall', csomagnev])
            else:
                pip._internal.main(['uninstall', csomagnev])
    def telepites(self, csomagnev):
        baseURL = f"https://raw.githubusercontent.com/PiciAkk/ROBIN5-Csomagok/main/{csomagnev}"
        modulFajl = open(f"csomagok/{csomagnev}.py", "w+")
        modulFajl.write(requests.get(f"{baseURL}/modul.py").text)
        modulFajl.close()
        importok = (requests.get(f"{baseURL}/importok.py").text)
        fuggosegek = (requests.get(f"{baseURL}/fuggosegek.txt").text).split()
        self.fuggosegTelepites(fuggosegek)
        print("Csomag sikeresen telepítve")
    def torles(self, csomagnev):
        baseURL = f"https://raw.githubusercontent.com/PiciAkk/ROBIN5-Csomagok/main/{csomagnev}"
        fuggosegek = (requests.get(f"{baseURL}/fuggosegek.txt").text).split()
        try:
            os.remove(f"csomagok/{csomagnev}.py")
        except:
            raise Exception("Csomag nincs telepítve!")
        fuggosegekTorleseIs = input("Le szeretnéd törölni a csomag függőségeit is? (Y/n) ").lower()
        if fuggosegekTorleseIs == "y":
            self.fuggosegTorles(fuggosegek)
        elif fuggosegekTorleseIs == "n":
            pass
        else:
            raise Exception(f"A válasz {fuggosegekTorleseIs} nem megfelelő")
        print("Csomag sikeresen törölve!")
    def parameterTeszt(self, args):
        if len(args) < 3:
            raise Exception("Csomagnév nincs specifikálva!")
        elif len(args) > 3:
            raise Exception("Túl sok paraméter")
class ROBIN:
    def hangFelismeres(self):
        os.system("clear")

        # vegyük fel a hangot
        frekvencia = 44100
        hossz = 5
        felvetel = sd.rec(int(hossz * frekvencia), samplerate=frekvencia, channels=2)
        stdout.write("\nMondj valamit: ")
        sd.wait()  # várjuk a hangot
        write("hang.wav", frekvencia, felvetel)  # elmentjük a hangot

        # konvertáljuk a hangot PCM_16-ra
        adat, samplerate = soundfile.read("hang.wav")
        soundfile.write("hang.wav", adat, samplerate, subtype='PCM_16')

        # ismerjük fel a hang beszédét
        r = sr.Recognizer()
        with sr.AudioFile("hang.wav") as forras:
            hang = r.record(forras)
            try:
                parancs = r.recognize_google(hang, language="hu-HU")
                print(parancs)
                return parancs
            except:
                raise Exception("Nem sikerült a felismerés!")
    def beszed(self, szoveg):
        print(szoveg)
        tts = gTTS(szoveg, lang="hu")
        tts.save("beszed.mp3")
        playsound.playsound("beszed.mp3")
        os.remove("beszed.mp3")
    def csomagokBetoltese(self):
        modulok = os.listdir("./csomagok")
        for modul in modulok:
            exec(open(f"csomagok/{modul}", "r").read())
    def __init__(self):
        self.parancs = self.hangFelismeres()
        os.remove("hang.wav") # töröljük a (már elemzett) hangot
        self.csomagokBetoltese()
        # idáig csak akkor megy el a program, ha semelyik modul sem lépteti ki
        self.beszed("A parancs nem található!")

def main():
    csomagok = csomagkezelo()
    args = sys.argv
    if len(args) == 1:
        ROBIN()
        quit()
    elif args[1] == "telepites":
        csomagok.parameterTeszt(args)
        csomagok.telepites(args[2])
    elif args[1] == "torles":
        csomagok.parameterTeszt(args)
        csomagok.torles(args[2])

if __name__ == "__main__":
    main()
