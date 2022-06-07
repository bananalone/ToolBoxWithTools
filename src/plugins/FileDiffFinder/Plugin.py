'''
    plugin template, implement setup and run method, this is entry point of tool box
'''
import os
from .DiffFinder import DiffFinder

class Plugin:
    def __init__(self) -> None:
        self.first_path = None
        self.second_path = None
        self.diffFinder = DiffFinder()

    def setup(self):
        user_input = input("Enter path to first file >>> ")
        if not os.path.isfile(user_input):
            raise Exception(f'{user_input} is not a file')
        self.first_path = user_input
        user_input = input("Enter path to second file >>> ")
        if not os.path.isfile(user_input):
            raise Exception(f'{user_input} is not a file')
        self.second_path = user_input
    
    def run(self):
        with open(self.first_path, 'r', encoding='utf-8') as f:
            former = f.read()
        with open(self.second_path, 'r', encoding='utf-8') as f:
            latter = f.read()
        self.diffFinder.analyse(former, latter)
        print(self.diffFinder.format())


if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()
        