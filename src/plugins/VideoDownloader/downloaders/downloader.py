import os
import re
import uuid

from . import utils

class Downloader:
    NAME = 'name'
    VIDEO_URL = 'video_url'
    AUDIO_URL = 'audio_url'
    
    def __init__(self) -> None:
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
        }
    
    def parse(self, url: str) -> dict:
        raise NotImplementedError
    
    def download(self, url: str, output: str = None):
        video_info = self.parse(url)
        output = output if output else os.path.join('./', video_info[Downloader.NAME] + '.mp4')
        id = uuid.uuid1()
        v_path = os.path.join('./', 'v-' + str(id))
        a_path = os.path.join('./', 'a-' + str(id))
        print('Downloading video ... ')
        utils.download_media(video_info[Downloader.VIDEO_URL], headers=self.headers, output=v_path)
        print('Downloading audio ... ')
        utils.download_media(video_info[Downloader.AUDIO_URL], headers=self.headers, output=a_path)
        utils.merge_audio_video(a_path, v_path, output=output)
        os.remove(v_path)
        os.remove(a_path)


class Factory:
    def __init__(self) -> None:
        self.downloaders = {}
    
    def register(self, *patterns):
        def inner(cls: Downloader):
            for pattern in patterns:
                if pattern in self.downloaders:
                    raise Exception(f"{pattern} has already been registered")
                self.downloaders[pattern] = cls()
            return cls
        return inner
    
    def downloader(self, url: str) -> Downloader:
        for pattern in self.downloaders:
            if re.match(pattern, url):
                return self.downloaders[pattern]
            
    def download(self, url: str):
        self.downloader(url).download(url)


factory = Factory()