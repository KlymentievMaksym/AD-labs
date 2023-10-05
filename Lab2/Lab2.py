# import matplotlib as mtplt
# import numpy as np
# import cherrypy
# import jinja2
# import dataspyre as 
# import urllib
# import json
# from spyre import server
# import pandas as pd

# import os
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