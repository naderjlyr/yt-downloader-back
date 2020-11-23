import requests
from bs4 import BeautifulSoup


def get_quality(text):
    if text.__contains__('1080p'):
        return '1080p'
    elif text.__contains__('720p'):
        return '720p'
    elif text.__contains__('480p'):
        return '480p'
    else:
        return None


def get_download_links_series_azintv(post_id) -> list:
    """
    :param post_id:
    :rtype: list
    """
    url = "https://azintv.xyz/wp-admin/admin-ajax.php"

    payload = "action=getPostLinksAjax&id=" + post_id + "&posttype=tvshow"
    headers = {
        'authority': 'azintv.xyz',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://azintv.xyz',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://azintv.xyz/tvshow/series-5296406/',
        'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
        'cookie': '_ga=GA1.1.1932757469.1605702498; _ga_QZ7VPPQ3VY=GS1.1.1605971522.10.1.1605971908.0'
    }

    response_download_link = requests.request("POST", url, headers=headers, data=payload)

    soup_download_links = BeautifulSoup(response_download_link.text, 'html.parser')
    download_links = soup_download_links.find_all('h3')
    for download_link in download_links:
        series_link = download_link.findNext('a')['href']
        print(series_link)
        # http://dls1.mydownloadcenter.pw/Series/D/Designated%20Survivor/S03/720p%20WEBRip%20%20AAC%202CH%20%20x265%20PSA%20230MB/Designated_Survivor_S03E01_x265_720p_WEBRip_PSA.mkv
        response_series = requests.request("GET", series_link)
        soup_series = BeautifulSoup(response_series.text, 'html.parser')
        series_links = [{'title': series_element.find('a').text, 'link': series_element.find('a')['href']} for
                        series_element in soup_series.find_all('tr')[1:]]
        print(series_links)
    download_links = [{
        "title": clean_text(download_link.text),
        "link": [],
        "subtitle": '',
        "quality": clean_text(download_link.findNext('p').text).split(' / ')[0],
    } for download_link in
        download_links]
    return download_links


def get_download_links_azintv(imdb_id, year, film_type="Movies"):
    url = "http://dls1.mydownloadcenter.pw/" + film_type + "/" + year + "/" + imdb_id + "/"
    response_download_link = requests.request("GET", url)
    soup_download_links = BeautifulSoup(response_download_link.text, 'html.parser')
    download_links = soup_download_links.find_all('a')[1:]
    download_links = [{
        "title": download_link['href'],
        "link": [url + download_link['href']],
        "subtitle": '',
        "quality": get_quality(download_link['href']),

    } for download_link in
        download_links]
    return download_links


def clean_text(text):
    return text.replace('(', '').replace(')', '').replace('\n', '').replace('  ', '')


def subtitle_almas_download(imdb_id, year, film_type='Movies'):
    # download from almassub.pw
    url = "http://subtitle.mydownloadcenter.pw/AS/Movies/" + str(year) + "/" + str(imdb_id)

    response = requests.request("GET", url)
    response = response.text.encode('utf8').decode()
    soup = BeautifulSoup(response, 'lxml')
    a_tags = soup.find_all('a')
    if len(a_tags) > 0:
        links = [{a_tag['href'].split('.')[0]: 'http://subtitle.mydownloadcenter.pw/AS/'
                                               + film_type + '/' + str(year) +
                                               '/' + str(imdb_id) + "/" +
                                               a_tag['href']} for a_tag in a_tags[1:]]
        return links
    return []


def all_genres() -> list:
    """
    :rtype: list
    """
    url = "https://azintv.xyz/"

    response = requests.request("GET", url)
    response = response.text.encode('utf8').decode()
    soup = BeautifulSoup(response, 'lxml')
    parent_genres = soup.find_all('div', class_='home-genres')
    # genres = [parent_genre.find_all('a')['href'] for parent_genre in parent_genres]
    genres = [a['href'].split('/')[-2] for parent_genre in parent_genres for a in parent_genre.find('ul').find_all('a')]
    return list(set(genres))


#
def all_movie_imdb_ids(movie_genre: str, page_number: str = '2', film_type: str = 'movie') -> list:
    """
    :param movie_genre:
    :param page_number:
    :param film_type:
    :return:
    :rtype: object
    """
    url = "https://azintv.xyz/genre/" + movie_genre + "/page/" + str(page_number)
    if film_type == 'series':
        url = "https://azintv.xyz/tvshow-genre/" + movie_genre + "/page/" + str(page_number)
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posters = soup.find_all('div', class_='poster')
    imdb_ids = [poster.find('a')['href'].split('/')[-2] for poster in posters]
    return imdb_ids


