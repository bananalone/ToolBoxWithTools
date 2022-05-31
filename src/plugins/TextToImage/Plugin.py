'''
    plugin template, implement setup and run method, this is entry point of tool box
'''
import os

from PIL import Image, ImageDraw, ImageFont


class Plugin:
    def __init__(self) -> None:
        self.text_path = None
        self.img_path = None
        self.font_size = 28
        self.font_color = (0, 0, 0)
        self.bgcolor = (255, 255, 255)

    def setup(self):
        user_input = input("Enter path to text file >>> ")
        if not os.path.isfile(user_input):
            raise Exception("{} is not a file".format(user_input))
        self.text_path = user_input
        user_input = input("Enter path to save >>> ")
        if len(user_input) == 0:
            _substrs = self.text_path.split('.')
            _substrs[-1] = 'jpg'
            self.img_path = '.'.join(_substrs)
        else:
            if os.path.exists(user_input):
                raise Exception("{} should not exist".format(user_input))
            self.img_path = user_input
        user_input = input("Enter font size >>> ")
        self.font_size = int(user_input) if len(user_input) != 0 else self.font_size
        user_input = input("Enter font color (R, G, B) >>> ")
        self.font_color = tuple([int(c) for c in user_input.split(',')]) if len(user_input) != 0 else self.font_color
        user_input = input("Enter background color (R, G, B) >>> ")
        self.bgcolor = tuple([int(c) for c in user_input.split(',')]) if len(user_input) != 0 else self.bgcolor

    def _cal_width(self, line: str) -> int:
        num_chinese = int((len(line.encode('utf-8')) - len(line))/2)
        num_ascii = len(line) - num_chinese
        return (num_ascii + 1) // 2 + num_chinese

    def _text2image(self, text: str, save_path: str):
        lines = text.split('\n')
        rows = len(lines)
        len_of_line = [self._cal_width(line) for line in lines]
        cols = max(len_of_line)
        size = (int(cols * self.font_size), rows * self.font_size)
        img = Image.new('RGB', size, self.bgcolor)
        dr = ImageDraw.Draw(img)
        font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "fonts", "SimSun.ttf"), self.font_size)
        dr.text((0, 0), text, font=font, fill=self.font_color)
        img.save(save_path)

    def run(self):
        with open(self.text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        self._text2image(text, self.img_path)


if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()
