'''
    plugin template, implement setup and run method, this is entry point of tool box
'''
import os

from .Matcher import FileMatcher

class Plugin:
    def __init__(self) -> None:
        self.root = '.'
        self.pattern = None
        self.fileMatcher = FileMatcher()

    def setup(self):
        user_input = input('Enter root >>> ') 
        self.root = user_input if len(user_input) > 0 else self.root
        if not os.path.exists(self.root):
            raise Exception("Root do not exists")
        user_input = input("Enter pattern >>> ")
        self.pattern = user_input if len(user_input) > 0 else self.pattern
        if not self.pattern:
            raise Exception("Pattern not set")

    def run(self):
        fdists = []
        self._list_fdists(self.root, fdists)
        fdists.sort(key=lambda x:x[1])
        distThres = fdists[0][1]
        for fdist in fdists:
            if fdist[1] > distThres:
                break
            else:
                print(fdist[0])
    
    def _list_fdists(self, root: str, files: list) -> list:
        names = os.listdir(root)
        for name in names:
            file = os.path.join(root, name)
            if os.path.isfile(file):
                dist = self.fileMatcher.distance(name, self.pattern)
                files.append([file, dist])
            elif os.path.isdir(file):
                self._list_fdists(file, files)


if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()