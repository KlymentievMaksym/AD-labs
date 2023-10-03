import urllib.request
import sys
import datetime
import os
import pandas as pd

def create_file_with_dataset_and_receive_its_path(i, date_and_time_time, text):
    path_for_file = r'Csv\NOAA_ID'+str(i)+'_'+date_and_time_time+'.csv'
    with open(path_for_file,'wb') as out:
        print("Started writing!")
        out.write(text.encode())
        print("Done writing!")
    return path_for_file

def find_needed_id_for_province_in_dict(dictionary, province, province_index_NOAA, dictionary_for_transfer):
    # print(f"Received name: {province}")
    for j in range(1, len(dictionary)+1):
        # print(f"{province} == {dictionary[j]}, {province == dictionary[j]}")
        if province == dictionary[j]:
            dictionary_for_transfer[j] = province_index_NOAA
            return j
    raise NameError("Can't find province")

print("VHI is started...")

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
dict_for_transfer = dict()
dict_for_df = dict()

for i in range(1,28):
    print(f"Creating NOAA with id {i}")
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?provinceID="+str(i)+"&country=UKR&yearlyTag=Weekly&type=Mean&TagCropland=land&year1=1982&year2=2023"
    vhi_url = urllib.request.urlopen(url)
    print("Started reading and adapting!")
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
    location_of_name_start = text.find(f"{i}: ")
    location_of_name_end = text.find("  from")
    name_of_province = text[location_of_name_start+3:location_of_name_end]
    needed_id = find_needed_id_for_province_in_dict(dict_for_our_id, name_of_province.strip(), i, dict_for_transfer)
    # dict_for_NOAA_id[i] = name_of_province.strip()
    now = datetime.datetime.now()
    date_and_time_time = now.strftime("%d-%m-%Y-%H-%M-%S")
    print("Done reading and adapting!")
    if os.path.exists('Csv\\'):
        path_for_file = create_file_with_dataset_and_receive_its_path(i, date_and_time_time, text)
    else:
        print("Directory 'Csv' is missing...")
        print("Creating directory 'Csv'...")
        os.mkdir('Csv\\')
        print("Done creating directory 'Csv'!")
        path_for_file = create_file_with_dataset_and_receive_its_path(i, date_and_time_time, text)
    print("Started reading csv!")
    df = pd.read_csv(path_for_file, index_col=None, header=1, names=headers)
    # print(df.head())
    print("Done reading csv!")
    print("Started deleting NANs and adding our area index...")
    df = df.drop(df.loc[df['VHI'] == -1].index)
    df['Area'] = i
    df["Area"].replace({i:needed_id}, inplace = True)
    dict_for_df[needed_id] = df
    print("Done deleting NANs and adding our area index!")
    print("Done!")
    print("VHI is downloaded...")

def VHI_area_year_extremum(dataframe, area_index, year):
    df = dataframe[(dataframe["Year"] == year)]['VHI'] # (dataframe["Area"] == area_index) & 
    print(df)
    print("Min:", df.min())
    print("Max:", df.max())
    main_menu()

def VHI_area_extreme_drought_by_percent(dataframe, area_index, percent):
    df_drought = dataframe[(dataframe.VHI <= 15)] #  & (df.VHI != -1)
    print(df_drought)
    main_menu()

def VHI_area_average_drought_by_percent(dataframe, area_index, percent):
    df_drought = dataframe[(dataframe.VHI <= 35)] #  & (df.VHI != -1)
    print(df_drought)
    main_menu()

def main_menu():
    request = input('What exactly do you want? ("h" for help): ')
    if request == "h":
        print("""
              "h" to get help
              "0" to exit from application
              "1" to view VHI by area and year, also to get extremums from it
              "2" to view VHI by area and when it was extreme drought by percent
              "3" to view VHI by area and when it was average drought by percent""")
        main_menu()
    elif request == "1":
        area_index = int(input('Enter id of province: '))
        year = int(input('Enter year: '))
        VHI_area_year_extremum(dict_for_df[area_index], area_index, year)
    elif request == "2":
        area_index = int(input('Enter id of province: '))
        percent = input('Enter percent: ')
        VHI_area_extreme_drought_by_percent(dict_for_df[area_index], area_index, percent)
    elif request == "3":
        area_index = int(input('Enter id of province: '))
        percent = input('Enter percent: ')
        VHI_area_average_drought_by_percent(dict_for_df[area_index], area_index, percent)
    elif request == "0":
        sys.exit()
    else:
        main_menu()
    # area_index = input()

main_menu()
# df_drought = df[(df.VHI <= 15) & (df.VHI != -1)]
# min_v = df[(df.Year.astype(str)==str(i)) & (df.VHI != -1)]['VHI'].min()


