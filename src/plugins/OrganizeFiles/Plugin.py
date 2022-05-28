'''
    plugin template, implement setup and run method, this is entry point of tool box
'''

import os
import shutil

from tqdm import tqdm


class Plugin:
    def __init__(self) -> None:
        self._folder_path = None
        self._save_path = None

    def setup(self):
        '''
            set the necessary parameters
        '''
        self._folder_path = input("Enter the folder you want to organize >>> ")
        if not os.path.isdir(self._folder_path):
            raise Exception("{} is not a folder".format(self._folder_path))
        self._save_path = input("Enter the path you want to save >>> ")
        if os.path.exists(self._save_path):
            raise Exception("{} already exists".format(self._save_path))
        os.makedirs(self._save_path)
    
    def run(self):
        '''
            run
        '''
        if self._folder_path is None or self._save_path is None:
            return
        files = os.listdir(self._folder_path)
        for file in tqdm(files):
            path_to_file = os.path.join(self._folder_path, file)
            if os.path.isfile(path_to_file):
                suffix = file.split('.')[-1]
                save_to = os.path.join(self._save_path, suffix)
                if not os.path.exists(save_to):
                    os.makedirs(save_to)
                shutil.copyfile(path_to_file, os.path.join(save_to, file))
            elif os.path.isdir(path_to_file):
                save_to = os.path.join(self._save_path, 'folders')
                if not os.path.exists(save_to):
                    os.makedirs(save_to)
                shutil.copytree(path_to_file, os.path.join(save_to, file))
        
        
if __name__ == '__main__':
    plugin = Plugin()
    plugin.setup()
    plugin.run()