def single_movie(imdb_id, film_type="movie"):
    """
    :param imdb_id:
    :param film_type: series, movie
    :return:
    """
    poster_url = 'https://azintv.xyz/movie/' + imdb_id
    if film_type == "series":
        poster_url = 'https://azintv.xyz/tvshow/series-' + imdb_id
    response = requests.request("GET", poster_url)
    soup_detail = BeautifulSoup(response.text, 'html.parser')
    post_id = soup_detail.find('div', class_='downloadlinks text-center')['id']
    # DOWNLOAD LINKS

    imdb_data = imdb_single_info("tt" + imdb_id)
    name = imdb_data['name']
    description = clean_text(imdb_data['description'])
    genres = imdb_data['genres']
    country = imdb_data['country']
    language = imdb_data['language']
    year = imdb_data['year']
    duration = imdb_data['duration']
    image = imdb_data['image']
    imdb_rate = imdb_data['imdb_rate']
    subtitles = subtitle_almas_download(str(poster_url.split('/')[-2]), year)
    if film_type == "movie":
        download_urls = get_download_links_azintv(imdb_id, year=year)
    elif film_type == "series":
        download_urls = get_download_links_series_azintv(post_id)
    else:
        download_urls = []
    details = soup_detail.find('div', class_='detail')
    farsi_name = ''
    for detail in details.find_all('li'):
        if detail.find('span', class_='text-orange').text.__contains__('عنوان فارسی'):
            farsi_name = detail.find('strong').text
    return {
        'name': name,
        'farsi_name': farsi_name,
        'description': description,
        'genres': genres,
        'country': country,
        'year': year,
        'main_language': language,
        'subtitles': subtitles,
        'duration': duration,
        'imdb_id': imdb_id,
        'imdb_rate': imdb_rate,
        'image': image,
        'download_links': download_urls,

    }
    # END DOWNLOAD LINKS


def imdb_single_info(imdb_id):
    url = "https://www.imdb.com/title/" + str(imdb_id)
    response = requests.request("GET", url)
    response = response.text.encode('utf8').decode()
    soup = BeautifulSoup(response, 'lxml')
    name = soup.find("div", {"id": "ratingWidget"}).find('p').find('strong').text.strip()
    description = soup.find('div', class_='summary_text').text
    detail_elements = soup.find('div', {'id': 'titleDetails'}).find_all('div')
    year = clean_text(soup.find('span', {'id': 'titleYear'}).text) if soup.find('span', {'id': 'titleYear'}) else None
    imdb_rate = clean_text(soup.find('span', {'itemprop': 'ratingValue'}).text)
    image = soup.find('div', class_="poster").find('img')['src']

    country = ''
    language = ''
    for detail_element in detail_elements:
        if detail_element.find('h4') is not None:
            if detail_element.find('h4').text.__contains__("Country"):
                country = detail_element.find('a').text
            elif detail_element.find('h4').text.__contains__("Language"):
                language = detail_element.find('a').text

    genres = [genre.text for genre in
              soup.find('div', class_='title_wrapper').find('div', class_='subtext').find_all('a')][:-1]
    duration = clean_text(soup.find('div', class_='title_wrapper').find('time').text)
    return {
        'name': name,
        'description': description,
        'genres': genres,
        'country': country,
        'language': language,
        'duration': duration,
        'year': year,
        'imdb_rate': imdb_rate,
        'image': image,
    }


# print(imdb_single_info('tt7556122'))
# print(single_movie('5296406/', film_type="tvshow"))
# print(single_movie('8630154'))
if __name__ == '__main__':
    all_genres = all_genres()
    print(all_genres)
    for genre in all_genres:
        imdb_ids = all_movie_imdb_ids(genre)
        print(imdb_ids)
        for imdb_id in imdb_ids:
            print(single_movie(imdb_id))
sample_out = {
    'name': '',
    'farsi_name': '',
    'description': "",
    'genres': ['Mystery'],
    'country': 'South Korea',
    'year': '2020',
    'main_language': 'Korean',
    'subtitles': [],
    'duration': '1h 37min',
    'imdb_id': '11727052',
    'imdb_rate': '5.7',
    'image': 'https://m.media-amazon.com/images/M268_AL_.jpg',
    'download_links': [{'title': '',
                        'link': [
                            'http:.1080p.10bit.BluRay.x265.HEVC.VXT.mp4'],
                        'subtitle': '',
                        'quality': '1080p'},
                       ]}
