# work-calendar

Work calendar service. It's a part of my Smart Home.

Сервис, возвращающий информацию, выходным или рабочим является день.

## (EN)

How many holidays in Russia!
This is a service that defines a business day or a day off. It use open data from [data.gov.ru](http://data.gov.ru/) site.

### Run

Simply use docker or docker-compose

### Examples

https://my_host/calendar/day/

https://my_host/calendar/day/2018-06-09/

It returns JSON structure:

_holiday_: True or False

_default_: True when the calendar from gov.ru is not loaded

https://my_host/calendar/update/ - It requests data update from [data.gov.ru](http://data.gov.ru/)

## (RU)

Сервис, возвращающий информацию, является день праздничным или нет. Использую как часть своего "Умного дома".
Используется производственный календарь, публикуемый на сайте [data.gov.ru](http://data.gov.ru/)

### Примеры запросов

https://my_host/calendar/day/

https://my_host/calendar/day/2018-06-09/

Возвращается JSON:

_holiday_: True or False

_default_ - True когда нет данных с сайта gov.ru и значение вычислено только по дню недели

https://my_host/calendar/update/ - Запрашивает обновление календаря с сайта [data.gov.ru](http://data.gov.ru/)

## TODO

Add personal calendar and sync it with Google.
