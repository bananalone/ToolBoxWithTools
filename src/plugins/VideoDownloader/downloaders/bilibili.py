import re
import requests

from .downloader import factory, Downloader
from . import utils


@factory.register(r'http(s)?://www.bilibili.com/video/.+')
class BiliBili(Downloader):
    def __init__(self) -> None:
        super().__init__()
        self.headers['referer'] = 'https://www.bilibili.com'
        
    def parse(self, url: str) -> dict:
        audio_url = ''
        response = requests.get(url, headers=self.headers)
        # print(response.text)
        name_pattern = re.compile(r'<title data-vue-meta="true">.*</title>')
        name = name_pattern.findall(response.text)[0]
        name = utils.removeSubStr(name, r'<title data-vue-meta="true">', r'_哔哩哔哩_bilibili</title>')
        video_url_pattern = re.compile(r'"video":.*?"baseUrl":".*?","base_url"')
        video_url = video_url_pattern.findall(response.text)[0]
        video_url = utils.removeSubStr(video_url, r'"video":.*?baseUrl":"', r'","base_url"')
        audio_url_pattern = re.compile(r'"audio":.*?"baseUrl":".*?","base_url"')
        audio_url = audio_url_pattern.findall(response.text)[0]
        audio_url = utils.removeSubStr(audio_url, r'"audio":.*?baseUrl":"', r'","base_url"')
        return {
            Downloader.NAME: name,
            Downloader.VIDEO_URL: video_url,
            Downloader.AUDIO_URL: audio_url
        }