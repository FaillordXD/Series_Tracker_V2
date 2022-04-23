import time
from os import mkdir
from os import path
import logging
logging.basicConfig(filename="save/ref/logging.log" ,level=logging.DEBUG)

from src.backend import file_manager as flmg
import src.view.GUI as g


def foldersetup():
    with open('./init.txt','r') as f:
        setup = f.read()
    dir_list=setup.split(',')
    if not path.exists(f'./{dir_list[0]}'):
        mkdir(f'./{dir_list[0]}')
        d_link = {'save':dir_list[0]}
        l_link = ['image','ref','S_df']
        for i in range(len(dir_list)-1):
            mkdir(path.join(f'./{dir_list[0]}',dir_list[i+1]))
            d_link[l_link[i]] = dir_list[i+1]

        flmg.save_to_json('./src/conf/linker.json',d_link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    foldersetup()
    app = g.GUI()
    app.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
