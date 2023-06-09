# ADR.001

Выбор класса системы хранение данных о конференциях и докладах

<!-- Название ADR состоит из [ADR.###] [Коротко суть принятого решения] -->

* Статус: Предложено
* Владелец: mekuleshov@mts.ru

## Контекст
<!-- Описание проблемы, требующей решения, причин, побудивших принять решение, ограничений, действовавших на момент принятия решения -->
Необходимо проанализировать, какой из типов хранилища данных больше подходит данных о конференциях и докладах 

## Варианты решения
<!-- Описание рассмотренных вариантов c их плюсами и минусами -->

### Традиционная ACID реляционная СУБД - PostgreSQL
<!-- Описание варианта 1 -->
* **Плюсы**
  * Не требуется дополнительная логика для организации консистентности данных бизнес уровня - выделение транзакций автоматически решает эту задачу
  * Больший опыт использования в команде - выше скорость разработки
  * Поддержка аналитических и агрегированных запросов для аналитики - средствами самой СУБД
* **Минусы**
  * Более сложный вариант горизонтального масштабирования
  * Изменения в модели данных требуют большей внимательности и процедур миграции данных
  * Масштабирование - только вертикальное

### Нереляционная БД BASE на основе MongoDB - вариант CP
<!-- Описание варианта 2 -->
* **Плюсы**
  * Поддержка горизонтального машстабирования при увеличинии нагрузки на сервис
  * Более гибкий подход к управлению моделью
* **Минусы**
  * При необходимости выполнять сложные аналитически запросы по нескольким коллекциям - нужно будет реализовывать дополнительную логику
  * Повышенный порог вхождения для данной технологии
  
### Нереляционная БД BASE на основе CassandraDB - вариант AP

* **Плюсы**
  * Поддержка горизонтального машстабирования при увеличинии нагрузки на сервис
  * Нет единой точки отказа (в отличии от других вариантов)
  * База оптимизирована на операции записи больше, чем на операции чтения
* **Минусы**
  * Слабая поддержка ограничений данных на уровне модели
  * Слабая структурироемость модели - в грубом приближении это скорее key-value база
  * Нет возможности использовать объединения в запросах - модель должна быть денормализована

## Решение
<!-- Описание выбранного решения. Решение должно быть сформулировано чётко ("Мы используем...", "Мы не используем", а не "Желательно.." или "Предлагается..."). 
Должна быть понятна связь между решением и проблемой, почему выбрали именно это решение из вариантов -->

В проекте helloconf Мы используем реляционную СУБД для микросервисов работы с конференциями, докладами и пользователями. Максимальный объем данных ожидается для 
регистраций онлайн пользователей. Согласно QR.005 - это количество не более 100к регистраций на одну конференцию.
В рамках ADR были проведены предварительные тесты, показывающие, что такой объем информации позволяет удовлетворить критерий QR.009.

Основные бизнес-сущности - пользователи, заявки на конференции, workflow заявки - подразумевают транзакционность, поэтому использование ACID базы - позволяет достичь этого с минимальным участием со стороны сервисного слоя.
В отличии о ACID - BASE больше подойдет для некритичных данных с большой нагрузкой. Например, комментарии пользователей к конференции. Решение о выборе базы для микросервиса комментариев - вынесено в отдельный ADR.

Дополнительным фактором влияющим на принятие решения - является поддержка выбранно СУБД как RDS ресурса на корпоративной
облачной платформе.

Также нам необходима поддержка ссылочной целостности на уровне базы - чего не могут обеспечить NoSQL базы. Иначе пришлось бы транзационную бизнес логикуу переносить в сервисный слой, что существенно усложняет разработку.

## Последствия
<!-- Положительные и отрицательные последствия (trade-offs). Арх. решения, которые потребуется принять как следствие принятого решения. Если решение содержит риски, то описано, как с ними планируют поступить (за счет чего снижать, почему принять). -->

Использование традиционной реляционной модели - уменьшает гибкость в модификации модели данных. Требуется скрипты миграции.