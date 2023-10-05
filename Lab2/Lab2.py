# import matplotlib as mtplt
# import numpy as np
# import cherrypy
# import jinja2
# import dataspyre as 
# import urllib
# import json
# from spyre import server
# import pandas as pd
# from ..__init__.py import *
import os
# print(os.getcwd())
# input()
# from .Lab1.Lab1 import receive_list_of_csv, get_dict_for_transfer

# class DropdownForVCI_TCI_VHI(server.App):
#     title = "NOAA data vizualization"
    
#     inputs = [{"type": 'dropdown',
#                "label": 'NOAA data dropdown',
#                "options": [{"label":"VCI", "value":"VCI"},
#                           {"label":"TCI", "value":"TCI"},
#                           {"label":"VHI", "value":"VGI"}],
#                "key":'ticker',
#                "action_id": "update_data"}]
    
# class TextEntryForMonthInterval(server.App):
#     title = "Text entry for month interval"
    
#     inputs = [{"type": 'text',
#                "label": 'data-ranges',
#                "options": [{"label":"VCI", "value":"VCI"},
#                           {"label":"TCI", "value":"TCI"},
#                           {"label":"VHI", "value":"VGI"}],
#                "key":'range',
#                "value":'9-10',
#                "action_id": "simple_html_output"}]
    
#     def getHTML(self, params):
#         ranges = params["range"]
#         return ranges

# class TableAndPlot(server.App):
#     title = "Table and plot"
    
#     inputs = [{"type": 'plot',
#                "id": 'plot',
#                "control_id": 'update_data',
#                "tab": 'Plot'},
#                {"type": 'table',
#                 "id": 'table_id',
#                 "control_id": 'update_data',
#                 "tab": 'Table',
#                 "on_page_load": True}]

# list_of_csv = receive_list_of_csv()
# print(list_of_csv)
if not os.path.exists("Csv\\"):
    create_VHI_dataset()
    dict_for_df = get_dict_for_df()
else:
    k = 0
    for name in os.listdir("Csv\\"):
        path = "Csv\\" + name
        df = read_VHI_dataframe(path)
        dict_for_df[k] = df
        k += 1
dict_for_transfer = get_dict_for_transfer()

# for file_name in list_of_csv:
    # pass