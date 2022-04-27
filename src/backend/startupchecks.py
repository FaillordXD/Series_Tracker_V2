from os import path
import src.view.iniwindow as ini
from src.backend.gen_webscrape import extract_image
from PySimpleGUI import user_settings_set_entry
def gen_missing_files(user_settings):
    thumb_path = path.join(path.join(user_settings['save'], user_settings['image']), 'Thumbnail.png')
    searchthumb_path = path.join(path.join(user_settings['save'], user_settings['image']), 'Search_Thumbnail.png')
    if not path.exists(thumb_path):
        extract_image(thumb_path)
        user_settings_set_entry('Thumbnail',path.relpath(user_settings['image'],thumb_path))
    if not path.exists(searchthumb_path):
        extract_image(searchthumb_path)
        user_settings_set_entry('SearchThumbnail', path.relpath(user_settings['image'], searchthumb_path))
    if 'fontsize' not in user_settings.dict.keys():
        user_settings_set_entry('fontsize', 10)
    if 'SeasonPerRow' not in user_settings.dict.keys():
        user_settings_set_entry('SeasonPerRow', 20)
        if 'SeasonTotal' not in user_settings.dict.keys():
            user_settings_set_entry('SeasonTotal', 5)



def startup_checks(app_path):
    if not path.exists('settings.json'):
        ini.ini_run(app_path)
    settings = ini.get_settings(app_path)
    gen_missing_files(settings)
