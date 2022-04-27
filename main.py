import logging

from src.backend import file_manager as flmg, startupchecks as suc
import src.view.GUI as g

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    suc.startup_checks()
    # TODO: preload settings
    #d_paths = flmg.load_from_json('./src/conf/linker.json',{})
    #logging.basicConfig(filename=path.join(d_paths['ref'],"logging.log"), level=logging.DEBUG)
    #app = g.GUI()
    #app.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
