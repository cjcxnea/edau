import json
import os
import pandas as pd


DEFAULT_JSON_FILE_PATH = 'json/user-25(下).json'


def add_users_to_json(user_data_list, json_file_path=DEFAULT_JSON_FILE_PATH):
    """
    将用户数据批量添加到user-25(下).json文件中
    
    参数:
        user_data_list: 用户数据列表，每个元素是一个包含用户信息的字典
        json_file_path: user-25(下).json文件路径，默认为'json/user-25(下).json'
    
    返回:
        bool: 操作是否成功
    """
    try:
        if not os.path.exists(json_file_path):
            print(f"错误: 文件 {json_file_path} 不存在")
            return False
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'users' not in data:
            print("错误: user.json中缺少users字段")
            return False
        
        existing_users = data['users']
        
        for user_data in user_data_list:
            if 'No.' not in user_data:
                print("警告: 用户数据中缺少No.字段，跳过该用户")
                continue
            
            no_value = user_data['No.']
            
            existing_user = next((u for u in existing_users if u['No.'] == no_value), None)
            
            if existing_user:
                print(f"警告: 用户编号 {no_value} 已存在，将更新该用户信息")
                existing_user.update(user_data)
            else:
                existing_users.append(user_data)
                print(f"成功添加用户: {user_data.get('uname', '未知')}")
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n操作完成！当前共有 {len(existing_users)} 个用户")
        return True
        
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False


