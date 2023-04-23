# ADR.002

Выбор шаблона интеграции

<!-- Название ADR состоит из [ADR.###] [Коротко суть принятого решения] -->

* Статус: Предложено
* Владелец: mekuleshov@mts.ru

## Контекст
<!-- Описание проблемы, требующей решения, причин, побудивших принять решение, ограничений, действовавших на момент принятия решения -->
Необходимо проанализировать, какой из способов межсервисного взаимодействия более подходящий для разрабатываемой системы helloconf

## Варианты решения
<!-- Описание рассмотренных вариантов c их плюсами и минусами -->

### Чистый REST API over HTTP1

Межсервисное взаимодействие (фронтэнд-бекенд) и (бекенд-бекенд) строится исключительно на синхронных вызовах по HTTP/REST API.

### gRPC over HTTP/2

Межсервисное взаимодействие через gRPC (включая front-end)

### GraphQL over 

Взаимодействие через GraphQL

## Сравнение

|                    | REST API                               | gRPC                             | GraphQL                                  |
|--------------------|----------------------------------------|----------------------------------|------------------------------------------|
| Накладные расходы на конвертацию | Средние, так как основной формат обмена данными - текстовый | Низкие - протокол бинарный | Среднее, также текстовый тип контента  |
| Объем данных       | Средний, достаточно сильная избыточность из текстовой природы | Низкий | Средний |
| Балансировка       | И клиентская и серверная | Для серверной баланисровки требуется поддержка HTTP2 | Балансировка по URL - да, более изощренные сложны в реализации |
| Поддержка асинхронных вызовов | Ограничена - только через повторные вызовы с клиента с проверкой статуса фоновой задачи | Да, из коробки | Асихнронность для отдельных операций запроса |

## Решение
<!-- Описание выбранного решения. Решение должно быть сформулировано чётко ("Мы используем...", "Мы не используем", а не "Желательно.." или "Предлагается..."). 
Должна быть понятна связь между решением и проблемой, почему выбрали именно это решение из вариантов -->
Мы используем для межсервисного взаимодействия REST API с балансировкой на уровне кластера. Исходя из доменной модели - не существует объектов с объемными и сложными структурами - таким образом дизайн API представляется понятной задачей и возможности GraphQL - избыточны. 
Нет потребности в экономии трафика - так как нет таких сценариев использования, где происходит интенсивный обмен между компонентами системы (кроме просмотра видео - которое обеспечивается сторонней платформой) - таким образом возможности gRPC также не дают преимуществ в нашем случае.

## Последствия
<!-- Положительные и отрицательные последствия (trade-offs). Арх. решения, которые потребуется принять как следствие принятого решения. Если решение содержит риски, то описано, как с ними планируют поступить (за счет чего снижать, почему принять). -->

Риски:

 * Возможность усложнения встроенного API при появлении потребностей в добавлении аналитических отчетов. Можно решать использованием готовых инструментов для анализа данных - например, Apache Superset. Достаточно будет описать источник данных или запрос на уровне СУБД.
 * Отсутствие настоящей асинхронности. В текущем дизайне системы нет мест, где бы она была нужна. Потенциально возможным местом появления асинхронных запросов или событий - получение уведомлений фронт-эндом от бекенда. Это может быть решено через SSE/WebSocket
