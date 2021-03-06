# Non-trivial_Films-DL

## О проекте

Проект создан для подбора фильмов на основе ваших любимых фильмов.

Подбор фильмов основан на схожести описаний.

Вся информация о фильмах взята с сайта Кинопоиск. 

## Технологии

База данных кинопоиска была выгружена с помощью beautifulsoup и selenium.

Технлогии для подбора фильмов с одинковым описанием: gensim на основе wordtovec.

И telegram api для бота в телеграме.

## Бот

Проект можно опробовать с помощью телерам бота.

@NonTrivialFilms_bot

## Планы

1. Создать сайт на **django**
2. Изменить технологию подбора фильмов (для ускорение процесса подбора)
3. Создание многоуровневой системы оценок фильмо (на основе не только описания, но и оценок и возрастного рейтинга)

## Запуск проекта

Для запуска проекта используйте сборку контейнера

``` bash
docker build -t your-name-image .
```

Докер запустит сайт с поиском фильмов

``` bash
docker run your-name-image
```
