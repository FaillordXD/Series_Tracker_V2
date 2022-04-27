import PySimpleGUI as sg
from os import path, mkdir

SETTINGS_PATH = '.'


def set_save():
    layout = [[sg.Text('Enter a save location:')],
              [sg.Input(sg.user_settings_get_entry('save', ''), key='-IN-SAVE-'), sg.FolderBrowse()],
              [sg.B('Save')]]

    window = sg.Window('Filename Example', layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Save':
            sp = path.abspath(values['-IN-SAVE-'])
            if not path.exists(values['-IN-SAVE-']):
                mkdir(sp)
            sg.user_settings_set_entry('save', sp)
            break
    window.close()


def set_sub():
    sf = sg.user_settings_get_entry("save")
    layout = [[sg.Text(f'Name folder or select existing folder in "{path.split(sf)[1]}"')],
              [sg.Text('Enter a image location:'),
               sg.Input(sg.user_settings_get_entry('image', ''), key='-IN-IMG-'), sg.FolderBrowse()],
              [sg.Text('Enter a reference location:'),
               sg.Input(sg.user_settings_get_entry('ref', ''), key='-IN-REF-'), sg.FolderBrowse()],
              [sg.Text('Enter a data location:'),
               sg.Input(sg.user_settings_get_entry('SDF', ''), key='-IN-SDF-'), sg.FolderBrowse()],
              [sg.B('Save')]]

    window = sg.Window('Filename Example', layout)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        elif event == 'Save':
            if values['-IN-IMG-'] and values['-IN-REF-'] and values['-IN-SDF-']:
                x = [values['-IN-IMG-'], values['-IN-REF-'], values['-IN-SDF-']]
                for i, pa in enumerate(x):
                    com_path = path.commonpath([sf, path.abspath(pa)])
                    if path.split(com_path)[1] != path.split(sf)[1]:
                        pa = path.join(sf, path.split(pa)[1])
                    if not path.exists(pa):
                        mkdir(pa)
                    x[i] = path.relpath(path.normpath(pa), start=sf)
                sg.user_settings_set_entry('image', x[0])
                sg.user_settings_set_entry('ref', x[1])
                sg.user_settings_set_entry('S_df', x[2])
                break
            else:
                sg.popup_timed("\tAll Folders need to be set.\n"
                               "Please select existing folders within save\n"
                               "\t\tor name new ones")
    window.close()


def ini_run(initpath=SETTINGS_PATH):
    sg.user_settings_filename(path=initpath, filename="settings.json")
    set_save()
    set_sub()


def get_settings(initpath=SETTINGS_PATH):
    sg.user_settings_filename(path=initpath, filename="settings.json")
    return sg.user_settings_object()


if __name__ == '__main__':
    ini_run()
