'''
    plugin template, implement setup and run method, this is entry point of tool box
'''
from .downloaders import factory

class Plugin:
    def __init__(self) -> None:
        self.url = None

    def setup(self):
        self.url = input("Enter url >>> ")
    
    def run(self):
        factory.download(self.url)