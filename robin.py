#!/usr/bin/python3
import sys
import pip
import subprocess
import requests
import os
import json
import playsound
from gtts import gTTS
import speech_recognition as sr
import time
import sounddevice as sd
import soundfile
from scipy.io.wavfile import write
from sys import stdin, stdout
from hunspell import Hunspell
from googletrans import Translator

class pip:
    def parancsFuttatas(self, parancs, csomag):
        folyamat = subprocess.Popen([sys.executable, '-m', 'pip', parancs, csomag], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = folyamat.communicate()
        exit_code = folyamat.wait()
        class returnableClass:
            pass
        returnable = returnableClass()
        returnable.exitcode = int(exit_code)
        returnable.stdout = stdout
        returnable.stderr = stderr
        return returnable
    def telepites(self, csomag):
        returnable = self.parancsFuttatas('install', csomag)
        return returnable
    def eltavolitas(self, csomag):
        returnable = self.parancsFuttatas('uninstall', csomag)
        return returnable
class csomagkezelo:
    def csomagokFrissitese(self, csomagok):
        frissitettCsomagok = 0
        for csomag in csomagok:
            baseURL = f"https://raw.githubusercontent.com/PiciAkk/ROBIN5-Csomagok/main/{csomag}"
            serverContent = requests.get(f"{baseURL}/modul.py").text
            try:
                localContent = open(f"csomagok/{csomag}.py", "r").read()
            except:
                raise Exception(f"{csomag} nincs telepítve, így nem lehet frissíteni!")
            if (serverContent != localContent):
                print(f"{csomag} frissítésre szorul!")
                self.telepites(csomag)
                frissitettCsomagok += 1
        if frissitettCsomagok == 0:
            print("Egy csomag sem szorult frissítésre")
        else:
            print(f"-----\n{frissitettCsomagok} csomag sikeresen frissítve")  
    def frissites(self):
        self.csomagokFrissitese(list(self.listazas()))
        # kilistázzuk a csomagokat, majd frissítjük azokat
    def listazas(self):
        modulok = os.listdir("csomagok")
        for modul in modulok:
            yield os.path.splitext(modul)[0]
    def fuggosegTelepites(self, fuggosegek):
        for csomagnev in fuggosegek:
            telepites = pip().telepites(csomagnev)
            if telepites.exitcode != 0:
                raise Exception(telepites.stderr)
            else:
                print(f"Függőség ({csomagnev}) sikeresen telepítve")
    def fuggosegTorles(self, fuggosegek):
        for csomagnev in fuggosegek:
            eltavolitas = pip().eltavolitas(csomagnev)
            if eltavolitas.exitcode != 0:
                raise Exception(eltavolitas.stderr)
            else:
                print(f"Függőség ({csomagnev}) sikeresen eltávolítva!")
    def telepites(self, csomagnev):
        baseURL = f"https://raw.githubusercontent.com/PiciAkk/ROBIN5-Csomagok/main/{csomagnev}"
        serverContent = requests.get(f"{baseURL}/modul.py").text
        if serverContent == "404: Not Found":
            raise Exception(f"A csomag ({csomagnev}) nem található!")
        modulFajl = open(f"csomagok/{csomagnev}.py", "w+")
        modulFajl.write(serverContent)
        modulFajl.close()
        fuggosegek = (requests.get(f"{baseURL}/fuggosegek.txt").text).split()
        self.fuggosegTelepites(fuggosegek)
        print("Csomag sikeresen telepítve")
    def torles(self, csomagnev):
        baseURL = f"https://raw.githubusercontent.com/PiciAkk/ROBIN5-Csomagok/main/{csomagnev}"
        fuggosegek = (requests.get(f"{baseURL}/fuggosegek.txt").text).split()
        try:
            os.remove(f"csomagok/{csomagnev}.py")
        except:
            raise Exception(f"A csomag ({csomagnev}) nincs telepítve!")
        fuggosegekTorleseIs = input("Le szeretnéd törölni a csomag függőségeit is? (Y/n) ").lower()
        if fuggosegekTorleseIs == "y":
            self.fuggosegTorles(fuggosegek)
        elif fuggosegekTorleseIs == "n":
            pass
        else:
            raise Exception(f"A válasz {fuggosegekTorleseIs} nem megfelelő")
        print("Csomag sikeresen törölve!")
class ROBIN:
    def hangFelismeres(self, prompt="Mondj valamit: "):
        # rakjunk egy newline karaktert a prompt elejére
        prompt = "\n" + prompt
        # cleareljük a konzolt
        print("\033[H\033[J", end="")

        # vegyük fel a hangot
        frekvencia = 44100
        hossz = 5
        felvetel = sd.rec(int(hossz * frekvencia), samplerate=frekvencia, channels=2)
        stdout.write(prompt)
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
        self.h = Hunspell(f"hu_HU", hunspell_data_dir="magyarispell") # inicializáljuk a hunspell-t
        os.remove("hang.wav") # töröljük a (már elemzett) hangfájlt
        self.csomagokBetoltese()
        # idáig csak akkor megy el a program, ha semelyik modul sem lépteti ki
        self.beszed("A parancs nem található!")

def main():
    csomagok = csomagkezelo()
    args = sys.argv
    def parameterTeszt(args):
        if len(args) < 3:
            raise Exception("Csomagnév nincs specifikálva!")
        elif len(args) > 3:
            raise Exception("Túl sok paraméter")
                
    if len(args) == 1:
        ROBIN()
        quit() # kilépünk, ha valahogy nem lépett még ki ROBIN
    elif args[1] == "telepites":
        parameterTeszt(args)
        csomagok.telepites(args[2])
    elif args[1] == "torles":
        parameterTeszt(args)
        csomagok.torles(args[2])
    elif args[1] == "csomagok":
        print('\n'.join(list(csomagok.listazas())))
        # kilistázzuk a csomagokat, külön sorokba tördeljük, majd kiíratjuk
    elif args[1] == "frissites":
        if len(args) == 3:
            csomagok.csomagokFrissitese([args[2]])
        else:
            csomagok.frissites()
    else:
        raise Exception("Parancs nem található!")

if __name__ == "__main__":
    main()
