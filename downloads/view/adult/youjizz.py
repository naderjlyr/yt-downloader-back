import sys

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_all_ids_ujz(category="most-popular", page_number="1"):
    url = "https://www.youjizz.com/" + category + "/" + page_number + ".html"

    headers = {
        'Cookie': 'commentPhrase=cllTWHVFd1ZzckYvVTRKd1ZZc1BWQ296clh5RCs0YjAyNTFjZGtQc3pLdz06OkgmihcPsRpzrB6ef53DIQU'
                  '=; RNLBSERVERID=ded6584 '
    }

    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_elements = soup.find_all('a', class_="frame video")
    return [a_element['data-video-id'] for a_element in a_elements]


def get_single_movie_ujz(movie_id):
    url = "https://www.youjizz.com/videos/-" + str(movie_id) + ".html "
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
    driver.get(url)
    # get the page source
    page_source = driver.page_source
    driver.close()
    # parse the HTML
    soup = BeautifulSoup(page_source, "html.parser")
    tags = soup.find('meta', {'name': 'keywords'})['content'].split(' , ')
    description = soup.find('meta', {'name': 'description'})['content']
    try:
        video_favorite = soup.find("input", {'id': "checkVideoFavorite"})
        views = video_favorite['data-views']
        rating = video_favorite['data-rating']
    except:
        views = 0
        rating = 0
    scripts = soup.find_all("script")
    image_url = "http:" + soup.find('meta', {'property': 'og:image'})['content']
    for script in scripts:
        if str(script).__contains__('var dataEncodings'):
            script = str(script)
            data_encodings = script.split('}];')[0]
            data_encodings = data_encodings.replace('<script>', '').replace(
                'var dataEncodings = ', '').replace('\n', '').replace(' ', '') + "}]"
            # data_encodings_str = data_encodings.split('dataEncodings =')[1] + "}]"
            # all_movie_data = list(eval(data_encodings_str))
            # download_links = [
            #     {'title': movie_data['name'],
            #      'link': ["https:" + movie_data['filename'].replace('\\', '')],
            #      'subtitle': '',
            #      'quality': movie_data['quality']}
            #     for movie_data in all_movie_data
            # ]
            return {'name': soup.find('title').text,
                    'farsi_name': '+18 ?????? ?????? ?????? ?????? ?????? ???????? ???????? ???????? ???????? ?????????? ',
                    'description': description,
                    'views': views,
                    'url': url,
                    'rating': rating,
                    'movie_id': movie_id,
                    'tags': tags,  # type of this field is Array
                    'image': image_url,
                    'download_links': data_encodings
                    }

# if __name__ == '__main__':
#     for page_number in range(1, 100):
#         all_ids = get_all_ids_ujz(page_number=str(page_number))
#         print(all_ids)
#         for movie_id in all_ids:
#             print(get_single_movie_ujz(movie_id))
