# Python Practicum Telegram bot

#### Бот обращается к API Яндекс.Практикума и сообщает через Telegram об изменениях в статусах домашних работ, взятых на проверку.

##### Инструкция по запуску:

1. Склонируйте репозиторий в удобную для вас директорию:

  ```git clone <ссылка на репозиторий> <директория>```

2. Перейдите в директорию и создайте в ней виртуальное окружение:

  Linux:

  ```python3 -m venv venv```

  Windows:

  ```python -m venv venv```

3. Активируйте виртуальное окружение:

  Linux:

  ```source venv/bin/activate```

  Windows:

  ```source vevn/Scripts/activate```

4. Установите необходимые зависимости:

  ```pip install -r requirements.txt```

5. Создайте бота в Telegram для получения статусов проверки домашних работ: 

	- Найдите @BotFather.
	- Нажмите Start и выполните команду /newbot. 
	- Задайте диалоговое и техническое имя вашего бота. 
	- После успешного создания бота вы получите токен (TELEGRAM_TOKEN).

6. Создайте в директории приложения файл **.env**, который должен обязательно содержать следующие данные (кавычки не нужны):

	 **PRACTICUM_TOKEN**='' получаем по адресу https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a

	 **TELEGRAM_TOKEN**='' токен из шага 5.

	 **TELEGRAM_CHAT_ID**='' получаем через бота @userinfobot.

7. Запуск приложения:

  Linux:

  ```python3 homework.py```

  Windows:

  ```python homework.py```
