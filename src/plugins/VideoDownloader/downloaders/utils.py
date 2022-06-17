import subprocess
import re

import requests
from tqdm import tqdm


def merge_audio_video(audio: str, video: str, output: str):
    cmd = f'ffmpeg -i "{audio}" -i "{video}" -c:v copy -c:a aac -strict experimental "{output}"'
    subprocess.run(cmd, shell=True)
    
    
def download_media(url: str, headers: dict, output: str, chunk_size = 2048):
    with requests.get(url, headers=headers, stream=True) as response:
        length = int(response.headers['content-length'])
        with open(output, 'wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=chunk_size), total=(length+chunk_size-1)//chunk_size):
                if chunk:
                    f.write(chunk)
                
                
def removeSubStr(text: str, *subs) -> str:
    rets = text
    for sub in subs:
        rets = re.sub(sub, '', rets)
    return rets