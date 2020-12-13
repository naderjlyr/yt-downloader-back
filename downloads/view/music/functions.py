import requests
from bs4 import BeautifulSoup

ALL_GENRES = {'genreid:MA0000012170': 'Avant-Garde', 'genreid:MA0000002467': 'Blues',
              'genreid:MA0000002944': "Children's", 'genreid:MA0000002521': 'Classical',
              'genreid:MA0000004433': 'Comedy/Spoken', 'genreid:MA0000002532': 'Country',
              'genreid:MA0000002567': 'Easy Listening', 'genreid:MA0000002572': 'Electronic',
              'genreid:MA0000002592': 'Folk', 'genreid:MA0000012075': 'Holiday',
              'genreid:MA0000002660': 'International', 'genreid:MA0000002674': 'Jazz', 'genreid:MA0000002692': 'Latin',
              'genreid:MA0000002745': 'New Age', 'genreid:MA0000002613': 'Pop/Rock', 'genreid:MA0000002809': 'R&B',
              'genreid:MA0000002816': 'Rap', 'genreid:MA0000002820': 'Reggae', 'genreid:MA0000004431': 'Religious',
              'genreid:MA0000004432': 'Stage & Screen', 'genreid:MA0000011877': 'Vocal'}


def d(t):
    o = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
         "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "m", "n", "p", "q", "r", "s", "t", "u", "v", "x",
         "y",
         "z", "1", "2", "3"]
    length = len(o)
    e = ""
    if 0 == t:
        return o[0]
    while 1:
        if t < 0:
            t = t * -1
            e = e + "-"
        value = int(t % length)
        t = int(t / length)
        e = e + o[value]
        if t <= 0:
            break
    return e


def get_album_music_titles(url):
    headers = album_music_headers
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    songs_sections = soup.find('tbody').find_all('tr')
    names_list = []
    for songs_section in songs_sections:
        if songs_section is not None:
            if songs_section.find('div', class_="title") is not None:
                if songs_section.find('div', class_="title").find('a') is not None:
                    names_list.append(songs_section.find('div', class_="title").find('a').text)
    return names_list


def get_all_music_titles(genre, page_number: int = 2) -> list:
    url = "https://www.allmusic.com/advanced-search/results/" + str(page_number)

    payload = "filters[]=" + genre + "&sort="
    headers = allmusic_header

    response = requests.request("POST", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, "html.parser")
    all_sections = soup.find('tbody').find_all('tr')
    song_names = []
    for single_section in all_sections:
        if single_section.find('td', class_='cover').find('a') is not None:
            detail_href = single_section.find('td', class_='cover').find('a')['href']
            detail_url = "https://www.allmusic.com" + detail_href
            song_names += get_album_music_titles(detail_url)
        else:
            break
    return song_names


# CONSTS
myfreemp3_header = {
    'authority': 'myfreemp3.vip',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, '
              '*/*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://myfreemp3.vip',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://myfreemp3.vip/',
    'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
    'cookie': '__cfduid=d9649c8884b9b05ad161740cc3963f3431606683203; _ga=GA1.2.67462512.1606683204; musicLang=en; '
              '_gid=GA1.2.525480570.1607355071; _gat=1 '
}

album_music_headers = {
    'authority': 'www.allmusic.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'text/html, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.allmusic.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.allmusic.com/advanced-search',
    'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',

    'Cookie': 'allmusic_session'
              '=9ZXIfeKAfTPQNnsyHLxdb7MWJkc3aAzK4BdGOfefbmGiNbNMrc067OYP7h9r7fgkPH4IEv2zaZ0t443CREK5Lqfwfaxhjf'
              '8MYAZIVdBdIPmRoBG0837rgBiHwpfuuccSf26nuD%2FPEAk2zqZbVvlBQkRV1tae902UduFKwrdBHeIdQv%2B'
              '%2BIOklA2v5DCyd3eKE6WhHhsS0MOy1%2FeUWhzYO'
              '%2BKcgxUMeTqBDjhHSEwH4J3eXlSnIHmkC8qemVpO8J9ymSYoAvx2NXvP7B%2FTwwft%2FZlHRgbuuR6vHW6gSfWqA'
              '%2BoIReXIyOktz2jbBnkWzJIcgStnOkVwBdqSpsC0DmwiwOkmzO9vPTEoUF'
              '%2BIa2enXPztuhYD5ejLKEaxGw4G606xPQP9vn4yUJm%2F5BAO3t6%2B5kf9%2FYfBdEv4R8BXJ9aWvWNhO1m'
              '%2BQlRRvTKu6AqvSHvaKaXiGlgBoRtJ%2Fh0CPashPzQ%3D%3D '
}
allmusic_header = {
    'authority': 'www.allmusic.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'text/html, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.88 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.allmusic.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.allmusic.com/advanced-search',
    'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
    'cookie': 'allmusic_session=nTE67s%2BC%2BRrwFe'
              '%2FxN1V7dS2DiklRSes4IzpzWEdOQfBzRjwVQLDoqdjx1EyhmTFruOHeyLORLaBe8%2FizeSuhd9D%2B'
              '%2F2i0lFzajCRkiGXtLw9Tj7vhynPlbu2dUqzv9WvVE2gQbTN'
              '%2BMpRGvM1Zm5GaKK37GWEDxBjIhd5b2n4hREOT23ZBQ503fI4JKBn%2FAttDjjJWhH'
              '%2FWm5fsyDzrFWVfYYAH791ANZm5R6NgT7JoDgv%2Fz3zzlzutgN6cM9FEZIrOcIYQcrwdcHkBqULCvn8%2B'
              '%2FfqLDnFkyQpDesBac9yfNmbPt2%2F5VxgYjVOUZlAYz7uQr8m%2FwvPsFnhjAQLjXQFAvgtt5zBTZiOWjR%2FVOcP1p'
              '%2FbuHHqwHeqscxzYt5ftR99zmiTH%2BDTHbfihwaWzOzY148JW5f58JV7Bu5L68XgXdFtmbXq8vOWtPzBBUIishuPp7R'
              '%2FKh3seT9Kzj3zfJvKO7Q%3D%3D; _ga=GA1.2.2059509668.1607378290; _gid=GA1.2.756508450.1607378290; '
              '__qca=P0-2067182979-1607378290775; policy=notified; registration_prompt=3; '
              'allmusic_session'
              '=9ZXIfeKAfTPQNnsyHLxdb7MWJkc3aAzK4BdGOfefbmGiNbNMrc067OYP7h9r7fgkPH4IEv2zaZ0t443CREK5Lqfwfaxh'
              'jf8MYAZIVdBdIPmRoBG0837rgBiHwpfuuccSf26nuD%2FPEAk2zqZbVvlBQkRV1tae902UduFKwrdBHeIdQv%2B'
              '%2BIOklA2v5DCyd3eKE6WhHhsS0MOy1%2FeUWhzYO'
              '%2BKcgxUMeTqBDjhHSEwH4J3eXlSnIHmkC8qemVpO8J9ymSYoAvx2NXvP7B%2FTwwft%2FZlHRgbuuR6vHW6gSfWqA'
              '%2BoIReXIyOktz2jbBnkWzJIcgStnOkVwBdqSpsC0DmwiwOkmzO9vPTEoUF'
              '%2BIa2enXPztuhYD5ejLKEaxGw4G606xPQP9vn4yUJm%2F5BAO3t6%2B5kf9%2FYfBdEv4R8BXJ9aWvWNhO1m'
              '%2BQlRRvTKu6AqvSHvaKaXiGlgBoRtJ%2Fh0CPashPzQ%3D%3D '
}
