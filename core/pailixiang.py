from bs4 import BeautifulSoup
import requests
import os

URL_GETINFO = "https://www.pailixiang.com/Portal/Services/AlbumDetail.ashx?t=1"


def download_all_images(url: str, store_path: str):
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    soup_data = BeautifulSoup(requests.get(url).text, "html.parser")
    for node in soup_data.find_all("script"):
        if "albumId" in str(node):
            albumId_raw = [i.strip() for i in str(node).split("\n") if "albumId" in i][0].split("{")[1].split("}")[0]
            albumId_raw = [i.strip() for i in str(albumId_raw).split(",") if "albumId" in i][0]
            albumId_raw = albumId_raw.split('"')[1]
    # print(albumId_raw)
    data = {
        "start": 0,
        "len": 1,
        "albumId": albumId_raw,
    }
    total_count = requests.post(URL_GETINFO, data).json()["TotalCount"]
    # print(total_count)
    for i in range(1, total_count):
        data["start"] = i
        image_info = requests.post(URL_GETINFO, data).json()["Data"][0]
        image_filename = image_info["Name"]
        image_url = image_info["DownloadImageUrl"]
        print("正在下栽第{}张 - 文件名:{}".format(i, image_filename))
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # 如果响应状态不是200，就主动抛出异常
        except requests.RequestException as err:
            print("Oops: Something else happened", err)
            return
        with open(os.path.join(store_path, image_filename), "wb") as out_file:
            out_file.write(response.content)
