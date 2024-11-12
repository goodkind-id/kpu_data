import urllib.parse
from bs4 import BeautifulSoup
import json
import requests
import urllib
import argparse
from PIL import Image
import os
from io import BytesIO
import re

def fetch(url, body):
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Opera\";v=\"112\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "referrer": "https://infopemilu.kpu.go.id/Pemilihan/Pasangan_calon",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "mode": "cors"
    }

    #body = "id_wilayah=d0da09053e6a20c1bf89edd59f656aeedb47f97cb04dd2e4820d98bd05b04f9eb15ef9437c183e84f9e135f8a4e3eb65034aff8d67233c4774913e5d804efe1d14mTW0Rd%2BNFfaSNKA%2FKb6bfhtnRRFxQmqjQIQWfMEXI%3D"
    
    response = requests.post(url, headers=headers, data=body)

    return response

def fetch_image(url_image):
    # Download the image
    response = requests.get(url_image)
    if response.status_code == 200:
        # Parse the URL to get the path
        parsed_url = urllib.parse.urlparse(url_image)

        # Get the path without the query string
        path_without_query = parsed_url.path.lstrip("/")

        # Create the full directory structure
        base_dir = os.path.join('data/foto', os.path.dirname(path_without_query))
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        # Get the filename from the URL and the original extension
        original_filename = os.path.basename(path_without_query)
        original_extension = os.path.splitext(original_filename)[1].lower()

        if args.webp:

            # Only convert if the original file is not in WebP format
            if original_extension != '.webp':
                # Load the image using PIL
                img = Image.open(BytesIO(response.content))

                # Replace the original extension with .webp for the output file
                webp_filename = os.path.splitext(original_filename)[0] + '.webp'

                # Path to save the converted image (mimicking the original URI structure)
                output_path = os.path.join(base_dir, webp_filename)

                # Convert and save the image as WebP
                img.save(output_path, 'webp')
                print(f"Image successfully saved as WebP at {output_path}")
            else:
                print(f"The image is already in WebP format: {original_filename}")
        else:
            # Load the image using PIL
            img = Image.open(BytesIO(response.content))

            # Path to save the converted image (mimicking the original URI structure)
            output_path = os.path.join(base_dir, original_filename)

            # Convert and save the image as WebP
            img.save(output_path)

            print(f"Get Image with original format: {original_filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
def parse_html_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    pairs = []
    candidates = []

    # Find pairs blocks
    pair_blocks = soup.find_all('div', class_='card p-3 h-100')

    for pair_block in pair_blocks:
        pair = {}
        pair['candidates'] = []
        pair['parties'] = []
        pair['visi_misi'] = {
            'visi' : None,
            'misi' : None
        }


        # Find all candidate blocks
        candidate_blocks = pair_block.find_all('div', class_='col-sm-12')

        for block in candidate_blocks:
            candidate = {}

            # Extract candidate type (CALON or WAKIL CALON)
            candidate_type = block.find('strong').get_text().strip()

            # Extract image URL and name
            image_tag = block.find('img')
            candidate['image_url'] = image_tag['src'] if image_tag else None
            candidate['name'] = image_tag['alt'] if image_tag else None

            calon_id = 0

            if candidate['image_url'] is not None:
                if args.get_foto:
                    fetch_image(candidate['image_url'])

                match = re.search(r'calon/(\d+)/', urllib.parse.urlparse(candidate['image_url']).path.lstrip("/"))
                if match:
                    calon_id = match.group(1)
                    
            modal_id = f"modalCakada{calon_id}" if candidate_type == 'CALON' else f"modalCawakeda{calon_id}"

            personal_block = soup.find('div', id=modal_id)

            if personal_block is not None:
                personal_info = personal_block.find_all('p')
                details = {}

                for p in personal_info:
                    strong_text = p.find('strong').get_text().replace(':', '').strip()
                    value = p.get_text().replace(strong_text + ':', '').strip()
                    details[strong_text] = value

                candidate['details'] = details

                # Get job information from <li> under "Pekerjaan"
                pekerjaan_section = personal_block.find('p', string='Pekerjaan:')
                if pekerjaan_section:
                    pekerjaan_list = pekerjaan_section.find_next('ul').find_all('li')
                    candidate['Pekerjaan'] = [li.text.strip() for li in pekerjaan_list if li.text.strip()]

                # Get legal status information from <li> under "Status Hukum"
                hukum_section = personal_block.find('p', string='Status Hukum:')
                if hukum_section:
                    hukum_list = hukum_section.find_next('ul').find_all('li')
                    candidate['Status Hukum'] = [li.text.strip() for li in hukum_list if li.text.strip()]

                get_info(candidate, personal_block)

            pair['candidates'].append({
                'type': candidate_type,
                'data': candidate,
                'calon_id': calon_id
            })

        # Find party blocks
        party_blocks = pair_block.find('div', class_='party').find_all('img', class_='img-fluid')

        for party_block in party_blocks:
            party = {}
            party['image_url'] = party_block['src']
            party['name'] = party_block['alt']

            pair['parties'].append(party)

        # Find visi-misi blocks
        visi_misi_blocks = pair_block.find('div', class_='visi-misi').find_all('p', class_='text-justify')

        for visi_misi_block in visi_misi_blocks:
            if pair['visi_misi']['visi'] is None:
                pair['visi_misi']['visi'] = visi_misi_block.get_text()
            elif pair['visi_misi']['misi'] is None:
                pair['visi_misi']['misi'] = visi_misi_block.get_text()

        # Initialize variables to store calon_id values
        calon_id = None
        wakil_calon_id = None
        pair_id = 0

        # Iterate through the candidates to find the calon_id for each type
        for candidate in pair['candidates']:
            if candidate['type'] == 'CALON':
                calon_id = candidate['calon_id']
            elif candidate['type'] == 'WAKIL CALON':
                wakil_calon_id = candidate['calon_id']

        # Concatenate the two calon_id values into the desired format
        if calon_id is not None and wakil_calon_id is not None:
            result = f"{calon_id}-{wakil_calon_id}"
            pair_id = result
        else:
            print("Missing CALON or WAKIL CALON data")

        pairs.append({
            'pair_id': pair_id,
            'data': pair
        })

    return json.dumps(pairs, indent=4)

# Function to extract table data
def get_table_data_old(soup, table_heading):
    table_data = []
    table_section = soup.find('th', string=table_heading)
    if table_section:
        table = table_section.find_parent('table')
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                row_data = [col.text.strip() for col in cols]
                table_data.append(row_data)
    return table_data

def get_table_data(soup, table_heading):
    table_data = []
    table_section = soup.find('th', string=table_heading)
    if table_section:
        table = table_section.find_parent('table')
        
        # Extract headers from the table
        headers = [th.text.strip() for th in table.find('thead').find_all('th')][1:]
        
        # Extract rows
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:
                row_data = {headers[i]: col.text.strip() for i, col in enumerate(cols)}
                table_data.append(row_data)
    return table_data

def get_info(candidate_info, soup):
    # Extracting the candidate's basic information
    #candidate_info = get_candidate_info(soup)

    # Extract Riwayat Pendidikan
    candidate_info['Riwayat Pendidikan'] = get_table_data(soup, 'Riwayat Pendidikan')

    # Extract Riwayat Kursus/Diklat
    candidate_info['Riwayat Kursus/Diklat'] = get_table_data(soup, 'Riwayat Kursus/Diklat')

    # Extract Riwayat Organisasi
    candidate_info['Riwayat Organisasi'] = get_table_data(soup, 'Riwayat Organisasi')

    # Extract Riwayat Tanda Penghargaan
    candidate_info['Riwayat Tanda Penghargaan'] = get_table_data(soup, 'Riwayat Tanda Penghargaan')

    # Extract Riwayat Publikasi
    candidate_info['Riwayat Publikasi'] = get_table_data(soup, 'Riwayat Publikasi')

    # Display the extracted information
    #for key, value in candidate_info.items():
    #    print(f"{key}: {value}")


def set_args():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process some pilkada data.")

    # Define the arguments
    parser.add_argument('--jenis_pemilihan', type=str, default="Gubernur", help='Type of Election : Gubernur|Walikota|Bupati, default:Gubernur')
    parser.add_argument('--get_foto', action='store_true', help='Get photo, default:False')
    parser.add_argument('--webp', action='store_true', help='Convert Image to Webp, default:False')

    global args

    # Parse the arguments
    args = parser.parse_args()

# Print the response or handle it as needed

set_args()

url_get_wilayah = "https://infopemilu.kpu.go.id/Pemilihan/Pasangan_calon/get_wilayah"

if args.jenis_pemilihan:
    list_pemilihan = args.jenis_pemilihan.split("|")

for pemilihan in list_pemilihan:
    body = f"jenis_pemilihan={pemilihan}"

    print(body)

    wilayah_arr = json.loads(fetch(url_get_wilayah,body).text)

    i = 0

    for wilayah in wilayah_arr:
        url = "https://infopemilu.kpu.go.id/Pemilihan/Pasangan_calon/filter"
        #body = "id_wilayah=ea23fd68f1136f2912b3fae095148429528e8f93f75e5135b4596302e63c772f417272704bafd8313f1c2918b80836622c6eea1b72e5a7ea325856a47d5f0e4cFwT81UqpOHwdUmBzIuShajzyKN4CGKaw7g9H5GNCaAo%3D"
        body = "id_wilayah=" + urllib.parse.quote(wilayah["id_wilayah_encrypted"])

        # Create the full directory structure
        base_dir = os.path.join('data', f"{pemilihan}")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        json_filename = f"{i}-{wilayah['nama_wilayah_baru']}.json"

        print(json_filename)

        output_path = os.path.join(base_dir, json_filename)

        text = fetch(url,body).text
        #print(text)
        json_result = parse_html_to_json(text)
        with open(output_path, "w") as external_file:
            external_file.write(json_result)
            external_file.close()

        i = i + 1
