from os import path
import src.view.iniwindow as ini
from src.backend.gen_webscrape import extract_image

def gen_missing_files(user_settings):
    no_img_path = path.join(path.join(user_settings['save'],user_settings['image']),'default.png')
    thumb_path = path.join(path.join(user_settings['save'], user_settings['image']), 'Thumbnail.png')
    searchthumb_path = path.join(path.join(user_settings['save'], user_settings['image']), 'Search_Thumbnail.png')
    if not path.exists(no_img_path):
        extract_image(no_img_path)
    if not path.exists(thumb_path):
        extract_image(thumb_path)
    if not path.exists(searchthumb_path):
        extract_image(searchthumb_path)



def startup_checks():
    if not path.exists('settings.json'):
        ini.ini_run('.')
    settings = ini.get_settings('.')

    gen_missing_files(settings)
