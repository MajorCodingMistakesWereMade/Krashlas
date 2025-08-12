import os
from pathlib import Path
import json
from threading import Thread
from maad import sound, util

global voicebank
global ready
global voicebank_path

freq = 48000

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
    
voicebankSamples = {}

for dirpath, dirnames, filenames in os.walk(voicebank_path / "Resources" / "Sounds"):
    for filename in filenames:
        if filename.endswith(".wav"):
            file_path = Path(dirpath) / filename
            sObj = sound.load(str(file_path))
            name = filename.replace(".wav", "")
            voicebankSamples[name] = sObj
    
    

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
        if position == 0 and f"{letter}_Start" in voicebankSamples:
            sounds.append(voicebankSamples[f"{letter}_Start"])
        if f"{letter}_Mid" in voicebankSamples:
            sounds.append(voicebankSamples[f"{letter}_Mid"])
        if position == len(myObj["Sound"]) - 1 and f"{letter}_End" in voicebankSamples:
            sounds.append(voicebankSamples[f"{letter}_End"])
    print(sounds)
    fullSoundDataList.append(sounds)
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
    
soundOutput = []
for currentSound in fullSoundDataList:
    soundOutput.append(util.crossfade_list(currentSound, freq, fade_len=.25))
outputSound = util.crossfade_list(soundOutput, freq, fade_len=.1)
output_filename = f"{song} ft. {data['Title']}.mp3"
sound.write(output_filename, freq, outputSound, format="mp3", codec="libmp3lame", bitrate=320)
print(f"Song saved as {output_filename} in the current directory.")