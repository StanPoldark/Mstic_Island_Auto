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
        if item.get('materialNo') == 10001 and item.get('num', 0) > 0:
            return item['inventoryIndex']
    return None

def count_bp_seeds(bp: List[Dict]) -> Tuple[int, int]:
    """Count total rice seeds in bp"""
    for item in bp:
        if item.get('materialNo') == 10001:
            return item.get('materialNum', 0),item.get('backpackIndex', 0)
    return 0,0

def count_seeds(inventory: List[Dict]) -> int:
    """Count total rice seeds in inventory"""
    for item in inventory:
        if item.get('materialNo') == 10001:
            return item.get('num', 0)
    return 0


def count_rice(bp: List[Dict]) -> int:
    """Count total rice in inventory"""
    for item in bp:
        if item.get('materialNo') == 10101:
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
    
def farm_loop():
    """Main farming loop"""
    land_index = 1  # Using first land plot
    seed_price = 0.8
    rice_price = 0.87
    
    while True:
        try:
            # Check assets first
            assets = get_assets()
            if not assets or assets.get('code') != 0:
                print("Failed to get assets")
                time.sleep(600)
                continue
                
            marrow = assets['data']['marrow']
            print(f"Current marrow: {marrow}")
            
            # Check inventory

            
            bp = check_bp()

            bp_seed_count, index = count_bp_seeds(bp)
            rice_count = count_rice(bp)

            if bp_seed_count > 0:
                switch(index,1,1)

            inventory = check_inventory()

            if not inventory:
                print("Failed to check inventory")
                time.sleep(600)
                continue

            print(f"Current BP - Seeds: {bp_seed_count}, Rice: {rice_count}")

            seed_count = count_seeds(inventory)
            print(f"Current inventory - Seeds: {seed_count}")
            
            # Check land status
            land_status = get_land_status()
            if not land_status or land_status.get('code') != 0:
                print("Failed to check land status")
                time.sleep(600)
                continue
            
            land_data = land_status['data']
            current_land = next((land for land in land_data if land['landIndex'] == land_index), None)
            
            if not current_land:
                print(f"Could not find land with index {land_index}")
                time.sleep(600)
                continue
            
            if current_land.get('status') is False:  # Land is empty
                if seed_count > 0:
                    # Find seed inventory slot and plant
                    seed_index = find_seed_inventory_index(inventory)
                    if seed_index and handle_planting(land_index, seed_index):
                        print("Successfully planted seeds")
                    else:
                        print("Failed to plant seeds")
                else:
                    # Sell rice if we have any
                    if rice_count > 0:
                        print(f"Selling {rice_count} rice")
                        sell_result = sell(material_no=10101, num=rice_count, price=rice_price)
                        if not sell_result or sell_result.get('code') != 0:
                            print("Failed to sell rice")
                            time.sleep(600)
                            continue
                    
                    # Calculate and buy new seeds based on available marrow
                    seeds_to_buy = calculate_seed_purchase_amount(marrow, seed_price)
                    if seeds_to_buy > 0:
                        print(f"Buying {seeds_to_buy} new seeds")
                        buy_result = buy(material_no=10001, num=seeds_to_buy, price=seed_price)
                        if not buy_result or buy_result.get('code') != 0:
                            print("Failed to buy seeds")
                            time.sleep(600)
                            continue
            else:  # Land has plants
                remain_time = current_land.get('remainTime', 0)
                if remain_time <= 0:
                    # Harvest
                    print("Harvesting crops")
                    gather_result = gather(landIndex=land_index)
                    if not gather_result or gather_result.get('code') != 0:
                        print("Failed to harvest")
                        time.sleep(600)
                        continue
                else:
                    print(f"Waiting for growth... Remaining time: {remain_time} seconds")
                    # Wait for a portion of the remaining time before checking again
                    time.sleep(min(remain_time, 600))
                    continue
            
            time.sleep(10)  # Short delay between cycles
            
        except Exception as e:
            print(f"Error in farming loop: {e}")
            time.sleep(600)

if __name__ == "__main__":
    print("Starting farming automation...")
    farm_loop()