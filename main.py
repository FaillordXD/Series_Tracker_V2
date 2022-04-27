import logging
import sys
from os import path
from src.backend import file_manager as flmg, startupchecks as suc
import src.view.GUI as g

if getattr(sys, 'frozen', False):
    application_path = path.dirname(sys.executable)
# or a script file (e.g. `.py` / `.pyw`)
elif __file__:
    application_path = path.dirname(__file__)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    suc.startup_checks(application_path)
    # TODO: preload settings
    app = g.GUI()
    app.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
