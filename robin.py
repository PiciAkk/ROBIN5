#!/usr/bin/python3
import sys
import pip
import requests
import os
import json
import playsound
from gtts import gTTS
import speech_recognition as sr
from sys import stdin, stdout

class csomagkezelo:
    def importTelepites(self, importok):
        importokFajl = open("csomagok/importok.txt", "a+")
        for i in importok:
            importokFajl.write(i + "\n")
    def importTorles(self, torlendoImportok):
        mostaniImportok = open("csomagok/importok.txt", "r").read()
        importokFajl = open("csomagok/importok.txt", "w+")
        for i in torlendoImportok:
            mostaniImportok.replace(i, "")
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
        importok = (requests.get(f"{baseURL}/importok.txt").text).split()
        fuggosegek = (requests.get(f"{baseURL}/fuggosegek.txt").text).split()
        self.fuggosegTelepites(fuggosegek)
        self.importTelepites(importok)
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
        importok = (requests.get(f"{baseURL}/importok.txt").text).split()
        self.importTorles(importok)
    def parameterTeszt(self, args):
        if len(args) < 3:
            raise Exception("Csomagnév nincs specifikálva!")
        elif len(args) > 3:
            raise Exception("Túl sok paraméter")
class ROBIN:
    def hangFelismeres(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            os.system("clear")
            stdout.write("\nMondj valamit: ")
            audio = r.listen(source)
            try:
                parancs = r.recognize_google(audio, language="hu-HU")
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
    def importokBetoltese(self):
        importok = open("csomagok/importok.txt", "r").read().split("\n")
        for i in importok:
            if i != "":
                print(i)
                try:
                    __import__(i)
                except ImportError:
                    raise Exception("Nem található a modul: " + i)
    def csomagokBetoltese(self):
        modulok = os.listdir("./csomagok")
        for modul in modulok:
            exec(open(f"csomagok/{modul}", "r").read())
    def __init__(self):
        self.parancs = self.hangFelismeres()
        self.importokBetoltese()
        self.csomagokBetoltese()
        # idáig csak akkor megy el a program, ha semelyik modul sem lépteti ki a programot
        self.beszed("Parancs nem található!")

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
