# import matplotlib as mtplt
# import cherrypy
# import jinja2
# import json
# import numpy as np

import urllib
import datetime
import os
import pandas as pd
from spyre import server

headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
dict_for_transfer = {
    22: 1,
    23: 2,
    24: 3,
    25: 4,
    3: 5,
    4: 6,
    8: 7,
    19: 8,
    20: 9,
    21: 10,
    9: 11,
    26: 12,
    10: 13, 
    11: 14,
    12: 15,
    13: 16,
    14: 17,
    15: 18,
    16: 19,
    27: 20, 
    17: 21,
    18: 22,
    6: 23,
    1: 24,
    2: 25,
    7: 26,
    5: 27
    }


def find_needed_id_for_NOAA(our_id):
    for id in dict_for_transfer:
        if dict_for_transfer[id] == our_id:
            return id


def find_needed_path(bpath):
    # print(bpath)
    for fpath in os.listdir("Csv\\"):
        if bpath in fpath:
            return fpath


def check_file_existence(file_name_i, is_need_name=False):
    try:
        list_of_csv = os.listdir("Csv")
    except FileNotFoundError:
        os.mkdir('Csv\\')
        list_of_csv = os.listdir("Csv")
    for name in list_of_csv:
        if 'NOAA_ID'+str(file_name_i) in name:
            if is_need_name:
                return name
            return True
    return False


def create_file(i, date_and_time_time, text):
    path_for_file = r'Csv\NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv'
    with open(path_for_file,'wb') as out:
        out.write(text.encode())
    return path_for_file
    

def create_VHI_dataset():
    for i in range(1,28):
        print(f"\nCreating NOAA with id {i}")
        url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID="+str(i)+"&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=land&year1=1982&year2=2023"
        vhi_url = urllib.request.urlopen(url)
        
        text = vhi_url.read()
        text = text.decode()
        # print(type(text))
        text = text.replace("b'","")
        text = text.replace("'","")
        text = text.replace(",  from 1982 to 2023,","  from 1982 to 2023")
        text = text.replace(",\n","\n")
        text = text.replace("</pre></tt>","")
        text = text.replace("<tt><pre>","")
        text = text.replace("<br>","")

        now = datetime.datetime.now()
        date_and_time_time = now.strftime("%d-%m-%Y-%H-%M-%S")
        
        if not check_file_existence(i):
            create_file(i, date_and_time_time, text)
        else:
            print("\nFile already exists\n")


try:
    for npath in os.listdir("Csv\\"):
        pass
except FileNotFoundError:
    create_VHI_dataset()


class TheBestApp(server.App):
    title = "NOAA data vizualization"
    inputs = [
        {"type": 'dropdown',
        "label": 'NOAA data dropdown',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'ticker',
        "action_id": "update_data"},
        
        {"type": 'dropdown',
        "label": 'Province',
        "options": [{"label":"Vinnytsya", "value":"1"},
                  {"label":"Volyn", "value":"2"},
                  {"label":"Dnipropetrovsk", "value":"3"},
                  {"label":"Donetsk", "value":"4"},
                  {"label":"Zhytomyr", "value":"5"},
                  {"label":"Transcarpathia", "value":"6"},
                  {"label":"Zaporizhzhya", "value":"7"},
                  {"label":"Ivano-Frankivsk", "value":"8"},
                  {"label":"Kiev", "value":"9"},
                  {"label":"Kirovohrad", "value":"10"},
                  {"label":"Luhansk", "value":"11"},
                  {"label":"Lviv", "value":"12"},
                  {"label":"Mykolayiv", "value":"13"},
                  {"label":"Odessa", "value":"14"},
                  {"label":"Poltava", "value":"15"},
                  {"label":"Rivne", "value":"16"},
                  {"label":"Sumy", "value":"17"},
                  {"label":"Ternopil", "value":"18"},
                  {"label":"Kharkiv", "value":"19"},
                  {"label":"Kherson", "value":"20"},
                  {"label":"Khmelnytskyy", "value":"21"},
                  {"label":"Cherkasy", "value":"22"},
                  {"label":"Chernihiv", "value":"23"},
                  {"label":"Chernivtsi", "value":"24"},
                  {"label":"Crimea", "value":"25"},
                  {"label":"Kiev City", "value":"26"},
                  {"label":"Sevastopol", "value":"27"}],
        "key":'province',
        "action_id": "update_data"},

        {"type": 'text',
        "label": 'Data Time (Year)',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'range',
        "value":'1982-2023',
        "action_id": "update_data"},
        
        {"type": 'text',
        "label": 'Data Time (Week)',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'rangeW',
        "value":'1-52',
        "action_id": "update_data"},
        
        {"type": 'text',
        "label": 'Plot Size (width, height)',
        "options": [{"label":"VCI", "value":"VCI"},
                  {"label":"TCI", "value":"TCI"},
                  {"label":"VHI", "value":"VHI"}],
        "key":'pltsize',
        "value":'12, 8',
        "action_id": "update_data"}]

    controls = [{
            "type": "button",
            "label": "Download Current Data Table",
            "id": "load_data"
        },
        {
            "type": "hidden",
            "label": "Update all data",
            "id": "update_data"
        },]

    tabs = ["Table", "Plot"]

    outputs = [{
        "type": "table",
        "id": "Show_data",
        "control_id": "update_data",
        "tab": "Table",
        "on_page_load": True
    },
    {
        "type": "download",
        "id": "download_data",
        "control_id": "load_data",
        "tab": "Download",
        "on_page_load": False
    },
    {
        "type": 'plot',
        "id": 'plot',
        "control_id": 'update_data',
        "tab": 'Plot',
        "on_page_load": True
    },]

    def getData(self, params):
        ticker = params['ticker']
        drange = params['range']
        dwrange = params['rangeW']
        
        province_our_id = params['province']
        province_needed_id = find_needed_id_for_NOAA(int(province_our_id))
        
        npath = find_needed_path("NOAA_ID"+str(province_needed_id))
        
        df = pd.read_csv("Csv\\" + npath, index_col=None, header=1, names=headers)
        df['Area'] = province_our_id
        df = df.drop(df.loc[df['VHI'] == -1].index)
                
        drange = drange.split("-")
        dwrange = dwrange.split("-")
        
        cond_year = (df.Year>=int(drange[0])) & (df.Year<=int(drange[1]))
        cond_week = (df.Week>=int(dwrange[0])) & (df.Week<=int(dwrange[1]))
        
        list_of_things_to_view = ["Year", "Week", str(ticker), "Area"]
        
        return df.loc[cond_year & cond_week][list_of_things_to_view]
    
    def getPlot(self, params):
        ticker = params['ticker']
        pltsize = params['pltsize']
        df = self.getData(params)

        df_copy = df.copy()
        df_copy_val = df_copy[["Year", "Week"]].values

        for i in range(len(df_copy_val)):
            df_copy_val[i][1] = i+1

        df_copy[["Year", "Week"]] = df_copy_val

        width, height = int(pltsize.split(', ')[0]), int(pltsize.split(', ')[1])

        plt_obj = df_copy.plot(x="Week", y=str(ticker), figsize=(width, height), grid=True, style='.-', markerfacecolor='black')
        fig = plt_obj.get_figure()
        return fig

app1 = TheBestApp()
app1.launch(port=9093)
