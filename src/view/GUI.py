import base64
import io
import logging

import PIL
import PySimpleGUI as sg
from PIL import Image

import src.view.layout_generation as lg
#from GUI_requests import request_data, event_request
#from src.backend import web_scraper

c = sg.LOOK_AND_FEEL_TABLE
black_orange = {'BACKGROUND': '#030320',
                'TEXT': '#FF6F00',
                'INPUT': '#FCC57C',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#E3E3E3',
                'BUTTON': ('#FF6F00', '#000000'),
                'PROGRESS': ('#000000', '#000000'),
                'BORDER': 2,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

sg.theme_add_new('MyBlackOrange', black_orange)
sg.theme('MyBlackOrange')

BUTTON_SELECTED=('#000000','#FF6F00')
BUTTON_DESELECTED=('#FF6F00', '#000000')
BUTTON_DELETE = ('#FFFFFF','#FF0000')


class GUI:

    def __init__(self):
        FontSize = sg.user_settings_get_entry('fontsize')
        max_seasons = sg.user_settings_get_entry('SeasonTotal')
        el_per_row = sg.user_settings_get_entry('SeasonPerRow')
        layout = lg.generate_layout(max_seasons=max_seasons,el_per_row=el_per_row,fontsize=FontSize)
        self.mainWindow = sg.Window('Test', layout, element_padding=(0, 0), finalize=True)
        for i in range(max_seasons + 1):
            self.mainWindow[f'-SEASON-%{i}'].update(visible=False)
        self.focus = None
        location = self.mainWindow.current_location()
        location = location[0] - 200, location[1] + 200

    def update_elements(self):
        pass

    def run(self):
        while True:
            cur_focus = self.mainWindow.find_element_with_focus()
            if cur_focus is not None:
                self.focus = cur_focus
            event, values = self.mainWindow.read(
                timeout=200, timeout_key='timeout')
            if event != "timeout":
                logging.debug(f'event: {event}, values: {values}')
            if event == '-SEE-':
                for i in range(max_seasons+1):
                    self.mainWindow[f'-SEASON-%{i}'].update(visible=True)
            if event == 'close' or event == sg.WIN_CLOSED:
                break


        self.mainWindow.Close()
