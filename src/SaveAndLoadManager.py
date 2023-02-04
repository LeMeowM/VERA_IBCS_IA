import json
import os


class SaveAndLoadSystem:
    def __init__(self, save_folder):
        self.save_folder = save_folder
        self.file_data = {'file_1': False, 'file_2': False,
                          'file_3': False}

    def save_file(self, data, file):
        #save_file = open(self.save_folder + '/' + file + '.json', "wb")
        json_object = json.dumps(data)
        with open(self.save_folder + '/' + file + '.json', "w") as outfile:
            outfile.write(json_object)

    def load_save(self, file):
        save_file = open(self.save_folder + '/' + file + '.json', "rb")
        if os.stat(self.save_folder + '/' + file + '.json').st_size != 0:
            return json.load(save_file)
        else:
            return None

    def delete_save(self, file):
        return os.remove(self.save_folder + '/' + file + '.json')

    def check_for_file(self, file):
        return os.path.exists(self.save_folder + '/' + file + '.json')
