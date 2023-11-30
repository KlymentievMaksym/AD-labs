import urllib.request
import sys
import datetime
import os
import pandas as pd

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

def create_file_with_dataset_and_receive_its_path(i, date_and_time_time, text):
    path_for_file = r'Csv\NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv'
    with open(path_for_file,'wb') as out:
        print("Started writing!")
        out.write(text.encode())
        print("Done writing!")
    return path_for_file

def find_needed_id_from_NOAA(our_id):
    for id in dict_for_transfer:
        if id == our_id:
            return dict_for_transfer[id]

# dict_for_NOAA_id = dict()
headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
dict_for_our_id = {
    1:"Vinnytsya",
    2:"Volyn",
    3:"Dnipropetrovsk",
    4:"Donetsk",
    5:"Zhytomyr",
    6:"Transcarpathia",
    7:"Zaporizhzhya",
    8:"Ivano-Frankivsk",
    9:"Kiev",
    10:"Kirovohrad",
    11:"Luhansk",
    12:"Lviv",
    13:"Mykolayiv",
    14:"Odessa",
    15:"Poltava",
    16:"Rivne",
    17:"Sumy",
    18:"Ternopil",
    19:"Kharkiv",
    20:"Kherson",
    21:"Khmelnytskyy",
    22:"Cherkasy",
    23:"Chernihiv",
    24:"Chernivtsi",
    25:"Crimea",
    26:"Kiev City",
    27:"Sevastopol"
    }

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

# dict_for_transfer = dict()
dict_for_df = dict()
    
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
            path_for_file = create_file_with_dataset_and_receive_its_path(i, date_and_time_time, text)
        else:
            print("\nFile already exists\n")
    read_VHI_dataset()


def read_VHI_dataset():
    for npath in os.listdir("Csv\\"):
        # print("Started reading csv!")   
        df = pd.read_csv("Csv\\" + npath, index_col=None, header=1, names=headers)
        # print("Done reading csv!")
        j = int(npath[(npath.find("ID")+2):(npath.find("ID")+4)].replace("_", ""))
        # print("Started deleting NANs and adding our area index...")
        df = df.drop(df.loc[df['VHI'] == -1].index)
        needed_id = find_needed_id_from_NOAA(j)
        df['Area'] = needed_id 
        dict_for_df[needed_id] = df
        # print("Done deleting NANs and adding our area index!")
    print("Done!")
    # print("VHI is downloaded...")

# def receive_list_of_csv():   
#     # path = os.path.abspath("Csv\\")
#     # os.chroot()
#     path = os.getcwd()
#     print(path)
#     list_of_csv = os.listdir(path)
#     return list_of_csv

def get_dict_for_our_id():
    return dict_for_our_id

def get_dict_for_transfer():
    return dict_for_transfer

def get_dict_for_df():
    return dict_for_df

def VHI_area_year_extremum(dataframe, year): # , area_index
    df = dataframe[(dataframe["Year"] == year)][['Year', 'Week', 'VHI', 'Area']] # (dataframe["Area"] == area_index) & 
    print(df.to_string(index=False))
    print("Min:", df['VHI'].min())
    print("Max:", df['VHI'].max())
    main_menu()

def VHI_area_extreme_drought_by_percent(dataframe): # , percent, area_index
    df_drought = dataframe[(dataframe.VHI <= 15)] #  & (df.VHI != -1)
    print(df_drought[['Year', 'Week', 'VHI', 'Area']].to_string(index=False))
    main_menu()

def VHI_area_average_drought_by_percent(dataframe): # , percent, area_index
    df_drought = dataframe[(dataframe.VHI <= 35)] #  & (df.VHI != -1)
    print(df_drought[['Year', 'Week', 'VHI', 'Area']].to_string(index=False))
    main_menu()

def VHI_data(dataframe, float_number, difference):
    diff = ["<", ">", "<=", ">="]
    try:
        float_number = float(float_number)
    except ValueError:
        float_number = float_number.split()
    if difference in diff and type(float_number) == float:
        if difference == "<":
            df = dataframe[dataframe.VHI < float_number]
        if difference == ">":
            df = dataframe[dataframe.VHI > float_number]
        if difference == "<=":
            df = dataframe[dataframe.VHI <= float_number]
        if difference == ">=":
            df = dataframe[dataframe.VHI >= float_number]
    elif difference == "" and type(float_number) == list:
        int1 = float(float_number[0])
        int2 = float(float_number[1])
        df = dataframe[(dataframe.VHI >= int1) & (dataframe.VHI <= int2)]
    else:
        print("Operation was unsuccesful!")
        df = dataframe
    print(df[['Year', 'Week', 'VHI', 'Area']].to_string(index=False))
    main_menu()

def main_menu():
    request = input('\nWhat exactly do you want? ("h" for help): ')
    if request == "h":
        print("""
              "h" to get help
              "0" to exit from application
              "1" to view VHI by area and year, also to get extremums from it
              "2" to view VHI by area and when it was extreme drought
              "3" to view VHI by area and when it was average drought
              "4" to view VHI in diffences (like VHI > 10.5 or 50 <= VHI <= 100)
              "5" to view all csv files
              "6" to delete all csv files
              "7" to reload csv files""")
        main_menu()
    elif request == "1":
        area_index = int(input('Enter id of province: '))
        while area_index > 27 or area_index < 1:
            area_index = int(input('Enter id of province: '))
        year = int(input('Enter year: '))
        while year > 2023 or year < 1982:
            year = int(input('Enter year: '))
        print(dict_for_our_id[area_index])
        VHI_area_year_extremum(dict_for_df[area_index], year) # , area_index
    elif request == "2":
        area_index = int(input('Enter id of province: '))
        while area_index > 27 or area_index < 1:
            area_index = int(input('Enter id of province: '))
        print(dict_for_our_id[area_index])
        # percent = input('Enter percent: ')
        VHI_area_extreme_drought_by_percent(dict_for_df[area_index]) # , percent, area_index
    elif request == "3":
         area_index = int(input('Enter id of province: '))
         while area_index > 27 or area_index < 1:
             area_index = int(input('Enter id of province: '))
         # percent = input('Enter percent: ')
         print(dict_for_our_id[area_index])
         VHI_area_average_drought_by_percent(dict_for_df[area_index]) # , percent, area_index
    elif request == "4":
        area_index = int(input('Enter id of province: '))
        while area_index > 27 or area_index < 1:
            area_index = int(input('Enter id of province: '))
        number_or_list_of_2_numbers = input('Enter number or 2 numbers by space: ')
        diff = input('Enter "<", ">", "<=", ">=" or leave empty: ')
        print(dict_for_our_id[area_index])
        VHI_data(dict_for_df[area_index], number_or_list_of_2_numbers, diff)
    elif request == "5":
        list_to_show = os.listdir("Csv")
        print(*list_to_show, sep="\n")
        main_menu()
    elif request == "6":
        for file_name in os.listdir("Csv"):
            os.remove("Csv\\"+file_name)
        print("Done!")
        main_menu()
    elif request == "7":
        create_VHI_dataset()
        main_menu()
    elif request == "0":
        sys.exit()
    else:
        main_menu()

if __name__ == "__main__":
    check = input("Wanna download files? (0-False, 1-True): ")
    if check == "1":
        create_VHI_dataset()
    else:
        try:
            read_VHI_dataset()
        except FileNotFoundError:
            create_VHI_dataset()
    main_menu()
