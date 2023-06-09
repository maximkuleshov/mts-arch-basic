## Импорт данных в mongo

Данные по авторам я брал из прошлого модуля - [ExportJson](ExportJson.json).
Для загрузки использовалась утилита `mongoimport`:

    $ mongoimport --username admin --password admin --authenticationDatabase admin --db college --collection temp --jsonArray ExportJson.json

Утилита грузит так, что индекс `_id` получает тип `ObjectId` -- а сервис построен так, что ожидает строку.
Поэтому грузим во временную коллекцию и после загрузки переделываем ее в целевую `authors` через mongo shell:

    > db.authors.insertMany(db.temp.find().map(function (document) { document._id = document._id + ''; return document; }))
    > db.temp.drop()

Проверяем, что все данные загружены:

    > db.authors.count()
    100000

## Нагрузочное тестирование сервисов

Далее нужно создать список `id` авторов для [lua-скрипта](get.lua) нагрузочного тестироваия. Так как в отличии от прошлого примера - у нас не последовательные целые числа в качестве `id`.
Пользуемся `mongoexport`:

    $ mongoexport --username admin --password admin --authenticationDatabase admin --db college --collection authors -f _id --csv | tail -n +2 > oids.txt

Выгрузка происходит в формате csv, но нам не нужна первая строчка заголовка. После этого нужно чуть поправить [lua-скрипт](get.lua).

Запускаем тестирование. Проводим измерения с такими же параметрами, что и для версии MariaDB.

### Сервис без кэширования

| Время / Потоки / Соединения | Latency  | RPS           | MariaDB Latency | MariaDB RPS |
| --------------------------- | -------- | ------------- | --------------- | ----------- |
| 60 / 1 / 1                  | 12.16ms  | 106.18        | 23.66ms         | 44.96       |
| 60 / 10 / 10                | 57.65ms  | 140.27        | 222.24ms        | 44.94       |              
| 60 / 50 / 50                | 240.45ms | 169.48        | 1300ms          | 32.61       |

### Сервис с кэшированием

| Время / Потоки / Соединения | Latency  | RPS           | MariaDB Latency | MariaDB RPS |
| --------------------------- | -------- | ------------- | --------------- | ----------- |
| 60 / 1 / 1                  | 10.21ms  | 100.90        | 13.22ms         | 91.73       |
| 60 / 10 / 10                | 73.00ms  | 110.94        | 90.23ms         | 111.82      |              
| 60 / 50 / 50                | 391.58ms | 104.98        | 815.82ms        | 60.83       |

### Выводы

1. MongoDB показывает чуть более высокую производительность на простых данных, чем PostgreSQL. В тоже время, при увеличении количества одновременных запросов - производительность MongoDB падает заметно медленне, чем PostgreSQL. Возможно, таких же результатов можно достичь и на PostgreSQL - но потребуется анализ узких мест и тюнинг модели данных.
 
2. MongoDB отлично справляется с выдачей данных по `id` без дополнительного внешнего кэша.
Кеширование помогает уже не так эффективно, как в случае с реляционной БД. Правда, в прошлом примере узким местом был пул-коннектов, так что сравнивать не совсем уместно. Тем не менее, для случая с небольшим одновременным количество запросов - кэш почти не дает прироста.

## Описание операций MongoDB

**Aggregation** - выполнение аналитических запросов над данными. 
Пример: для нашей базы найти самые редкие 10 фамилий и вывести количество авторов с такими фамилиями:

```
db.authors.aggregate([
        {
            $group: {
                "_id": "$last_name", 
                "count": { $sum: 1 }
            }
        },
        {
            $sort: { 
                "count": 1
            } 
        },
        {
            $limit: 10
        }
])
```

**Text Search** - выполнение текстового поиска с ипользованием языка запросов. 
Пример: найдем среди коллекции авторов таких, у которых должность менеджер, но не cash manager. 
Сначала создадим индекс:

```
db.authors.createIndex({ title: "text" })
```

Затем собственно поиск. Ограничим выдачу первыми 10 записями:

```
db.authors.find( { "$text": { $search: "manager -cash" } }).limit(10)
```

Текстовый поиск может использовать индекс объединенный из нескольких полей документа.

**MapReduce** - выполнение операции оптимизированной под алгоритм map-reduce для коллекции данных.
Пример: в базе у автора есть дата рождения. Сгруппируем авторов по возрастам и выведем количество по каждому возрасту. *Функция вычисления возраста в примере, конечно, кривая, потому что мне не удалось сходу найти неагрегатнную функцию разницы между двумя датами в годах*. Документация по современным версиям Mongo сообщает, что в подобных операциях нужно отдавать предпочтение методу `Aggregate`.

```
var mapFunction = function() {
    emit(Math.trunc((new Date() - new Date(this.birth_date)) / (1000 * 60 * 60 * 24 * 365)), 1)
}

var reduceFunction = function(year, count) {
    return Array.sum(count);
};

db.authors.mapReduce(mapFunction, reduceFunction, { out: "authors_age" })

db.authors_age.find({}).sort({"_id": -1})
```

**GeoSpatial Queries** - выполнение запросов, включащих гео-функции. 

Например, если бы у авторов были координаты их домашнего адреса (полученные, скажем, из текстового адреса в результате геокодинга) - то можно было бы выполнить запрос вида "*получить всех авторов которые живут не далее чем 10км от данной точки*".

**Transaction** - хотя и MongoDB относится к NoSQL документным базам - в документации сказано, что в современных версиях системы поддерживаются транзакции в рамках нескольких документов (включая документы разных коллекций) и даже в конфигурациях sharding/replica set.

Пример: когда автор регистрируется на конференцию - мы одновременно записываем документ и в коллекцию `authors` и в коллекцию `presentations`. При возникновении ошибки - данные не окажутся в промежуточном состоянии - то есть автор без презентации или презентация без автора - и мы получим состояние такое же, какое и было до момента старта (неудачной) записи. 