def export_users_to_csv(csv_file_path, json_file_path=DEFAULT_JSON_FILE_PATH, mode='append'):
    """
    将json/user-25(下).json中的用户信息导出到CSV文件中
    根据编号和姓名检查数据是否已存在，避免重复数据
    
    参数:
        csv_file_path: CSV文件路径
        json_file_path: user-25(下).json文件路径，默认为'json/user-25(下).json'
        mode: 导出模式，'append'为追加模式（默认），'overwrite'为覆盖模式
    
    返回:
        tuple: (成功导出的数量, 跳过的数量)
    """
    try:
        if not os.path.exists(json_file_path):
            print(f"错误: 文件 {json_file_path} 不存在")
            return (0, 0)
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'users' not in data:
            print("错误: user.json中缺少users字段")
            return (0, 0)
        
        users = data['users']
        
        if mode == 'overwrite':
            if os.path.exists(csv_file_path):
                print(f"覆盖模式：将删除 {csv_file_path} 的所有数据")
                os.remove(csv_file_path)
            existing_data = {}
        elif mode == 'append':
            existing_data = {}
            if os.path.exists(csv_file_path):
                try:
                    df_existing = pd.read_csv(csv_file_path)
                    for _, row in df_existing.iterrows():
                        key = (str(row.get('No.', '')), str(row.get('uname', '')))
                        existing_data[key] = True
                except Exception as e:
                    print(f"警告: 读取现有CSV文件失败 - {e}，将创建新文件")
        else:
            print(f"无效的模式: {mode}")
            return (0, 0)
        
        new_users = []
        skipped_count = 0
        
        for user in users:
            key = (str(user.get('No.', '')), str(user.get('uname', '')))
            if key in existing_data:
                skipped_count += 1
                print(f"跳过重复用户: {user.get('uname', '未知')} (编号: {user.get('No.', '')})")
            else:
                new_users.append(user)
        
        if new_users:
            df_new = pd.DataFrame(new_users)
            
            if mode == 'overwrite' or not os.path.exists(csv_file_path):
                df_new.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
            else:
                df_new.to_csv(csv_file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
            
            print(f"\n成功导出 {len(new_users)} 个用户到 {csv_file_path}")
        else:
            print(f"\n没有新用户需要导出")
        
        if skipped_count > 0:
            print(f"跳过 {skipped_count} 个重复用户")
        
        return (len(new_users), skipped_count)
        
    except Exception as e:
        print(f"错误: 导出CSV失败 - {e}")
        return (0, 0)


def export_users_to_excel(excel_file_path, json_file_path=DEFAULT_JSON_FILE_PATH, mode='append'):
    """
    将json/user-25(下).json中的用户信息导出到Excel文件中
    根据编号和姓名检查数据是否已存在，避免重复数据
    
    参数:
        excel_file_path: Excel文件路径
        json_file_path: user-25(下).json文件路径，默认为'json/user-25(下).json'
        mode: 导出模式，'append'为追加模式（默认），'overwrite'为覆盖模式
    
    返回:
        tuple: (成功导出的数量, 跳过的数量)
    """
    try:
        if not os.path.exists(json_file_path):
            print(f"错误: 文件 {json_file_path} 不存在")
            return (0, 0)
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'users' not in data:
            print("错误: user.json中缺少users字段")
            return (0, 0)
        
        users = data['users']
        
        if mode == 'overwrite':
            if os.path.exists(excel_file_path):
                print(f"覆盖模式：将删除 {excel_file_path} 的所有数据")
                os.remove(excel_file_path)
            existing_data = {}
        elif mode == 'append':
            existing_data = {}
            if os.path.exists(excel_file_path):
                try:
                    df_existing = pd.read_excel(excel_file_path)
                    for _, row in df_existing.iterrows():
                        key = (str(row.get('No.', '')), str(row.get('uname', '')))
                        existing_data[key] = True
                except Exception as e:
                    print(f"警告: 读取现有Excel文件失败 - {e}，将创建新文件")
        else:
            print(f"无效的模式: {mode}")
            return (0, 0)
        
        new_users = []
        skipped_count = 0
        
        for user in users:
            key = (str(user.get('No.', '')), str(user.get('uname', '')))
            if key in existing_data:
                skipped_count += 1
                print(f"跳过重复用户: {user.get('uname', '未知')} (编号: {user.get('No.', '')})")
            else:
                new_users.append(user)
        
        if new_users:
            df_new = pd.DataFrame(new_users)
            
            if mode == 'overwrite' or not os.path.exists(excel_file_path):
                df_new.to_excel(excel_file_path, index=False)
            else:
                with pd.ExcelWriter(excel_file_path, mode='a', engine='openpyxl') as writer:
                    df_new.to_excel(writer, index=False, header=False)
            
            print(f"\n成功导出 {len(new_users)} 个用户到 {excel_file_path}")
        else:
            print(f"\n没有新用户需要导出")
        
        if skipped_count > 0:
            print(f"跳过 {skipped_count} 个重复用户")
        
        return (len(new_users), skipped_count)
        
    except Exception as e:
        print(f"错误: 导出Excel失败 - {e}")
        return (0, 0)


def create_sample_users():
    """
    创建示例用户数据
    
    返回:
        list: 示例用户数据列表
    """
    sample_users = [
        {
            "No.": "5",
            "testSub": "全国大学英语四级考试(CET4)",
            "uname": "赵六",
            "idCard": "447812001072436227",
            "schoolName": "上海交通大学",
            "reportNum": "252144038004380",
            "examNum": "441430252112432",
            "totalScore": "510",
            "listening": "175",
            "reading": "185",
            "writing": "150",
            "speakingExamNum": "--",
            "speakingScore": "--"
        },
        {
            "No.": "6",
            "testSub": "全国大学英语六级考试(CET6)",
            "uname": "钱七",
            "idCard": "447812001072436228",
            "schoolName": "浙江大学",
            "reportNum": "252144038004381",
            "examNum": "441430252112433",
            "totalScore": "490",
            "listening": "165",
            "reading": "175",
            "writing": "150",
            "speakingExamNum": "--",
            "speakingScore": "--"
        }
    ]
    return sample_users


def read_users_from_excel(file_path):
    """
    从Excel文件中读取用户数据
    
    参数:
        file_path: Excel文件路径
    
    返回:
        list: 用户数据列表
    """
    try:
        df = pd.read_excel(file_path)
        
        required_fields = [
            'No.', 'testSub', 'uname', 'idCard', 'schoolName',
            'reportNum', 'examNum', 'totalScore', 'listening',
            'reading', 'writing', 'speakingExamNum', 'speakingScore'
        ]
        
        for field in required_fields:
            if field not in df.columns:
                print(f"警告: Excel文件中缺少字段 {field}")
        
        users = []
        for _, row in df.iterrows():
            user = {}
            for field in required_fields:
                user[field] = str(row.get(field, '--')) if field in df.columns else '--'
            users.append(user)
        
        return users
        
    except ImportError:
        print("错误: 需要安装pandas库。请运行: pip install pandas openpyxl")
        return []
    except Exception as e:
        print(f"错误: 读取Excel文件失败 - {e}")
        return []


def read_users_from_csv(file_path):
    """
    从CSV文件中读取用户数据
    
    参数:
        file_path: CSV文件路径
    
    返回:
        list: 用户数据列表
    """
    try:
        df = pd.read_csv(file_path)
        
        required_fields = [
            'No.', 'testSub', 'uname', 'idCard', 'schoolName',
            'reportNum', 'examNum', 'totalScore', 'listening',
            'reading', 'writing', 'speakingExamNum', 'speakingScore'
        ]
        
        for field in required_fields:
            if field not in df.columns:
                print(f"警告: CSV文件中缺少字段 {field}")
        
        users = []
        for _, row in df.iterrows():
            user = {}
            for field in required_fields:
                user[field] = str(row.get(field, '--')) if field in df.columns else '--'
            users.append(user)
        
        return users
        
    except ImportError:
        print("错误: 需要安装pandas库。请运行: pip install pandas")
        return []
    except Exception as e:
        print(f"错误: 读取CSV文件失败 - {e}")
        return []


def get_user_count(json_file_path=DEFAULT_JSON_FILE_PATH):
    """
    获取当前用户数量
    
    参数:
        json_file_path: user-25(下).json文件路径，默认为'json/user-25(下).json'
    
    返回:
        int: 用户数量
    """
    try:
        if not os.path.exists(json_file_path):
            return 0
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return len(data.get('users', []))
        
    except Exception as e:
        print(f"错误: 获取用户数量失败 - {e}")
        return 0


if __name__ == '__main__':
    print("=" * 50)
    print("用户数据管理工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 使用示例数据测试")
        print("2. 从Excel文件导入")
        print("3. 从CSV文件导入")
        print("4. 从JSON文件导入")
        print("5. 导出用户数据到CSV文件")
        print("6. 导出用户数据到Excel文件")
        print("7. 查看当前用户数量")
        print("0. 退出")
        
        choice = input("\n请输入选项 (0-7): ").strip()
        
        if choice == '0':
            print("再见！")
            break
            
        elif choice == '1':
            users = create_sample_users()
            print(f"\n将添加 {len(users)} 个示例用户")
            add_users_to_json(users)
            
        elif choice == '2':
            file_path = input("请输入Excel文件路径: ").strip()
            users = read_users_from_excel(file_path)
            if users:
                print(f"\n从Excel文件中读取到 {len(users)} 个用户")
                add_users_to_json(users)
                
        elif choice == '3':
            file_path = input("请输入CSV文件路径: ").strip()
            users = read_users_from_csv(file_path)
            if users:
                print(f"\n从CSV文件中读取到 {len(users)} 个用户")
                add_users_to_json(users)
                
        elif choice == '4':
            file_path = input("请输入JSON文件路径: ").strip()
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    users = data.get('users', [])
                    print(f"\n从JSON文件中读取到 {len(users)} 个用户")
                    add_users_to_json(users)
            except Exception as e:
                print(f"错误: 读取JSON文件失败 - {e}")
                
        elif choice == '5':
            csv_path = input("请输入CSV文件路径: ").strip()
            if not csv_path:
                csv_path = 'users.csv'
            
            print("\n请选择导出模式:")
            print("1. 追加模式（默认，保留现有数据）")
            print("2. 覆盖模式（删除现有数据）")
            mode_choice = input("请输入模式选择 (1-2, 默认1): ").strip()
            
            mode = 'append'
            if mode_choice == '2':
                mode = 'overwrite'
            
            print(f"\n正在导出用户数据到 {csv_path} (模式: {mode})...")
            exported, skipped = export_users_to_csv(csv_path, mode=mode)
            print(f"导出完成: 成功 {exported} 个, 跳过 {skipped} 个")
            
        elif choice == '6':
            excel_path = input("请输入Excel文件路径 (仅支持 .xlsx 格式！！！): ").strip()
            if not excel_path:
                excel_path = 'users.xlsx'
            
            print("\n请选择导出模式:")
            print("1. 追加模式（默认，保留现有数据）")
            print("2. 覆盖模式（删除现有数据）")
            mode_choice = input("请输入模式选择 (1-2, 默认1): ").strip()
            
            mode = 'append'
            if mode_choice == '2':
                mode = 'overwrite'
            
            print(f"\n正在导出用户数据到 {excel_path} (模式: {mode})...")
            exported, skipped = export_users_to_excel(excel_path, mode=mode)
            print(f"导出完成: 成功 {exported} 个, 跳过 {skipped} 个")
            
        elif choice == '7':
            count = get_user_count()
            print(f"\n当前共有 {count} 个用户")
            
        else:
            print("无效的选项")
