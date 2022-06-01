'''
    plugin template, implement setup and run method, this is entry point of tool box
'''
import os
from .auto import bot

class Plugin:
    def __init__(self) -> None:
        self.script = None

    def setup(self):
        user_input = input("Enter path to script >>> ")
        if not os.path.exists(user_input):
            raise Exception("{} do not exists".format(user_input))
        self.script = user_input
    
    def run(self):
        with open(self.script, 'r', encoding='utf-8') as f:
            script = f.read()
        bot.exec(script)
        print(script)


if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()