import urllib.request
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


print("VHI is started...")

# http = urllib3.PoolManager()

# print(os.path.curdir)

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
    df = pd.read_csv(path_for_file, index_col=None, header=1)
    print(df.head())
    print("Done reading csv!")
    
    print("Done!")
    
# with open(url, "r")as cher:
#     txt = cher.read()

# print(txt)
# txt = txt.replace(",\n","\n")
# print(txt)
# with open(url, "w")as cher:
#     cher.write(txt)

# df = pd.read_csv(url, index_col='year', header=1)
# df.head()

print("VHI is downloaded...")
# print(type(df))
# print(df.info())

