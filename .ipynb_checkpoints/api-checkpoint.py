from flask import Flask, request, Response
import json
from itsdangerous import NoneAlgorithm
import pandas as pd
import glob

app = Flask(__name__)

# 搜尋檔案路徑
path ='./download/'
csv_files = glob.glob(path + "/*A.csv")
df_list = (pd.read_csv(file) for file in csv_files)

# 一次讀取全部檔案
big_df   = pd.concat(df_list, ignore_index=True)

# 數字轉換
def trans(num_str):
    # 判別中文字零到九
    han_list = ['零','一','二','三','四','五','六','七','八','九']
    # 判別單位
    unit_list = ['','','十','百','千']
    result = ''
    num_len = len(num_str)
    for i in range(num_len):
        num = int(num_str[i])
        if i != num_len - 1:
            if num != 0:
                result = result + han_list[num] + unit_list[num_len - i]
            else:
                if result[-1] == '零':
                    continue
                else:
                    result = result + '零'
        else:
            if num != 0:
                result += han_list[num]
    # 將一十六更改為十六
    if result[0] == '一' and num_len == 2:
        result = result[1:]
    return result
 

@app.route('/',methods=['Get'])
def get_data():

# 判斷是否需要搜尋街區
    if request.args.get('block') != None:
        block = request.args.get('block')
    else:
        block = None

# 判斷是否需要搜尋樓層，有的話也將樓層轉換為中文模式
    if request.args.get('floor') != None:
        floor = request.args.get('floor')
        floor = trans(str(floor))

    else:
        floor = None

#  判斷是否搜尋建物型態
    if request.args.get('type') != None:
        type = request.args.get('type')
    else:
        type = None
    
# 開始做條件篩選    
    if block != None and floor == None and type == None:
        small_df = big_df.query(f"鄉鎮市區=='{block}'")

    elif block != None and floor != None and type == None:
        small_df = big_df.query(f"鄉鎮市區=='{block}' and 總樓層數=='{floor}層'")

    elif block != None and floor == None and type != None:
        small_df = big_df.query(f"鄉鎮市區=='{block}' and 建物型態=='{type}'")

    elif block != None and floor != None and type != None:
        small_df = big_df.query(f"鄉鎮市區=='{block}' and 總樓層數=='{floor}層' and 建物型態=='{type}'")
    
    elif block == None and floor != None and type == None:
        small_df = big_df.query(f"總樓層數=='{floor}層'")
        
    elif block == None and floor != None and type != None:
        small_df = big_df.query(f"總樓層數=='{floor}層' and 建物型態=='{type}'")
        
    elif block == None and floor == None and type != None:
        small_df = big_df.query(f"建物型態=='{type}'")

# 將篩選結果整理成json 檔案並回傳
    ans = small_df.to_json(orient = 'index',force_ascii=False)
    return ans
        

if __name__ == "__main__":
    app.run(debug=True)