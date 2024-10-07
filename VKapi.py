import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlparse


def shorten_link(token, user_input):
    url = "https://api.vk.ru/method/utils.getShortLink"
    api_version = "5.131"

    params = {
        "access_token": token,
        "url": user_input,
        "v": api_version,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()

    return response_data["response"]["short_url"]


def count_clicks(token, short_url):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    api_version = "5.131"

    parsed_url = urlparse(short_url)
    key = parsed_url.path.split('/')[-1]

    params = {
        "access_token": token,
        "key": key,
        "source": "vk_cc",
        "access_key": "",
        "interval": "forever",
        "intervals_count": 1,
        "v": api_version
    }

    response = requests.get(api_url, params=params)
    response.raise_for_status()
    data = response.json()
    if data["response"]["stats"]:
        return sum(interval["views"] for interval in data["response"]["stats"])
    else:
        return 0


def is_shorten_link(token, url):
    api_url = "https://api.vk.com/method/utils.getLinkStats"
    api_version = "5.131"

    parsed_url = urlparse(url)
    key = parsed_url.path.split('/')[-1]

    params = {
        "access_token": token,
        "key": key,
        "source": "vk_cc",
        "access_key": "",
        "interval": "forever",
        "intervals_count": 1,
        "v": api_version
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        return 'response' in data
    except:
        return False


def main():
    load_dotenv()
    token = os.environ.get("TOKEN")
    user_input = input("Введите ссылку:")

    try:
        if is_shorten_link(token, user_input):
            clicks = count_clicks(token, user_input)
            print(f"Количество кликов по ссылке: {clicks}")
        else:
            short_link = shorten_link(token, user_input)
            print(f"Сокращенная ссылка: {short_link}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP ошибка: {http_err}")


if __name__ == "__main__":
    main()
