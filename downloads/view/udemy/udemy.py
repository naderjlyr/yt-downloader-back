import requests
from bs4 import BeautifulSoup


def get_all_udemy_links(page_number=1, category='video-tutorials'):
    url = "https://downloadly.ir/download/elearning/" + category + "/page/" + str(page_number)
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_url_divs = soup.find_all('div', class_='bp-head')
    links = [all_url_div.find('a')['href'].split('/')[-2] for all_url_div in all_url_divs]
    return links


def get_single_udemy(url_slug, category='video-tutorials'):
    url = "https://downloadly.ir/elearning/" + category + "/" + str(url_slug)
    response = requests.request("GET", url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find('h1', class_='post-tile entry-title').text
    image = soup.find('div', class_='feature-img')
    image_url = ''
    if image is not None:
        image_url = image.find('img')['src']
    entry_content = soup.find('div', class_='entry-content')
    description = entry_content.find_all('p')[0].text
    header_tags = entry_content.find_all('h3')
    download_links = []
    for header_tag in header_tags:
        if header_tag.text == 'لینک دانلود':
            download_link_title = ''
            for tags in header_tag.findAllNext():
                if tags.name == "h4":
                    download_link_title = tags.text
                if tags.name == "a":
                    try:
                        download_link = tags['href']
                        download_link_name = "password: www.downloadly.ir" + download_link_title + " " + tags.text
                        download_links.append({
                            'title': download_link_name,
                            'link': download_link,
                        })
                    except:
                        continue
    return {'name': title,
            'farsi_name': description,
            'description': '',
            'url_slug': url_slug,
            'image': image_url,
            'download_links': download_links
            }


if __name__ == '__main__':
    print(get_single_udemy('crash-course-electronics-and-pcb-design'))
    # print(get_single_udemy('100-days-of-code-the-complete-python-pro-bootcamp-for-2021'))
    # for page_number in range(1, 200):
    #     for url_slug in get_all_udemy_links(page_number=page_number):
    #         print(get_single_udemy(url_slug))
out_sample = {'name': 'title',
              'farsi_name': 'description',
              'description': '',
              'image': 'image_url',
              'download_links': [{
                  'title': '',
                  'link': '',
              }]
              }
