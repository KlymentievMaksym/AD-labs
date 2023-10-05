# import matplotlib as mtplt
# import numpy as np
# import cherrypy
# import jinja2
# import dataspyre as 
# import urllib
# import json
# from spyre import server
# import pandas as pd

import os
import pandas as pd
from spyre import server
headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']

def read_VHI_dataframe(path_for_file):
    df = pd.read_csv(path_for_file, index_col=None, header=1, names=headers)
    # print(df.head())
    return df

for name in os.listdir("Csv\\"):
    df = read_VHI_dataframe("Csv\\" +name)
    # print(df)



# class SimpleApp(server.App):
# 	title = "Simple App"
# 	inputs = [{
# 		"type": "text",
# 		"key": "words",
# 		"label": "write words here",
# 		"value": "hello world", 
# 		"action_id": "simple_html_output"
# 	}]

# 	outputs = [{
# 		"type": "html",
# 		"id": "simple_html_output"
# 	}]

# 	def getHTML(self, params):
# 		words = params["words"]
# 		return "Here's what you wrote in the textbox: <b>%s</b>" % words

# import os
class DropdownForVCI_TCI_VHI(server.App):
    title = "NOAA data vizualization"
    
    inputs = [{"type": 'dropdown',
                "label": 'NOAA data dropdown',
                "options": [{"label":"VCI", "value":"VCI"},
                          {"label":"TCI", "value":"TCI"},
                          {"label":"VHI", "value":"VGI"}],
                "key":'ticker',
                "action_id": "update_data"},
              {"type": 'text',
                "label": 'data-ranges',
                "options": [{"label":"VCI", "value":"VCI"},
                          {"label":"TCI", "value":"TCI"},
                          {"label":"VHI", "value":"VGI"}],
                "key":'range',
                "value":'9-10',
                "action_id": "simple_html_output"}]
    outputs = [{"type": 'plot',
      "id": 'plot',
      "control_id": 'update_data',
      "tab": 'Plot'},
      {"type": 'table',
      "id": 'table_id',
      "control_id": 'update_data',
      "tab": 'Table',
      "on_page_load": True}]
#     def getHTML(self, params):
#         ranges = params["range"]
#         return ranges
# class TextEntryForMonthInterval(server.App):
#     title = "Text entry for month interval"
    
#     inputs = []
    
    

# class TableAndPlot(server.App):
#     title = "Table and plot"
    
#     inputs = []

# app = DropdownForVCI_TCI_VHI()
# app.launch(port=9097)
# app1 = TextEntryForMonthInterval()
# app1.launch(port=9095)
app1 = DropdownForVCI_TCI_VHI()
app1.launch(port=9093)