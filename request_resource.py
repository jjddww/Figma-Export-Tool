import os
import re
from idlelib.iomenu import errors

import requests
from pathlib import Path

ANDROID_SCALES = [1, 1.5, 2, 3, 4]
iOS_SCALES = [1, 2, 3]

def get_file_key(window, res_link):
    match = re.search(r"design/([^/]+)", res_link)
    result = ""

    if match:
        result = match.group(1)
        window.print_log(f'file key = {result}')
        print("file key = ", result)
    else:
        window.print_log("Pattern error")
        print("Pattern error")

    return result



def get_res_node_id(window, res_link):
    match = re.search(r"\?node-id=(.*?)&", res_link)
    result = ""

    if match:
        result = match.group(1)
        window.print_log(f'image node id = {result}')
        print("node id = ", result)
    else:
        window.print_log("Pattern error")
        print("Pattern error")

    return result



def export_resource(window, platform, token, paths, res_link, res_name):
    if platform == "android":
        scales = ANDROID_SCALES
        file_key = get_file_key(window, res_link)
        node_id = get_res_node_id(window, res_link)

        headers = {
            'X-Figma-Token': token
        }

        for index, scale_value in enumerate(scales):
            if not Path(paths[index]).exists():
                pass

            else:
                params = {
                    'ids': node_id,
                    'scale': scale_value,
                    'format': 'png'
                }
                response = requests.get(f'https://api.figma.com/v1/images/{file_key}', headers=headers, params=params)
                if response.status_code == 200:
                    try:
                        print(response.json()['images'])
                        res_url = response.json()['images'][node_id.replace("-", ":")]
                        full_path = os.path.join(paths[index], res_name)
                        download_res(window, res_url, f'{full_path}.png')
                    except Exception as e:
                        window.print_log(e)
                        print(e)

                else:
                    window.print_log(f"Error fetching image: {response.status_code} - {response.text}")
                    print(f"Error fetching image: {response.status_code} - {response.text}")

    elif platform =="iOS":
        scales = iOS_SCALES
        file_key = get_file_key(window, res_link)
        node_id = get_res_node_id(window, res_link)

        headers = {
            'X-Figma-Token': token
        }

        for index, scale_value in enumerate(scales):
            if not Path(paths[0]).exists():
                pass

            else:
                params = {
                    'ids': node_id,
                    'scale': scale_value,
                    'format': 'png'
                }
                response = requests.get(f'https://api.figma.com/v1/images/{file_key}', headers=headers, params=params)
                if response.status_code == 200:
                    try:
                        print(response.json()['images'])
                        res_url = response.json()['images'][node_id.replace("-", ":")]
                        temp_res_name = f'{res_name}@{int(index) + 1}x'
                        full_path = os.path.join(paths[0], temp_res_name)
                        download_res(window, res_url, f'{full_path}.png')
                    except Exception as e:
                        window.print_log(e)
                        print(e)

                else:
                    window.print_log(f"Error fetching image: {response.status_code} - {response.text}")
                    print(f"Error fetching image: {response.status_code} - {response.text}")



def download_res(window, url, res_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if os.path.exists(res_name):
                window.print_log(f"동일한 이름의 파일이 존재합니다 {res_name}")
                print(f"동일한 이름의 파일이 존재합니다 {res_name}")
            else:
                with open(res_name, 'wb') as file:
                    file.write(response.content)
                window.print_log(f"Success Save '{res_name}'")
                print(f"Saved '{res_name}'")

        else:
            window.print_log(f'{response.status_code} - {response.text}')
            print(f'{response.status_code} - {response.text}')
    except Exception as e:
        window.print_log(e)
        print(e)

