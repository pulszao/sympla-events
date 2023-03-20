from time import sleep
import requests as requests
from bs4 import BeautifulSoup

url = 'https://www.sympla.com.br/eventos/caxias-do-sul-rs?cl=17-festas-e-shows'
api_url = 'https://admin.hipubapp.com/web/v1/schedule/register/'
# api_url = 'http://localhost:8000/web/v1/schedule/register/'

card_link = 'EventCardstyle__CardLink-sc-1rkzctc-3 eDXoFM sympla-card'
card_title = 'EventCardstyle__EventTitle-sc-1rkzctc-7'
card_place = 'EventCardstyle__EventLocation-sc-1rkzctc-8'
title_class = 'EventListInfostyle__Title-sc-1wzh7l6-2'
hour_class = 'EventListInfostyle__ListOption-sc-1wzh7l6-4'
host_name_class = 'EventLocalInfosstyle__HostName-twjfn8-3'
div_place_class = 'EventLocalInfosstyle__Info-twjfn8-2'  # the city is in the last <p> of the div
description_class = 'EventDescriptionstyle__Description-sc-1hmlyb8-0'


def get_event_data(event_url: str):
    if event_url is not None:
        response = requests.get(
            'https://www.sympla.com.br/evento/bulls-retro-israel-novaes/1884582',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        evt = response.text
        event_html = BeautifulSoup(evt, "html.parser")

        banner_url = event_html.find_all('img')[0].get('src')

        evt_title = event_html.find_all('h1', {'class': title_class})[0].text

        hour = event_html.find_all('li', {'class': hour_class})[0].text
        hour = get_hour_formatted(hour)

        host_name = event_html.find_all('h2', {'class': host_name_class})[0].text.strip()
        host_name = host_name.normalize('NFD').replace(u'\u0300', '').encode('ascii', 'ignore').decode()

        if host_name == 'Super Club Caxias':
            host_name = 'Reffugio'
        elif host_name == 'Super Club Caxias':
            host_name = 'Super Club'
        elif host_name == 'Tulipa Restaurante - Pavilhoes Festa da Uva':
            host_name = 'Tulipa Restaurante'

        evt_city = event_html.find_all('div', {'class': div_place_class})[0].find_all('p')[-1].text

        description = event_html.find_all('div', {'class': description_class})[0].text

        create_events({
            'banner_url': banner_url,
            'title': evt_title,
            'hour': hour,
            'host_name': host_name,
            'city': evt_city,
            'description': description
        })


def get_hour_formatted(hour):
    splitted_hour = hour.strip().split(' ')

    init_date = '0' + splitted_hour[0] if len(splitted_hour[0]) == 1 else splitted_hour[0]
    init_month = '0' + str(get_month_day(splitted_hour[1]))
    init_year = splitted_hour[3]
    init_hour = splitted_hour[5]

    final_date = ''
    final_month = ''
    final_year = ''
    final_hour = splitted_hour[-1]

    if len(splitted_hour) > 10:
        final_date = '0' + splitted_hour[7] if len(splitted_hour[7]) == 1 else splitted_hour[7]
        final_month = '0' + str(get_month_day(splitted_hour[8]))
        final_year = splitted_hour[10]
    else:
        final_date = init_date
        final_month = init_month
        final_year = init_year

    formatted_hour = {
        'initial_date': f"{init_year}-{init_month}-{init_date} {init_hour}",
        'final_date': f"{final_year}-{final_month}-{final_date} {final_hour}"
    }

    return formatted_hour


def get_month_day(month):
    if month == 'jan':
        return 1
    elif month == 'fev':
        return 2
    elif month == 'mar':
        return 3
    elif month == 'abr':
        return 4
    elif month == 'mai':
        return 5
    elif month == 'jun':
        return 6
    elif month == 'jul':
        return 7
    elif month == 'ago':
        return 8
    elif month == 'set':
        return 9
    elif month == 'out':
        return 10
    elif month == 'nov':
        return 11
    elif month == 'dez':
        return 12


def create_events(data):
    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        print(response.text)
        return True
    else:
        print(response.status_code)
        return False


def create_basic_events(data):
    response = requests.post(api_url, data=data)
    if response.status_code == 200:
        print(response.text)
        return True
    else:
        print(response.status_code)
        return False


if __name__ == '__main__':

    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    events = soup.find_all('a', {'class': card_link})

    if len(events) > 0:
        for ev in events:
            sleep(5)
            link = ev.get('href')
            # title = ev.attrs['title']
            # city = ev.attrs['aria-label'].split(', ')[-2]
            # palce = ev.attrs['aria-label'].split(', ')[-3].replace('em ', '')
            # date = ev.text[5:19].split(' ')
            # day = date[0]
            # month = get_month_day(date[1])
            # hour = date[-1]

            if link is not None:
                get_event_data(link)
                # create_basic_events({
                #     'title': title,
                #     'host_name': palce,
                #     'city': city,
                #     'description': '',
                #     'hour': {
                #         'initial_date': f"2023-{month}-{day} {hour}",
                #         'final_date': f"2023-{month}-{day} {hour}",
                #     },
                # })
    else:
        print('No events found')
