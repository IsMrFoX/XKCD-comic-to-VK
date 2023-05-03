import requests
import os
from random import randint
from dotenv import load_dotenv


def main():
    load_dotenv()

    url_template = 'https://xkcd.com/{}/info.0.json'
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_version_api = '5.131'

    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    data = response.json()
    total_comic_pages = data['num']
    page_comic_num = randint(1, total_comic_pages)

    url = url_template.format(page_comic_num)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    img_url = data['img']
    comment = data['alt']
    img_name = img_url.split("/")[-1]
    img_response = requests.get(img_url)
    img_response.raise_for_status()

    with open(f'{img_name}', 'wb') as file:
        file.write(img_response.content)

    # получаем URL сервера для загрузки изображения
    url = f'https://api.vk.com/method/photos.getWallUploadServer?access_token={vk_access_token}&v={vk_version_api}'
    response = requests.get(url)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']

    # отправляем POST-запрос с изображением на сервер VK
    with open(f'{img_name}', 'rb') as file:
        files = {
            'photo': ('image.jpg', file.read()),
            'caption': comment
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        response_json = response.json()
        server, photo, _hash = response_json['server'], response_json['photo'], response_json['hash']

    # сохраняем фотографию на сервере VK
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'server': server,
        'photo': photo,
        'hash': _hash,
        'access_token': vk_access_token,
        'v': vk_version_api
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    photo_id = response.json()['response'][0]['id']
    owner_id = response.json()['response'][0]['owner_id']

    # публикуем пост на стене фан-сообщества
    attachments = f'photo{owner_id}_{photo_id}'
    params = {
        'access_token': vk_access_token,
        'v': vk_version_api,
        'owner_id': f'-{vk_group_id}',
        'from_group': 1,
        'message': comment,
        'attachments': attachments
    }
    response = requests.post('https://api.vk.com/method/wall.post', params=params)
    os.remove(img_name)

    # проверяем, прошел ли запрос успешно
    response_dict = response.json()
    if 'error' in response_dict:
        error_msg = response_dict['error']['error_msg']
        print(f'Ошибка при публикации поста: {error_msg}')
    else:
        post_id = response_dict['response']['post_id']
        print(f'Пост успешно опубликован, id = {post_id}')


if __name__ == "__main__":
    main()
