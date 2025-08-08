# from maad import sound, util
import os
from pathlib import Path
import json

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
        with open(voicebank_path / "Resources" / "Desc" / "Desc.json") as f:
        data = json.load(f)
        print(f"Using voicebank: {data["Title"]}")
        ready = True
    