import json


def save_to_json(file,save_data):
    """
        saves Dictionary to JSON file [file].
        Parameters:
        file : name of the file
                 (Example: '../save/file.json')
        defaultdata : list of seasons of the series (Used for Name of sheets)
        Returns: dict
    """
    json_object = json.dumps(save_data, indent=4)
    with open(file, "w") as outfile:
        outfile.write(json_object)