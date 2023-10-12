# import matplotlib as mtplt
# import numpy as np
# import cherrypy
# import jinja2
# import dataspyre as 
import urllib
# import json
# from spyre import server
# import pandas as pd

import os
import pandas as pd
from spyre import server
headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']

class TheBestApp(server.App):
    title = "NOAA data vizualization"
    inputs = [
        {"type": 'dropdown',
        "label": 'NOAA data dropdown',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'ticker',
        "action_id": "Show_data"},
        {"type": 'text',
        "label": 'Data Time (Year)',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'range',
        "value":'1982-2023',
        "action_id": "Show_data"},
        {"type": 'text',
        "label": 'Data Time (Week)',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'rangeW',
        "value":'1-52',
        "action_id": "Show_data"}]

    # controls = [{
    #         "type": "button",
    #         "label": "Load Table",
    #         "id": "Show_data"
    #     }]

    outputs = [{
        "type": "table",
        "id": "Show_data",
        "control_id": "update_data",
        "tab": "Table",
        "on_page_load": True
    }]

    def getData(self, params):
        ticker = params['ticker']
        drange = params['range']
        dwrange = params['rangeW']
        
        df = pd.read_csv("Csv\\NOAA_ID1_05-10-2023-20-41-41.csv", index_col=None, header=1, names=headers)
        df['Area'] = 1
        df = df.drop(df.loc[df['VHI'] == -1].index)
        # print(r"||||||||||||||||||||||||||||||", int(drange[:4]), int(drange[5:]), r"||||||||||||||||||||||||||||||") #[str(ticker).find("ticker=")+7:str(ticker).find("ticker=")+10]
        
        drange = drange.split("-")
        dwrange = dwrange.split("-")
        
        cond_year = (df.Year>=int(drange[0])) & (df.Year<=int(drange[1]))
        cond_week = (df.Week>=int(dwrange[0])) & (df.Week<=int(dwrange[1]))
        
        list_of_things_to_view = ["Year", "Week", str(ticker), "Area"]
        
        return df.loc[cond_year & cond_week][list_of_things_to_view]


app1 = TheBestApp()
app1.launch(port=9093)
