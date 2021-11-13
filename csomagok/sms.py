import os
import json

def smsKuldes(telefonszam, uzenet):
    os.system(f"""kdeconnect-cli --send-sms "{uzenet}" --destination {telefonszam} --device e3d5c6a284a0e008""")
def telefonszamLekeres(kisbetusnev, kontaktok):
    for kontakt in kontaktok:
        if kontakt["name"].lower() == kisbetusnev:
            return kontakt["number"].replace(" ", "") 
beszed = self.beszed
parancs = self.parancs
h = self.h
hangFelismeres = self.hangFelismeres
kontaktok = json.loads(open("konfiguraciok/kontaktok.json", "r").read())

if "üzenet" in parancs.lower() or "küld" in parancs.lower() or "ír" in parancs.lower():
    if "küldj egy üzenetet" == parancs.lower():
        # nincs személynév specifikálva
        beszed("Kinek szeretnél üzenetet küldeni?")
        szemelynev = hangFelismeres(f"\nKinek szeretnél üzenetet küldeni? ")
    else:
        # van személynév specifikálva
        szemelynev = parancs.split()[-1]
    stemmedSzemelynev = h.stem(szemelynev)[0]
    telefonszam = telefonszamLekeres(stemmedSzemelynev, kontaktok)
    beszed(f"Mit küldjek el {szemelynev}?")
    uzenet = hangFelismeres(f"\nMit küldjek el {szemelynev}? ")
    smsKuldes(telefonszam, uzenet)
    beszed("Üzenet sikeresen elküldve...")
    quit()
