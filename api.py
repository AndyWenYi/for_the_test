from flask import Flask, request, Response
import json
from itsdangerous import NoneAlgorithm
import pandas as pd
import glob

app = Flask(__name__)

path ='./download/'
csv_files = glob.glob(path + "/*A.csv")
df_list = (pd.read_csv(file) for file in csv_files)
big_df   = pd.concat(df_list, ignore_index=True)


def trans(num_str):
    han_list = ['零','一','二','三','四','五','六','七','八','九']
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
        if result[0] == '一' and len(result) != 1:
            result = result[1:]
    return result
 

@app.route('/',methods=['Get'])
def get_data():

    if request.args.get('block') != None:
        block = request.args.get('block')
    else:
        block = None

    if request.args.get('floor') != None:
        floor = request.args.get('floor')
        floor = trans(str(floor))

    else:
        floor = None

    if request.args.get('type') != None:
        type = request.args.get('type')
    else:
        type = None
    
    
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

    ans = small_df.to_json(orient = 'index',force_ascii=False)
    return ans
        

if __name__ == "__main__":
    app.run(debug=True)