import json
from datetime import datetime
# from pprint import pprint
from urllib.parse import urlencode
import requests
from yaupload import upload_photos
from yaupload import make_folder


class User:
    def __init__(self, vk_id):
        self.id = vk_id
        self.photo_list = []

    def get_profile_photos(self, album_id="profile"):
        profile_photos_info_list = []
        downloaded_files = []
        url = f"https://api.vk.com/method/photos.get"
        parameters = {
            "owner_id": self.id,
            "album_id": album_id,
            "extended": 1,
            "photo_sizes": 1,
            "count": 5,
            "access_token": "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008",
            "v": 5.122
        }
        url_requests = "?".join((url, urlencode(parameters)))
        resp = requests.get(url_requests)
        self.photo_list = resp.json()["response"]["items"]
        for photo in self.photo_list:
            profile_photos_info_list.append(
                {
                    "url": photo["sizes"][-1]["url"],
                    "likes": photo["likes"]["count"],
                    "size_type": photo["sizes"][-1]["type"],
                    "data": datetime.fromtimestamp(photo["date"]).strftime(
                        '%Y-%m-%d %H:%M:%S').replace("-", "_").split()[0]
                }
            )
            downloaded_files.append({"file_name": f'{photo["likes"]["count"]}.jpg',
                                     "size": photo["sizes"][-1]["type"]})
        with open("downloaded_photos.json", "a") as file:
            json.dump(downloaded_files, file)
        return profile_photos_info_list

    def get_albums_list(self):
        albums_photos_info_list = []
        url = f"https://api.vk.com/method/photos.getAlbums"
        parameters = {
            "owner_id": self.id,
            "count": 10,
            "access_token": "958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008",
            "v": 5.122
        }
        url_requests = "?".join((url, urlencode(parameters)))
        response = requests.get(url_requests)
        try:
            print(response.json()["response"]["items"])
            for album in response.json()["response"]["items"]:
                albums_photos_info_list.append({"album_id": album["id"], "title": album["title"]})
            return albums_photos_info_list
        except KeyError:
            print('Альбомы пользователя заблокированы')
            return albums_photos_info_list

def user_initial():
    vk_id = int(input("Введите vk id - "))
    ya_path = input("Введите название папки для сохнаниения в яндекс диск - ")
    # vk_id = 14154609 552934290
    # ya_path = 'ульянов1'
    u = User(vk_id)
    make_folder(ya_path)
    print('Выберите альбом для загрузки фото...')
    for index, album in enumerate(u.get_albums_list()):
        print(f'{index} - {album["title"]}')
    try:
        index = int(input('...или введите любую букву для загрузки фото профиля\n'))
        upload_photos(ya_path, u.get_profile_photos(u.get_albums_list()[index]["album_id"]))
    except ValueError:
        upload_photos(ya_path, u.get_profile_photos())


user_initial()
