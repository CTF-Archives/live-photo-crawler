from urllib.parse import urlparse
from core.photoplus import get_all_images as photoplus_dl
from core.pailixiang import download_all_images as pailixiang_dl

DEBUG = False


def photoplus_init(id: int, store_path: str):
    photoplus_dl(id, store_path)


def pailixiang_init(url: str, store_path: str):
    pailixiang_dl(url, store_path)


if __name__ == "__main__":
    store_path = "./res"
    if DEBUG == False:
        store_path = input("Enter where will you store photos (default: ./res): ")
        if store_path == "":
            store_path = "./res"
    print("Store path set to: {}".format(store_path))
    url = input("Please input live photos url: ")
    url_domain = urlparse(url).hostname
    print("URL has been identified: {}".format(url_domain))
    match url_domain:
        case "live.photoplus.cn":
            photoplus_id = urlparse(url).path.split("/")[3]
            if photoplus_id.isnumeric():
                photoplus_init(int(photoplus_id), store_path)
        case "www.pailixiang.com":
            pailixiang_init(url.split("?")[0], store_path)
