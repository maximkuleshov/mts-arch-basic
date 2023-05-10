# Контекст решения
<!-- Окружение системы (роли, участники, внешние системы) и связи системы с ним. Диаграмма контекста C4 и текстовое описание. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375783261
-->

## Контекстная диаграмма (C4 Context)

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

Person(visitor, "Visitor", "Очный посетитель конференции ")
Person(listener, "Listener", "Зарегистрированный online-слушатель конференции")
Person(speaker, "Speaker", "Докладчик, который презентует свою тему на конференции")
Person(moderator, "Moderator", "Модератор, который просматриваеи заявки, предоставляет обратную связь и управлеят расписанием")

System(helloconf, "Платформа конференций HelloConf", "Современнмая платформа конференций")
System_Ext(streaming, "Стриминговая платформа для организации живой трансляции в Интернет")
System_Ext(sometube, "Платформа хранения записанных видео докладов")
System_Ext(email, "E-mail шлюз", "Отправляет уведомления о событиях с заявкой, подтверждении регистрации и другое")
System_Ext(sms, "SMS gateway", "Отправляет уведомления Докладчикам о важных изменениях - статус заявки, расписание")
System_Ext(sso, "SSO system", "Авторизация пользователей по корпоративному стандарту")
ContainerDb(db, "Database", "PostgresSQL", "База для хранения основных бизнес сущностей")
ContainerDb(cassandra, "High Performance Db", "CassandraDB", "База для хранения социальной активности")


Rel_D(visitor, helloconf, "Регистрируется и пишет комментарии, получает подтверждение участия")
Rel_D(listener, helloconf, "Регистрируется, получает ссылку на online-трансляци, может писать комментарии")
Rel_D(speaker, helloconf, "Регистрируется и проходит этап согласования доклада")
Rel_D(moderator, helloconf, "Обрабатывает заявки")
Rel_U(visitor, sso, "Регистрация и авторизация")
Rel_U(listener, sso, "Регистрация и авторизация")
Rel_U(speaker, sso, "Регистрация и авторизация")
Rel_U(moderator, sso, "Регистрация и авторизация")
Rel(helloconf, streaming, "Использует стриминговую платформу")
Rel(helloconf, sometube, "Используется для хранения видео")
Rel_L(helloconf, email, "Доставляение уведомления по email")
Rel_R(helloconf, sms, "Доставляет уведомления по SMS")
Rel(helloconf, db, "Обрабатывает операции с данными")
Rel(helloconf, cassandra, "Операции с комментариями")
Rel_U(email, visitor, "Получает подтверждение регистрации и участия")
Rel_U(email, speaker, "Получеет подтверждение регистрации и обновление статуса заявки")
Rel_U(sms, speaker, "Получает уведомления о событиях с заявкой на доклад")
@enduml
```

## Список выделенных контекстов

* Контекст участников (пользователей). Включает в себя supporting subdomain в виде SSO системы МТС. Но сохраняет дополнительную информацию о пользователях, полезную, например, для HR службы. Также для докладчиков сохрняется краткое описание их опыта, ссылка на портфолио и другие сведения полезные в процессе презентации доклада
* Контекст конференции. Включает в себя supporting subdomain платформ хранения и стриминга видео (WASD)
* Контекст социальных коммуникаций внутри платформы. Это любая активность участников всех типов в рамках конференции - комментарии, лайки, ответы и реакции.

## Диаграмма ограниченных контекстов
  
<!-- Диаграмма ограниченных контекстов -->

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

' skinparam linetype polyline
LAYOUT_WITH_LEGEND()


Person(moderator, "Модератор", "Модератор, который просматриваеи заявки, предоставляет обратную связь и управлеят расписанием")
Person(participant, "Участник конференции", "Онлайн, Оффлайн и докладчик")

System_Boundary(helloconf,"Платформа конференций HelloConf", "Современнмая платформа конференций") {
    Container(userContext, "Контекст участников", "", "Регистрация онлайн, оффлайн посетителей и докладчиков")
    Container(conferenceContext, "Контекст конференций", "", "Управление конференциями, жизненный цикл и модерация]")
    Container(socializingContext, "Контекст общения участников", "", "Комментарии к докладам, ревью докладов со стороны модераторов")
}

System_Ext(sso, "SSO system", "Авторизация пользователей по корпоративному стандарту")
System_Ext(streaming, "Стриминговая платформа для организации живой трансляции в Интернет")
System_Ext(sometube, "Платформа хранения записанных видео докладов")
System_Ext(sms, "Шлюз отправки уведомлений через SMS")
System_Ext(email, "Шлюз отправки уведомлений через Email")

Rel(userContext, conferenceContext, "Привязка докладов и расписания к пользователям-участникам")
Rel(userContext, socializingContext, "Привязка социальной активности к пользователям-участникам")


Rel(participant, userContext, "Регистрируется как участник")
Rel_U(userContext, sso, "Создание учетной записи и аутентификация")
Rel_U(moderator, conferenceContext, "Создание конференции, рецензирует доклады, дает обратную связь")
Rel_D(conferenceContext, streaming, "Использует стриминговую платформу")
Rel_D(conferenceContext, sometube, "Используется для получение для доступа к сохраненным видео") 

Rel(participant, socializingContext, "Используется для коммуникации")
Rel(moderator, socializingContext, "Используется для коммуникации")
Rel_L(conferenceContext, sms, "Уведомление о событиях модерации")
Rel_R(socializingContext, email, "Уведомления о события социального контекста")

@enduml
```