import requests
import json
import os

url = 'https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json'

print("正在下载中国地图数据...")
response = requests.get(url)
data = response.json()

print(f"成功下载中国地图数据，包含 {len(data['features'])} 个省级行政区")

os.makedirs('data', exist_ok=True)

with open('data/china_provinces.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

print("已保存到 data/china_provinces.json")
