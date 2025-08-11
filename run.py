# from maad import sound, util
import os
from pathlib import Path
import json
from threading import Thread

global voicebank
global ready
global voicebank_path

ready = False
while not ready:
    voicebank = input("What voicebank do you want to use?")
    script_path = Path(__file__)
    script_directory = script_path.parent
    voicebank_path = script_directory / "voicebanks" / voicebank
    if not voicebank_path.exists():
        print(f"Voicebank '{voicebank}' does not exist in the 'voicebanks' directory.")
    else:
        with open(voicebank_path / "Resources" / "Desc" / "Desc.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"Using voicebank: {data['Title']}")
            ready = True
    
song = input("What song do you want to use?")
SavedSongs = script_directory / "SavedSongs"
song_path = SavedSongs / f"{song}.json"

# A.start A.Mid B.Mid C.Mid C.End

fullSoundDataList = []

with open(song_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def soundCommand(myObj):
    sounds = []

    for position, letter in enumerate(myObj["Sound"]):
        if position == 0:
            sounds.append(f"{letter}_Start")
        sounds.append(f"{letter}_Mid")
        if position == len(myObj["Sound"]) - 1:
            sounds.append(f"{letter}_End")
    print(sounds)
    return sounds

def pitchCommand(myObj):
    for coord in myObj["Coordinates"]:
        print(coord["X"], coord["Y"], coord["CurveIntensity"])

for myObj in data["Song"]:
    sct = Thread(target=soundCommand, args=(myObj,))
    pct = Thread(target=pitchCommand, args=(myObj,))
    sct.start()
    pct.start()
    sct.join()
    pct.join()
    
            

