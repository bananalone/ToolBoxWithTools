import subprocess
import re

import requests
from tqdm import tqdm


def merge_audio_video(audio: str, video: str, output: str):
    cmd = f'ffmpeg -i "{audio}" -i "{video}" "{output}"'
    subprocess.run(cmd, shell=True)
    
    
def download_media(url: str, headers: dict, output: str, chunk_size = 2048):
    response = requests.get(url, headers=headers, stream=True)
    with open(output, 'wb') as f:
        for chunk in tqdm(response.iter_content(chunk_size=chunk_size)):
            if chunk:
                f.write(chunk)
                
                
def removeSubStr(text: str, *subs) -> str:
    rets = text
    for sub in subs:
        rets = re.sub(sub, '', rets)
    return rets