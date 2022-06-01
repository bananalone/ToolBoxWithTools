import time
import pyautogui


class Bot:
    def __init__(self) -> None:
        self.cmds = {}

    def register(self, *names):
        def cmd_func(func):
            for name in names:
                self.cmds[name] = func
            return func
        return cmd_func

    def exec(self, script: str):
        lines = script.strip().split('\n')
        for line in lines:
            words = line.split(maxsplit=1)
            cmd = words[0]
            if cmd not in words:
                continue
            if len(words) > 1:
                args = [arg.strip() for arg in words[1].split(',')]
                self.cmds[cmd](*args)
            else:
                self.cmds[cmd]
            time.sleep(0.2)


bot = Bot()

CONFIDENCE = 0.9

@bot.register('mv', 'move')
def move(path: str):
    loc = pyautogui.locateCenterOnScreen(path, confidence=CONFIDENCE)
    pyautogui.moveTo(loc)

@bot.register('c', 'click', 'lc', 'left-click')
def click(path: str):
    mouse_loc = pyautogui.position()
    loc = pyautogui.locateCenterOnScreen(path, confidence=CONFIDENCE)
    pyautogui.click(loc)
    pyautogui.moveTo(mouse_loc)

@bot.register('dc', 'double-click')
def doubleClick(path: str):
    mouse_loc = pyautogui.position()
    loc = pyautogui.locateCenterOnScreen(path, confidence=CONFIDENCE)
    pyautogui.doubleClick(loc)
    pyautogui.moveTo(mouse_loc)

@bot.register('rc', 'right-click')
def rightClick(path: str):
    mouse_loc = pyautogui.position()
    loc = pyautogui.locateCenterOnScreen(path, confidence=CONFIDENCE)
    pyautogui.rightClick(loc)
    pyautogui.moveTo(mouse_loc)

@bot.register('tw', 'typewrite')
def typewrite(msg: str):
    pyautogui.typewrite(msg, 0.2)

@bot.register('sc', 'scroll')
def scroll(clicks: str):
    pyautogui.scroll(int(clicks))