import requests
import json
import time
from typing import Dict, List, Tuple, Optional

key = ""

def get_headers():
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US;en-q=0.5;zh-CN;q=0.5;zhq=0.7;jcq=0.6",
        "Authorization": key,
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "member.ls.land",
        "Origin": "https://game.ls.land",
        "Referer": "https://game.ls.land/",
        "Sec-Ch-Ua": '"Google Chrome";v="131", "Chromium";v="131", "Not A Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "Android",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }

def get_assets():
    url = "https://member.ls.land/g/assets/get"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def buy(material_no: int, num: int, price: float):
    url = "https://member.ls.land/g/shop/buy"
    payload = {
        "materialNo": material_no,
        "num": num,
        "price": price
    }
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def sell(material_no: int, num: int, price: float):
    url = "https://member.ls.land/g/shop/sell"
    payload = {
        "materialNo": material_no,
        "num": num,
        "price": price
    }
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def gather(landIndex: int):
    url = "https://member.ls.land/g/land/gather"
    payload = {
        "landIndex": landIndex,
    }
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def sow(invenIndex: int, landIndex: int):
    url = "https://member.ls.land/g/land/sow"
    payload = {
        "invenIndex": invenIndex,
        "landIndex": landIndex,
    }
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def list_bp():
    url = "https://member.ls.land/g/bp/list"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
def list_inventory():
    url = "https://member.ls.land/g/inven/list"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
def get_land_status():
    url = "https://member.ls.land/g/land/get"
    try:
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def check_bp() -> Optional[Dict]:
    """Check inventory for seeds and crops"""
    response = list_bp()
    if response and response.get('code') == 0:
        return response['data']
    return None

def check_inventory() -> Optional[Dict]:
    """Check inventory for seeds and crops"""
    response = list_inventory()
    if response and response.get('code') == 0:
        return response['data']
    return None

def find_seed_inventory_index(inventory: List[Dict]) -> Optional[int]:
    """Find the first slot with rice seeds (materialNo: 10001)"""
    for item in inventory:
        if item.get('materialNo') == 10002 and item.get('num', 0) > 0:
            return item['inventoryIndex']
    return None

def count_bp_seeds(bp: List[Dict]) -> Tuple[int, int]:
    """Count total rice seeds in bp"""
    for item in bp:
        if item.get('materialNo') == 10002:
            return item.get('materialNum', 0),item.get('backpackIndex', 0)
    return 0,0

def count_seeds(inventory: List[Dict]) -> int:
    """Count total rice seeds in inventory"""
    for item in inventory:
        if item.get('materialNo') == 10002:
            return item.get('num', 0)
    return 0


def count_rice(bp: List[Dict]) -> int:
    """Count total rice in inventory"""
    for item in bp:
        if item.get('materialNo') == 10102:
            return item.get('materialNum', 0)
    return 0

def calculate_seed_purchase_amount(marrow: float, price: float) -> int:
    """Calculate how many seeds to buy based on available marrow"""
    max_seeds = int(marrow / price)
    # Ensure we don't buy more than 6 seeds at a time
    return max_seeds

def handle_planting(land_index: int, seed_index: int):
    """Handle the planting process"""
    print(f"Planting seeds from slot {seed_index}")
    sow_result = sow(invenIndex=seed_index, landIndex=land_index)
    if not sow_result or sow_result.get('code') != 0:
        print("Failed to plant seeds")
        return False
    return True

