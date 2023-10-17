# Бот "Жабка"

Шуточный бот, который по средам отправляет картинку с жабой в чат пользователю или группе, подписанным на сервис. Вы также можете запросить картинку в другие дни недели, но в таком случае на картинке будет указание, что сегодня не среда. Бот включает в себя команды для администраторов по обновлению пакета изображений, перезапуску бота и просмотру подписанных пользователей.

## Описание

Бот "Жабка" - это веселый и забавный Telegram-бот, который отправляет изображения с жабами пользователям или группам, подписанным на этот сервис. Картинки отправляются специально по средам в честь популярной интернет-традиции, известной как "Среднекосаточная жаба".

По средам бот радует подписчиков забавными изображениями жабок, распространяя радость и юмор. Однако пользователи также могут запросить изображения с жабами в другие дни недели. В таких случаях изображение дружелюбно напомнит, что сегодня не среда.

Бот включает в себя набор команд для администраторов по управлению пакетом изображений, перезапуску бота и просмотру списка подписанных пользователей. Эти команды предоставляют администраторам необходимые инструменты для поддержания и улучшения опыта пользователей.

## Требования

Для запуска проекта убедитесь, что у вас установлены следующие зависимости:

- Python 3.10+
- aiogram
- SQLAlchemy
- asyncpg
- fake-headers (необходимо, если требуются фейковые заголовки; используется в core.parser.pic_parser.py)
- apscheduler

## Установка и Использование

1. Клонируйте репозиторий на свой компьютер.
2. Создайте виртуальное окружение.
3. Установите зависимости с помощью `pip install -r requirements.txt`.
4. Создайте и запустите сервер базы данных PostgreSQL.
5. Отредактируйте файл .env.
6. Запустите бота с помощью `python main.py`.

# Настройки базы данных
DATABASE_URL = 'postgresql+asyncpg://username:password@localhost/database'





# Zhabka Bot

A humorous bot that sends a frog image to a user/group chat on Wednesdays to subscribers. You can also request an image on other days, but in that case, the image will indicate that today is not Wednesday. The bot includes admin commands for updating the image pack, restarting the bot, and viewing subscribed users.

## Description

The Wednesday Frog Bot is a fun and quirky Telegram bot that sends frog images to users or groups who are subscribed to the service. These images are specifically sent on Wednesdays, in celebration of the popular internet tradition known as "Wednesday Frog."

On Wednesdays, the bot sends delightful frog images to subscribers, spreading joy and humor. However, users can also request frog images on other days of the week. In such cases, the image will playfully remind them that it's not Wednesday.

The bot includes a set of admin commands for managing the image pack, restarting the bot, and viewing the list of subscribed users. These commands provide the necessary tools for administrators to maintain and enhance the user experience.

## Requirements

Before running the project, make sure you have the following dependencies installed:

- Python 3.10+
- aiogram
- SQLAlchemy
- asyncpg
- fake-headers (this is necessary if you need fake handlers. in core.parser.pic_parser.py)
- apscheduler


## Installation and Usage

1. Clone the repository to your computer.
2. Create a virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Create and run server DB Postgresql
5. Edit .env.
6. Run the bot using `python main.py`.


# Database settings
DATABASE_URL = 'postgresql+asyncpg://username:password@localhost/database'
