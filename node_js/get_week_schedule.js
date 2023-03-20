// This script reads a html from sympla and returns a set of events
const https = require('https');
var jsdom = require('jsdom');

const url = 'https://www.sympla.com.br/eventos/caxias-do-sul-rs?cl=17-festas-e-shows';

const card_class = 'jMNblV';
const card_link = 'EventCardstyle__CardLink-sc-1rkzctc-3 eDXoFM sympla-card';
const title_class = 'EventListInfostyle__Title-sc-1wzh7l6-2';
const hour_class = 'EventListInfostyle__ListOption-sc-1wzh7l6-4';
const host_name_class = 'EventLocalInfosstyle__HostName-twjfn8-3';
const div_place_class = 'EventLocalInfosstyle__Info-twjfn8-2'; // the city is in the last <p> of the div
const description_class = 'EventDescriptionstyle__Description-sc-1hmlyb8-0';
const banner_class = 'EventBannerstyle__SharingOptionsContainer-sc-15jnuc4-3';


https.get(url, (response) => {
    let data = '';

    response.on('data', (chunk) => {
        data += chunk;
    });

    response.on('end', async () => {
        const dom = new jsdom.JSDOM(data);        
        const events = dom.window.document.getElementsByClassName(card_link);

        if (events.length > 0) {
            for (const ev in events) {
                let link = events[ev].href;
                if (link !== undefined) {
                    let event = await getEventData(events[ev].href);
                }
            }
        } else {
          console.error(`No events found`);
        }
    });
}).on('error', (error) => {
    console.error(`'main' -> got error: ${error.message}`);
});


const getEventData = (eventUrl) => {
    if (eventUrl != undefined) {
        https.get(eventUrl, (response) => {
            let data = '';
        
            response.on('data', (chunk) => {
                data += chunk;
            });
        
            response.on('end', async () => {
                const dom = new jsdom.JSDOM(data);

                let headerStartIndex = data.indexOf('https://images.sympla.com.br/');
                let banner_url = data.substring(headerStartIndex, headerStartIndex + 49);

                let title = dom.window.document.getElementsByClassName(title_class)[0].innerHTML;

                let hour = dom.window.document.getElementsByClassName(hour_class)[0].innerHTML;
                hour = getHourFormatted(hour);

                let host_name = dom.window.document.getElementsByClassName(host_name_class)[0].innerHTML.trim();
                host_name = host_name.normalize('NFD').replace(/[\u0300-\u036f]/g, "");

                let city = dom.window.document.getElementsByClassName(div_place_class)[0].children[2].innerHTML;

                let description = dom.window.document.getElementsByClassName(description_class)[0].textContent;

                return {
                    'banner_url': banner_url,
                    'title': title,
                    'hour': hour,
                    'host_name': host_name,
                    'city': city,
                    'description': description
                };
            });
        }).on('error', (error) => {
            console.error(`'getEventData()' -> got error: ${error.message}`);
        });
    }
}


const getHourFormatted = (hour) => {
    let splitted_hour = hour.trim().split(' ');

    let init_date =  '0' + splitted_hour[0];
    let init_month =  '0' + getMonthDay(splitted_hour[1]);
    let init_year = splitted_hour[3];
    let init_hour = splitted_hour[5];

    let final_date = '';
    let final_month   = '';
    let final_year = '';
    let final_hour = splitted_hour[splitted_hour.length - 1];

    if (splitted_hour.length > 10) {
        final_date = '0' + splitted_hour[7];
        final_month = '0' + getMonthDay(splitted_hour[8]);
        final_year = splitted_hour[10];
    } else {
        final_date = init_date;
        final_month = init_month;
        final_year = init_year;
    }

    if (init_date.length > 2) {
        init_date = init_date.substring(1);
    }
    if (init_month.length > 2) {
        init_month = init_month.substring(1);
    }
    if (final_date.length > 2) {
        final_date = final_date.substring(1);
    }
    if (final_month.length > 2) {
        final_month = final_month.substring(1);
    }

    let formatted_hour = {
        'initial_date': init_year + '-' + init_month + '-' + init_date + ' ' + init_hour,
        'final_date': final_year + '-' + final_month + '-' + final_date + ' ' + final_hour,
    };

    return formatted_hour;
}


const getMonthDay = (month) => {
    if (month == 'jan') {
        return 1;
    }
    else if (month == 'fev') {
        return 2;
    }
    else if (month == 'mar') {
        return 3;
    }
    else if (month == 'abr') {
        return 4;
    }
    else if (month == 'mai') {
        return 5;
    }
    else if (month == 'jun') {
        return 6;
    }
    else if (month == 'jul') {
        return 7;
    }
    else if (month == 'ago') {
        return 8;
    }
    else if (month == 'set') {
        return 9;
    }
    else if (month == 'out') {
        return 10;
    }
    else if (month == 'nov') {
        return 11;
    }
    else if (month == 'dez') {
        return 12;
    }
}
