# FastAPI_TZ
Приложение по тестовому заданию.
Приложение использует БД SQLite. Выбор пал именно на неё, т.к. она проста в использовании и соответветствует требованиям ТЗ.
Команды приложения:
GET /memes: Получить список всех мемов (с пагинацией). Пагинация реализована через limit и offset, которые можно указать в строке браузера.
GET /memes/{id}: Получить конкретный мем по его ID. Например, при вводе http://localhost:8000/memes/1 (при наличии мема в БД и в бакете minIO) на экране отобразится изображение.
POST /memes: Добавить новый мем. В качестве имени берётся название файла. Возможно вставить только картинку - иначе выдаст ошибку. Изображение будет занесено в БД и в бакет minIO.
PUT /memes/{id}: Обновить существующий мем. Есть возможность как обновить только имя, так и картинку вместе с именем. При вводе картинки имя будет изменено на имя файла.
DELETE /memes/{id}: Удалить мем по его id. Изображение удалится как из бакета minIO, так и из БД.

Запустить приложение можно через docker путём выполнения следующих команд в командной строке:

git clone https://github.com/VictorRusyanov/FastAPI_TZ.git

cd FastAPI_TZ

docker build -t fastapi_tz .

docker-compose up


Взаимодейстовать с проектом можно через строку браузера, или по адресу http://localhost:8000/docs (через докуметанцию).

Параметры подключения к minIO, возможно, потребуется изменить.
