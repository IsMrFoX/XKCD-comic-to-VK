import requests
import os
from random import randint
from dotenv import load_dotenv


def download_random_comic(url_template):
    """
    Загружает случайный комикс из веб-комикса XKCD.

    Аргументы:
    url_template -- шаблон URL-адреса для загрузки комикса.

    Возвращает:
    Имя файла изображения комикса и его описание.
    """
    response = requests.get('https://xkcd.com/info.0.json')
    response.raise_for_status()
    comic_file = response.json()
    total_comic_pages = comic_file['num']
    page_comic_num = randint(1, total_comic_pages)

    url = url_template.format(page_comic_num)
    response = requests.get(url)
    response.raise_for_status()
    comic_file = response.json()
    img_url = comic_file['img']
    comment = comic_file['alt']
    filename = os.path.split(img_url)[1]

    img_response = requests.get(img_url)
    img_response.raise_for_status()

    with open(f'{filename}', 'wb') as file:
        file.write(img_response.content)

    return filename, comment


def upload_image_to_vk_server(filename, comment, vk_access_token, vk_api_version):
    """
    Загружает изображение комикса на сервер ВКонтакте для дальнейшей публикации на стене группы.

    Аргументы:
    filename -- имя файла изображения.
    comment -- описание комикса.
    vk_access_token -- access token ВКонтакте.
    vk_api_version -- версия API ВКонтакте.

    Возвращает:
    ID владельца и ID изображения на сервере ВКонтакте.
    """
    url = f'https://api.vk.com/method/photos.getWallUploadServer?access_token={vk_access_token}&v={vk_api_version}'
    response = requests.get(url)
    response.raise_for_status()
    upload_response = response.json()
    upload_url = upload_response['response']['upload_url']

    with open(f'{filename}', 'rb') as file:
        files = {
            'photo': ('image.jpg', file.read()),
            'caption': comment
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    upload_response = response.json()
    server, photo, _hash = upload_response['server'], upload_response['photo'], upload_response['hash']

    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'server': server,
        'photo': photo,
        'hash': _hash,
        'access_token': vk_access_token,
        'v': vk_api_version
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    upload_response = response.json()
    photo_id = upload_response['response'][0]['id']
    owner_id = upload_response['response'][0]['owner_id']

    return owner_id, photo_id


def post_comic_to_vk_wall(owner_id, photo_id, comment, vk_access_token, vk_group_id, vk_version_api):
    """
    Публикует комикс на стене группы ВКонтакте.

    Аргументы:
    owner_id -- ID владельца изображения на сервере ВКонтакте.
    photo_id -- ID изображения на сервере ВКонтакте.
    comment -- описание комикса.
    vk_access_token -- access token ВКонтакте.
    vk_group_id -- ID группы ВКонтакте.
    vk_api_version -- версия API ВКонтакте.

    Возвращает:
    Ответ от API ВКонтакте после публикации поста на стене группы.
    """
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
    response.raise_for_status()

    return response.json()


def print_is_post_successful(post_response):
    """
    Проверяет, прошла ли публикация поста на стене группы ВКонтакте успешно.

    Аргументы:
    post_response -- ответ от API ВКонтакте после публикации поста.

    Возвращает:
    None.
    """
    if 'error' in post_response:
        error_msg = post_response['error']['error_msg']
        print(f'Ошибка при публикации поста: {error_msg}')
    else:
        post_id = post_response['response']['post_id']
        print(f'Пост успешно опубликован, id = {post_id}')


def main():
    load_dotenv()

    url_template = 'https://xkcd.com/{}/info.0.json'
    vk_access_token = os.environ['VK_ACCESS_TOKEN']
    vk_group_id = os.environ['VK_GROUP_ID']
    vk_api_version = '5.131'

    filename, comment = download_random_comic(url_template)
    try:
        owner_id, photo_id = upload_image_to_vk_server(filename, comment, vk_access_token, vk_api_version)
    except Exception as error:
        print('Ошибка:', error)
    finally:
        os.remove(filename)

    post_response = post_comic_to_vk_wall(owner_id, photo_id, comment, vk_access_token, vk_group_id, vk_api_version)
    print_is_post_successful(post_response)


if __name__ == "__main__":
    main()
