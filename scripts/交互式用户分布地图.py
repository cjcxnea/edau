#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式用户分布地图生成脚本
功能：使用folium库创建交互式中国地图，展示用户在不同省份的分布情况
"""

import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import Search
import json
from pathlib import Path

# ==================== 配置参数 ====================

# 数据文件路径配置
DATA_DIR = Path("D:/Code Files/四六级/学习部署/data")
CSV_FILE = DATA_DIR / "sample_users.csv"
MAP_FILE = DATA_DIR / "china_provinces.json"
OUTPUT_FILE = DATA_DIR / "interactive_user_map.html"

# 地图配置参数
MAP_CENTER = [35, 105]  # 地图初始中心位置（中国中部）
MAP_ZOOM = 4            # 初始缩放级别
MAP_TILES = "OpenStreetMap"  # 底图类型

# 省份编码映射字典（身份证前两位对应省份）
PROVINCE_CODE_MAP = {
    '11': '北京市', '12': '天津市', '13': '河北省', '14': '山西省', '15': '内蒙古自治区',
    '21': '辽宁省', '22': '吉林省', '23': '黑龙江省',
    '31': '上海市', '32': '江苏省', '33': '浙江省', '34': '安徽省', '35': '福建省', '36': '江西省', '37': '山东省',
    '41': '河南省', '42': '湖北省', '43': '湖南省', '44': '广东省', '45': '广西壮族自治区', '46': '海南省',
    '50': '重庆市', '51': '四川省', '52': '贵州省', '53': '云南省', '54': '西藏自治区',
    '61': '陕西省', '62': '甘肃省', '63': '青海省', '64': '宁夏回族自治区', '65': '新疆维吾尔自治区',
    '71': '台湾省', '81': '香港特别行政区', '82': '澳门特别行政区'
}

# ==================== 数据加载和预处理 ====================

def load_user_data():
    """加载用户数据并统计省份分布"""
    print("正在加载用户数据...")
    
    try:
        # 读取CSV文件
        data = pd.read_csv(CSV_FILE)
        print(f"成功加载用户数据，共 {len(data)} 条记录")
        
        # 根据身份证号前两位获取省份
        def get_province(id_card):
            code = str(id_card)[:2]
            return PROVINCE_CODE_MAP.get(code, '未知')
        
        # 添加省份列
        data['province'] = data['idCard'].apply(get_province)
        
        # 统计省份分布
        province_counts = data['province'].value_counts()
        print(f"用户分布在 {len(province_counts)} 个省份")
        
        # 创建完整的省份用户数量字典（包括0用户的省份）
        all_provinces = list(PROVINCE_CODE_MAP.values())
        province_user_count = {province: 0 for province in all_provinces}
        
        # 更新有用户的省份数量
        for province, count in province_counts.items():
            if province in province_user_count:
                province_user_count[province] = count
        
        # 转换为DataFrame
        province_df = pd.DataFrame([
            {'province': province, 'user_count': count}
            for province, count in province_user_count.items()
        ])
        
        return province_df
        
    except Exception as e:
        print(f"加载用户数据失败: {e}")
        return None

def load_map_data():
    """加载地图数据"""
    print("正在加载地图数据...")
    
    try:
        if not MAP_FILE.exists():
            print(f"地图文件不存在: {MAP_FILE}")
            return None
        
        china_map = gpd.read_file(MAP_FILE)
        print(f"成功加载地图数据，包含 {len(china_map)} 个省级行政区")
        print(f"地图数据字段: {list(china_map.columns)}")
        
        return china_map
        
    except Exception as e:
        print(f"加载地图数据失败: {e}")
        return None

# ==================== 交互式地图功能 ====================

def create_interactive_map(province_df, china_map):
    """创建交互式地图"""
    print("正在创建交互式地图...")
    
    # 合并用户数据到地图数据
    china_map = china_map.merge(
        province_df,
        left_on='name',
        right_on='province',
        how='left'
    )
    
    # 填充缺失值为0
    china_map['user_count'] = china_map['user_count'].fillna(0)
    
    # 创建交互式地图对象
    m = folium.Map(
        location=MAP_CENTER,
        zoom_start=MAP_ZOOM,
        tiles=MAP_TILES
    )
    
    # 颜色映射函数：根据用户数量返回对应的蓝色渐变颜色
    def get_color(user_count):
        """根据用户数量返回对应的蓝色渐变颜色"""
        if user_count == 0:
            return '#f7fbff'  # 最浅蓝色（无用户）
        elif user_count <= 1:
            return '#deebf7'  # 浅蓝色（1个用户）
        elif user_count <= 2:
            return '#c6dbef'  # 中等浅蓝色（2个用户）
        elif user_count <= 3:
            return '#9ecae1'  # 中等蓝色（3个用户）
        else:
            return '#3182bd'  # 深蓝色（4个及以上用户）
    
    # 样式函数：设置每个省份的填充颜色和边框样式
    def style_function(feature):
        """设置省份样式"""
        user_count = feature['properties'].get('user_count', 0)
        return {
            'fillColor': get_color(user_count),  # 填充颜色
            'color': 'black',                    # 边框颜色
            'weight': 1,                         # 边框宽度
            'fillOpacity': 0.7,                  # 填充透明度
            'opacity': 0.8                       # 边框透明度
        }
    
    # 悬停高亮函数：鼠标悬停时高亮显示
    def highlight_function(feature):
        """悬停高亮效果"""
        return {
            'weight': 3,           # 悬停时边框加粗
            'color': 'red',        # 悬停时边框变红色
            'fillOpacity': 0.9     # 悬停时填充更不透明
        }
    
    # 将GeoDataFrame转换为GeoJSON格式（使用更安全的方法）
    # 避免numpy数组无法被JSON序列化的问题
    try:
        # 方法1：尝试直接转换
        geojson_data = china_map.to_json(na='null', show_bbox=True)
    except TypeError:
        # 方法2：如果方法1失败，使用更安全的转换方法
        print("使用安全转换方法处理GeoJSON数据...")
        
        # 创建一个简化的GeoDataFrame，只包含必要的字段
        simplified_map = china_map[['name', 'user_count', 'geometry']].copy()
        
        # 确保所有数据都是可序列化的类型
        simplified_map['name'] = simplified_map['name'].astype(str)
        simplified_map['user_count'] = simplified_map['user_count'].astype(int)
        
        # 使用更安全的JSON转换方法
        geojson_data = simplified_map.to_json(na='null', show_bbox=True)
    
    # 添加GeoJSON图层到地图
    folium.GeoJson(
        geojson_data,
        name='用户分布',
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'user_count'],
            aliases=['省份:', '用户数量:'],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800
        ),
        popup=folium.GeoJsonPopup(
            fields=['name', 'user_count'],
            aliases=['省份:', '用户数量:'],
            localize=True,
            labels=True
        )
    ).add_to(m)
    
    # 添加搜索功能
    search = Search(
        layer=folium.GeoJson(geojson_data),
        search_label='name',
        placeholder='搜索省份...',
        position='topleft'
    ).add_to(m)
    
    # 添加图例
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 220px; height: 170px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px;">
    <p style="font-weight: bold; margin-bottom: 10px;">用户数量图例</p>
    <p><i style="background:#f7fbff; width:20px; height:20px; display:inline-block; border:1px solid #ccc;"></i> 0 用户</p>
    <p><i style="background:#deebf7; width:20px; height:20px; display:inline-block; border:1px solid #ccc;"></i> 1 用户</p>
    <p><i style="background:#c6dbef; width:20px; height:20px; display:inline-block; border:1px solid #ccc;"></i> 2 用户</p>
    <p><i style="background:#9ecae1; width:20px; height:20px; display:inline-block; border:1px solid #ccc;"></i> 3 用户</p>
    <p><i style="background:#3182bd; width:20px; height:20px; display:inline-block; border:1px solid #ccc;"></i> 4+ 用户</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # 添加图层控制
    folium.LayerControl().add_to(m)
    
    return m

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("=" * 50)
    print("交互式用户分布地图生成器")
    print("=" * 50)
    
    # 检查数据目录
    if not DATA_DIR.exists():
        print(f"数据目录不存在: {DATA_DIR}")
        return
    
    # 加载用户数据
    province_df = load_user_data()
    if province_df is None:
        return
    
    # 加载地图数据
    china_map = load_map_data()
    if china_map is None:
        return
    
    # 创建交互式地图
    interactive_map = create_interactive_map(province_df, china_map)
    
    # 保存地图
    try:
        interactive_map.save(str(OUTPUT_FILE))
        print(f"✅ 交互式地图已成功保存到: {OUTPUT_FILE}")
        print("📊 地图功能说明:")
        print("   • 鼠标悬停: 查看省份信息和用户数量")
        print("   • 点击省份: 显示详细弹窗信息")
        print("   • 搜索功能: 左上角搜索框可搜索省份")
        print("   • 图层控制: 右上角可切换底图")
        print("   • 缩放拖拽: 支持鼠标滚轮缩放和拖拽移动")
        print("\n🌐 在浏览器中打开HTML文件即可查看交互式地图")
        
    except Exception as e:
        print(f"❌ 保存地图失败: {e}")

if __name__ == "__main__":
    main()