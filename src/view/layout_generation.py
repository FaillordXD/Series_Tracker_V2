import logging

import PySimpleGUI as sg
import PIL
import io
import base64
from os.path import join
import json

BUTTON_SELECTED=('#000000','#FF6F00')
BUTTON_DESELECTED=('#FF6F00', '#000000')
BUTTON_DELETE = ('#FFFFFF','#FF0000')



def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


def g_series_layout(fontsize = 12):
    '''
    Generates Upper left column. Selectable series from listbox and search field.

    :key '-SEARCH-','-SERIE-'

    :param fontsize:
    :type fontsize: int
    :return: layout for upper left column
    '''
    font = ('Arial', fontsize)
    series_names = []
    E_text = sg.Text('Serien suche:',font=font)
    E_input = sg.Input(size=(0, 1), enable_events=True, key='-SEARCH-',font=font, expand_x=True, focus=False)
    E_seasonlist = sg.Listbox(series_names, key='-SERIE-', enable_events=True, font = font, size=(60, 31), expand_y=True)
    return [[E_seasonlist], [sg.Text('')], [E_text, E_input]]


def g_season_layout(max_cnt,entry_cnt,fontsize=12):
    """
    Generates the layout of the upper right column.

    :key '-THUMBNAIL-', '-DESCRIPTION-','-SEASON-%0', f'-SEASON-%{x}','-EPISODE-',
    '-REFRESH-THIS-', '-SET-FAVORITE-','-DEL-'

    :param max_cnt: maximum number of seasons
    :type max_cnt: int
    :param entry_cnt: seasons per row
    :type entry_cnt: int
    :param fontsize: size of the font
    :type fontsize: int
    :return: layout of the upper right column
    """
    font = ('Arial', fontsize)
    episodes = []
    season_cnt = [[i + entry_cnt * rows + 1 for i in range(entry_cnt)] for rows in range(round(max_cnt / entry_cnt))]
    if max_cnt % entry_cnt > 0:
        season_cnt.append([b + max_cnt - max_cnt % entry_cnt + 1 for b in range(max_cnt % entry_cnt)])
    #request_data('thumbnail', specific='https://bs.to/public/images/default-cover.jpg')  # TODO: implement search
    with open(join('.',join('src',join('conf','linker.json'))),'r') as f:
        d_folder = json.load(f)
    img_p = d_folder['thumbnail']
    I_thumbnail = sg.Image(data=convert_to_bytes(img_p, (100, 150)), key='-THUMBNAIL-')
    T_descriptiontext = sg.Text('', key='-DESCRIPTION-', expand_x=True)
    C_image = sg.Column([[I_thumbnail]], justification='t', pad=(0, (0, 15)),expand_x=True)
    C_descriptiontext = sg.Column([[T_descriptiontext]], justification='top')
    C_special = sg.Column([[sg.pin(sg.Button('Special', key=f'-SEASON-%{0}', size=(7, 1), font=font, visible=True,
                                      enable_events=True))], [sg.VStretch()]],size=(80,0), expand_y=True)
    B_season = [[sg.Button(c, key=f'-SEASON-%{c}',
                           size=(3, 1), font=font,
                           visible=True,
                           enable_events=True) for c in y]  for y in season_cnt]
    F_seasonselection = sg.Frame('', B_season)
    L_episodes = sg.Listbox(episodes, key='-EPISODE-', enable_events=True, font=font,expand_x=True,size=(None,15))
    B_refresh = sg.Button('Refresh', key='-REFRESH-THIS-', enable_events=True, font=font,  visible=True)
    B_favorite = sg.Button('Set Favorite', key='-SET-FAVORITE-', font=font, enable_events=True,
                           visible=True)
    B_delete = sg.Button('Delete', key='-DEL-', font=font, enable_events=True, button_color=BUTTON_DELETE,
                         visible=True)
    B_functions = [B_refresh,sg.Text('  '),B_favorite,sg.Stretch(),B_delete]
    C_season = sg.Column([[F_seasonselection],[sg.Text('')],[L_episodes],[sg.Text('')],B_functions,[sg.Text('')]],element_justification='l')
    return [[C_image,C_descriptiontext],[C_special,C_season]]


def g_watch_layout(fontsize=12):
    """
    generates layout for lower left column. contains languages and hosts

    key: 

    :param fontsize: size of the font
    :type fontsize: int
    :return:
    """
    #language = request_data('languages')
    #hosts = request_data('hosts')
    #A_languages = [generate_Button(lang_k, lang_v, size=(15, 1)) for lang_k, lang_v in language.items()]
    #A_Hosts = [generate_Button('', host_k, image=host_v) for host_k, host_v in hosts.items()]
    B_languages = [sg.Button('lang',key = 'de')] # text from dict
    B_host = [sg.Button('host',key = 'host')] # image
    F_languages = sg.Frame('Languages', [B_languages])
    F_Hosts = sg.Frame('Host', [B_host])
    C_watch = sg.Column([[F_languages], [sg.Text('')], [F_Hosts]], justification='left')
    return [[C_watch]]


def g_function_layout():
    B_next = sg.Button('Continue', key='-GO-')
    B_new = sg.Button('New', key='-ADD-', pad=((0, 25), 0))
    B_refresh = sg.Button('Refresh', key='-REFRESH-', pad=((0, 85), 0))
    B_end = sg.Button('End', key='Exit')
    C_Functions = sg.Column([[sg.Push(), B_next, B_new, B_refresh, sg.Push(), B_end]])
    return [[C_Functions]]


def generate_layout(max_seasons=None,el_per_row=None):
    '''
    Function to generate the layout of the GUI
    :return: Layout for GUI
    '''
    if max_seasons == None:
        max_seasons = 20
    if el_per_row == None:
        el_per_row = 20
    C_series_selection = sg.Column(g_series_layout(),element_justification='l',expand_y=True)
    C_episode_selection = sg.Column(g_season_layout(max_seasons,el_per_row),element_justification='c')
    C_watch_selection = sg.Column(g_watch_layout(),expand_x=True)
    C_function_selection = sg.Column(g_function_layout(),expand_x=True)
    layout = [[C_series_selection,sg.VerticalSeparator(pad=(20,None)), C_episode_selection],
              [sg.HSeparator(pad= (None, 10))],
              [C_watch_selection, sg.vbottom(C_function_selection)]]
    # layout = [[sg.Text('Enter Text')],[sg.Button('close', key='close')]]
    return layout