import requests
from bs4 import BeautifulSoup
import json

url = "https://id.wikipedia.org/wiki/Kabinet_Merah_Putih"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def get_first_paragraph(person_url):
    try:
        person_response = requests.get(f"https://id.wikipedia.org{person_url}")
        person_soup = BeautifulSoup(person_response.text, "html.parser")
    
        paragraph = person_soup.find("p")
        return paragraph.get_text().strip() if paragraph else None
    except Exception as e:
        print(f"Error fetching {person_url}: {e}")
        return None

def get_high_res_image_url(thumb_url):
    if "/thumb/" in thumb_url:
    
        parts = thumb_url.split("/thumb/")
        base_url = parts[0]
    
        filename = parts[1].split("/")[:-1]
    
        return f"{base_url}/{'/'.join(filename)}"
    return thumb_url

cabinets = []
merged_cabinets = []
tables = soup.find_all("table", class_="wikitable")

for table in tables:
    cabinet_name = table.find_previous("h3").get_text().strip() if table.find_previous("h3") else "Unknown Cabinet"
    cabinet_members = []
    
    rows = table.find_all("tr")[1:] 
    for row in rows:
        columns = row.find_all("td")
        if len(columns) < 7:
            continue
    
        position = columns[1].get_text().strip()

        photo_img = columns[2].find("img")
        photo_url = f"https:{photo_img['src']}" if photo_img else None
        photo_high_res = get_high_res_image_url(photo_url)

        name = columns[3].get_text().strip()

        profile_tag = columns[3].find("a")
        profile_url = profile_tag['href'] if profile_tag else None

        party = columns[7].get_text().strip()
        party = "INDEPENDEN" if party == "Nonpartai" else party.upper()

    
        first_paragraph = get_first_paragraph(profile_url) if profile_url else None

    
        cabinet_members.append({
            "name": name,
            "picUrl": photo_high_res,
            "title": position,
            "party": party,
            "summary": first_paragraph,
            "source": f"https://id.wikipedia.org{profile_url}" if profile_url else None,
        })


    if (len(cabinet_members) > 0):
        cabinets.append({
            "cabinet_name": cabinet_name,
            "members": cabinet_members
        })

        merged_cabinets += cabinet_members



with open("cabinets.json", "w", encoding="utf-8") as f:
    json.dump(merged_cabinets, f, ensure_ascii=False, indent=4)

print("Data saved to cabinets.json")
