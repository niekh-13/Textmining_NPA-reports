##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    saving json                                             #
#                                                            #
##############################################################

# Import the relevant packages
from pathlib import Path
import json


class Save:

    # Set some initial attributes to define and create a save location for the images.
    def __init__(self, module_path:str='.py'):
        subdir = Path(module_path).name.split('.')[0]

        self.json_dir = Path('json') / subdir
        self.json_dir.mkdir(exist_ok=True, parents=True)

    def save(self, json_obj, name):

        json_name = f'{name}'
        format = 'json'

        save_path = self.json_dir / f'{json_name}.{format}'
        with open(save_path, 'w') as json_file:
            json.dump(json_obj, json_file)
        print(f'Json saved to {save_path}')
