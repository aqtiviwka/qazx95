import json
import os
import sys
from re import fullmatch

os.environ['DJANGO_SETTINGS_MODULE'] = 'qazx95.settings'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django
django.setup()

from load_json_file.models import Data

def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if f.name[-5:] == '.json':
        with open(f"uploads/{f.name}", "r") as json_file:
            data = json.load(json_file)
            dict_data = []
            if all(map(lambda item: ('name' in item) and ('date' in item), data)):
                print('File is correct')
                for i in data:
                    if not len(i['name']) <= 50 and fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}',
                                                              i['date']):
                        print('Data is not valid')
                        dict_data = []
                        break
                    else:
                        dict_data.append(dict(name=i["name"], date=i["date"]))
                print(dict_data)

            else:
                print('File is not correct')
        return True
    else:
        return False


# class UploadingData(object):
#     def __init__(self, data):
#         data = data
#         self.uploaded_file = data.get('file')
#         self.parsing()
#
#     def parsing(self):
#         print(type(self.uploaded_file))
#         # with open(self.uploaded_file, 'r') as f:
#         #     load_data = json.load(f)
#         #     print(load_data)
#         return False