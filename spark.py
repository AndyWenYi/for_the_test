from pyspark import pandas as ps
import pyspark
from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
import random
import json


# 文字轉換
def trans(zh_num):
  zh2digit_table = {'零': 0, '一': 1, '二': 2, '兩': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100, '千': 1000, '〇': 0, '○': 0, '○': 0, '０': 0, '１': 1, '２': 2, '３': 3, '４': 4, '５': 5, '６': 6, '７': 7, '８': 8, '９': 9, '壹': 1, '貳': 2, '參': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '拾': 10, '佰': 100, '仟': 1000, '萬': 10000, '億': 100000000}
  # 位數遞增，由高位開始取
  digit_num = 0
  # 結果
  result = 0
  # 暫時存儲的變量
  tmp = 0
  # 億的個數
  billion = 0
  while digit_num < len(zh_num):
    tmp_zh = zh_num[digit_num]
    tmp_num = zh2digit_table.get(tmp_zh, None)
    if tmp_num == 100000000:
        result = result + tmp
        result = result * tmp_num
        billion = billion * 100000000 + result
        result = 0
        tmp = 0
    elif tmp_num == 10000:
        result = result + tmp
        result = result * tmp_num
        tmp = 0
    elif tmp_num >= 10:
        if tmp == 0:
            tmp = 1
        result = result + tmp_num * tmp
        tmp = 0
    elif tmp_num is not None:
        tmp = tmp * 10 + tmp_num
    digit_num += 1
  result = result + tmp
  result = result + billion
  return result

# 讀取各個檔案並合併
df_a = ps.read_csv('A_lvr_land_A.csv')
df_b = ps.read_csv('B_lvr_land_A.csv')
df_e = ps.read_csv('E_lvr_land_A.csv')
df_f = ps.read_csv('F_lvr_land_A.csv')
df_h = ps.read_csv('H_lvr_land_A.csv')
big_df = df_a.append(df_b).append(df_e).append(df_f).append(df_h)

# 去做相對的條件篩選
ans = []
for ind, i in enumerate(big_df['建物型態'].to_numpy()): 
  try:
    # 先判斷是否為住宅大樓，並確認用途及樓層數
    if '住宅大樓' in i and big_df['主要用途'].to_numpy()[ind] != '住家用' and trans(big_df['總樓層數'].to_numpy()[ind][:-1]) >12:
      ans.append(ind)
  except:
    pass

# df_4為篩選結果
df_4 = big_df.iloc[ans]

# 選擇欲使用欄位，並將各縣市資料及分開處理
column_list = ['交易年月日','建物型態','鄉鎮市區']
df_5 = df_4[column_list]
tp1 = df_a[column_list]
tp1 = df_5.merge(tp1, how = 'inner')
tp2 = df_f[column_list]
tp2 = df_5.merge(tp2, how = 'inner')
yuan = df_h[column_list]
yuan = df_5.merge(yuan, how = 'inner')
chun = df_b[column_list]
chun = df_5.merge(chun, how = 'inner')
kao = df_e[column_list]
kao = df_5.merge(kao, how = 'inner')

# 更改各縣市交易年月日為西元日期
citys = [tp1, tp2, yuan, chun, kao]
for city in citys:
  timestamp = []
  for i in city['交易年月日'].to_list():
    timestamp.append(str(1911 + int(i[:3])) + '-' + i[3:5] + '-' + i[5:])
  city['交易年月日'] = timestamp
  city = ps.to_datetime(city['交易年月日'])

# 將資料打包成json檔案
city_chinese = ['台北市','新北市','桃園市','台中市','高雄市']
count = 0
ans = []

for times in range(1,3):
  for city in citys:
    randoms = []

    # 隨機選擇兩個不重複資料
    while len(randoms) < 2:
      randoms.append(random.randint(0,len(city)))
    random_city = city.iloc[randoms]
    time_slots = []

    # 將資料彙整成dictionary
    for i in range(len(randoms)):
      time_slots.append([{"date" : random_city.iloc[i]['交易年月日'],'events':[{'type':random_city.iloc[i]['建物型態'],'district':random_city.iloc[i]['鄉鎮市區']}]}])
      print([{"date" : random_city.iloc[i]['交易年月日'],'events':[{'type':random_city.iloc[i]['建物型態'],'district':random_city.iloc[i]['鄉鎮市區']}]}])
    city_info = {'city':city_chinese[count],'time_slots':time_slots}
    ans.append(city_info)
    count += 1

  # 將資料寫入json 檔案
  with open(f'result-part{times}.json','w') as f:
    json.dump(ans,f)