def switch(bpIndex:int,invenIndex:int,switchType:int):
    url = "https://member.ls.land/g/bi/switch"
    payload = {
        "bpIndex": bpIndex,
        "invenIndex": invenIndex,
        "switchType":switchType
    }
    try:
        response = requests.post(url, headers=get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
def get_min_remain_time(land_data: List[Dict]) -> int:
    """获取所有种植的土地中最短的剩余时间"""
    remain_times = [land.get('remainTime', 0) for land in land_data if land.get('status') is True]
    return min(remain_times) if remain_times else 0

def all_lands_planted(land_data: List[Dict]) -> bool:
    """检查是否所有土地都已种植"""
    return all(land.get('status') is True for land in land_data)

def farm_loop():
    """Main farming loop"""
    seed_price = 3
    rice_price = 3.3

    while True:
        try:
            # Check assets first
            assets = get_assets()
            if not assets or assets.get('code') != 0:
                print("Failed to get assets")
                time.sleep(1800)
                continue
                
            marrow = assets['data']['marrow']
            print(f"Current marrow: {marrow}")
            
            # Check inventory and BP
            bp = check_bp()
            bp_seed_count, index = count_bp_seeds(bp)
            rice_count = count_rice(bp)

            if bp_seed_count > 0:
                switch(index, 1, 1)

            inventory = check_inventory()
            if not inventory:
                print("Failed to check inventory")
                time.sleep(1800)
                continue

            print(f"Current BP - Seeds: {bp_seed_count}, Rice: {rice_count}")
            seed_count = count_seeds(inventory)
            print(f"Current inventory - Seeds: {seed_count}")
            
            # Check land status
            land_status = get_land_status()
            if not land_status or land_status.get('code') != 0:
                print("Failed to check land status")
                time.sleep(1800)
                continue
            
            land_data = land_status['data']
            if not land_data:
                print("Could not find land data")
                time.sleep(1800)
                continue
            
            # 处理收获
            harvest_count = 0
            for land in land_data:
                land_index = land.get('landIndex')
                if land.get('status') is True:  # 土地上有作物
                    remain_time = land.get('remainTime', 0)
                    if remain_time <= 0:
                        print(f"Harvesting crops on land {land_index}")
                        gather_result = gather(landIndex=land_index)
                        if not gather_result or gather_result.get('code') != 0:
                            print(f"Failed to harvest land {land_index}")
                            continue
                        harvest_count += 1

            # 如果有收获，重新检查库存和土地状态
            if harvest_count > 0:
                bp = check_bp()
                rice_count = count_rice(bp)
                land_status = get_land_status()
                land_data = land_status['data']

            # 处理种植
            empty_lands = [land for land in land_data if land.get('status') is False]
            if empty_lands:
                if seed_count == 0:
                    # 如果没有种子，先卖出大米
                    if rice_count > 0:
                        print(f"Selling {rice_count} rice")
                        sell_result = sell(material_no=10102, num=rice_count, price=rice_price)
                        if not sell_result or sell_result.get('code') != 0:
                            print("Failed to sell rice")
                            time.sleep(1800)
                            continue
                    
                    # 计算并购买新种子
                    seeds_to_buy = calculate_seed_purchase_amount(marrow, seed_price)
                    if seeds_to_buy > 0:
                        print(f"Buying {seeds_to_buy} new seeds")
                        buy_result = buy(material_no=10002, num=seeds_to_buy, price=seed_price)
                        if not buy_result or buy_result.get('code') != 0:
                            print("Failed to buy seeds")
                            time.sleep(1800)
                            continue
                        
                        # 更新库存信息
                        inventory = check_inventory()
                        seed_count = count_seeds(inventory)

                # 在所有空地上种植
                for land in empty_lands:
                    if seed_count > 0:
                        land_index = land.get('landIndex')
                        seed_index = find_seed_inventory_index(inventory)
                        if seed_index:
                            print(f"Planting seeds on land {land_index}")
                            if handle_planting(land_index, seed_index):
                                print(f"Successfully planted seeds on land {land_index}")
                                seed_count -= 1
                                # 更新库存中的种子数量
                                for item in inventory:
                                    if item['inventoryIndex'] == seed_index:
                                        item['num'] = max(0, item['num'] - 1)
                            else:
                                print(f"Failed to plant seeds on land {land_index}")
                    else:
                        break

            # 检查是否所有土地都已种植
            land_status = get_land_status()
            land_data = land_status['data']
            if all_lands_planted(land_data):
                # 获取最短剩余时间
                min_time = get_min_remain_time(land_data)
                if min_time > 0:
                    print(f"All lands planted. Waiting for {min_time} seconds until next harvest...")
                    # 等待到最短剩余时间前10秒
                    sleep_time = max(min_time - 10, 0)
                    time.sleep(sleep_time)
                    continue
            
            # 如果还有空地或有需要收获的，短暂等待后继续循环
            time.sleep(10)
            
        except Exception as e:
            print(f"Error in farming loop: {e}")
            time.sleep(1800)

if __name__ == "__main__":
    print("Starting farming automation...")
    farm_loop()