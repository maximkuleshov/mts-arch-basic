# Контекст решения
<!-- Окружение системы (роли, участники, внешние системы) и связи системы с ним. Диаграмма контекста C4 и текстовое описание. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375783261
-->
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

Person(visitor, "Visitor", "Очный посетитель конференции ")
Person(listener, "Listener", "Зарегистрированный online-слушатель конференции")
Person(speaker, "Speaker", "Докладчик, который презентует свою тему на конференции")
Person(moderator, "Moderator", "Модератор, который просматриваеи заявки, предоставляет обратную связь и управлеят расписанием")

System(helloconf, "Платформа конференций HelloConf", "Современнмая платформа конференций")
System(streaming, "Стриминговая платформа для организации живой трансляции в Интернет")
System(sometube, "Платформа хранения записанных видео докладов")
System(email, "E-mail шлюз", "Отправляет уведомления о событиях с заявкой, подтверждении регистрации и другое")
System(sms, "SMS gateway", "Отправляет уведомления Докладчикам о важных изменениях - статус заявки, расписание")
System(sso, "SSO system", "Авторизация пользователей по корпоративному стандарту")
ContainerDb(db, "Database", "PostgresSQL", "База для хранения бизнес сущностей")


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
Rel_U(email, visitor, "Получает подтверждение регистрации и участия")
Rel_U(email, speaker, "Получеет подтверждение регистрации и обновление статуса заявки")
Rel_U(sms, speaker, "Получает уведомления о событиях с заявкой на доклад")
@enduml
```
