'''
    plugin template, implement setup and run method, this is entry point of tool box
'''

import os

class Plugin:
    _BYTE_ORDER = 'little'
    _ENCODING = 'utf-8'
    
    def __init__(self) -> None:
        self._path = ''
        self._key = 'bananalone'

    def setup(self):
        '''
            set the necessary parameters
        '''
        user_input = input("Enter path of a file or folder >>> ")
        self._path = user_input if len(user_input) else self._path
        if not os.path.exists(self._path):
            raise FileNotFoundError(self._path)
        user_input = input("Enter your key >>> ")
        self._key = user_input if len(user_input) else self._key
        
    def _encrypt(self, path: str):
        if os.path.isfile(path):
            with open(path, 'rb') as f:
                b_content = f.read()
            len_content = len(b_content)
            b_key = bytes(self._key, encoding=Plugin._ENCODING)
            len_key = len(b_key)
            b_encrypted = bytearray()
            i = 0
            while i < len_content:
                j = i % len_key
                while i < len_content and j < len_key:
                    b_encrypted.append(b_content[i] ^ b_key[j])
                    i += 1
                    j += 1
            with open(path, 'wb') as f:
                f.write(b_encrypted)
        else:
            subpath = [os.path.join(path, n) for n in os.listdir(path)]
            for p in subpath:
                self._encrypt(p)
    
    def run(self):
        '''
            run
        '''
        print("Use {key} encrypt {path}".format(key = self._key, path = self._path))
        self._encrypt(self._path)
    
    
if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()
