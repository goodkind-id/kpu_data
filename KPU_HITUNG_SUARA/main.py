import requests
import os
import json

def get_list_provinces():
    try:
        url = f"https://sirekappilkada-obj-data.kpu.go.id/wilayah/pilkada/pkwkp/0.json"
        response = requests.get(url)
        # response = requests.get("https://pilkada2020.kpu.go.id/info/ref/wilayah/0.json")
        data = response.json()
        return data
    except:
        return []

def get_list_cities(province_code):
    try:
        url = f"https://sirekappilkada-obj-data.kpu.go.id/wilayah/pilkada/pkwkp/{province_code}.json"
        # url = f"https://pilkada2020.kpu.go.id/info/ref/wilayah/{province_code}.json"
        response = requests.get(url)
        data = response.json()
        return data
    except:
        return []

def store_regions():
    provinces = get_list_provinces()

    for p in provinces:
        code = p['kode']

        cities = get_list_cities(code)
        with open(f"wilayah/{code}.json", "w") as f:
            json.dump(cities, f, indent=4)


    with open("wilayah/0.json", "w") as f:
        json.dump(provinces, f, indent=4)

def get_regions():
    try:
        provinces = []
        with open("wilayah/0.json", "r") as f:
            provinces = json.load(f)

        for p in provinces:
            code = p['kode']

            with open(f"wilayah/{code}.json", "r") as f:
                p['cities'] = json.load(f)

        return provinces
    except:
        return []


def get_result_hitung_suara(path):
    try:
        url = f"https://pilkada2020.kpu.go.id/{path}"

        response = requests.get(url)
        data = response.json()
        return data
    except:
        return []

def store_result_hitung_suara(level = "p"):
    regions = get_regions()

    for r in regions:
        for c in r['cities']:
            province_code = r['kode']
            city_code = c['kode']
            
            if level.lower() == "c":
                folder_path = f"info/hhc/pkwkk/{province_code}"
            else:
                folder_path = f"info/hr/pkwkp/{province_code}"

            file_path = f"/{city_code}.json"

            path = folder_path + file_path

            data = get_result_hitung_suara(path)

            if not os.path.exists(f"result/{folder_path}"):
                os.makedirs(f"result/{folder_path}")

            with open(f"result/{path}", "w") as f:
                json.dump(data, f, indent=4)

def main():
    # store_regions()
    level = input("Input level [P (provinsi), c (kab/kota)]: ")
    store_result_hitung_suara(level)

if __name__ == "__main__":
  main()