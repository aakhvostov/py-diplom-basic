import json
from datetime import datetime
from urllib.parse import urlencode
import requests
from yaupload import upload_photos
from yaupload import make_folder


class User:
    def __init__(self, vk_id):
        self.id = vk_id
        self.photo_list = []

    def get_profile_photos(self):
        photos_info_list = []
        downloaded_files = []
        url = f"https://api.vk.com/method/photos.get"
        parameters = {
            "owner_id": self.id,
            "album_id": "profile",
            "extended": 1,
            "photo_sizes": 1,
            "count": 5,
            "access_token": "TOKEN",
            "v": 5.122
        }
        url_requests = "?".join((url, urlencode(parameters)))
        resp = requests.get(url_requests)
        self.photo_list = resp.json()["response"]["items"]
        for photo in self.photo_list:
            photos_info_list.append(
                {
                    "url": photo["sizes"][-1]["url"],
                    "likes": photo["likes"]["count"],
                    "size_type": photo["sizes"][-1]["type"],
                    "data": datetime.fromtimestamp(photo["date"]).strftime('%Y-%m-%d %H:%M:%S').
                        replace("-", "_").split()[0]
                }
            )
            downloaded_files.append({"file_name": f'{photo["likes"]["count"]}.jpg',
                                     "size": photo["sizes"][-1]["type"]})
        with open("downloaded_photos.json", "a") as file:
            json.dump(downloaded_files, file)
        return photos_info_list


def user_initial():
    # vk_id = int(input("Введите id "))
    # ya_path = input("Введите название папки ")
    make_folder("ya_path")
    upload_photos("ya_path", User(552934290).get_profile_photos())


user_initial()

# 552934290

