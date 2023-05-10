# Компонентная архитектура
<!-- Состав и взаимосвязи компонентов системы между собой и внешними системами с указанием протоколов, ключевые технологии, используемые для реализации компонентов.
Диаграмма контейнеров C4 и текстовое описание. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375783368
-->
## Контейнерная диаграмма

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

AddElementTag("microService", $shape=EightSidedShape(), $bgColor="CornflowerBlue", $fontColor="white", $legendText="microservice")
AddElementTag("storage", $shape=RoundedBoxShape(), $bgColor="lightSkyBlue", $fontColor="white")
AddElementTag("bus", $shape=RoundedBoxShape(), $bgColor="RoyalBlue", $fontColor="white", $legendText="Event Bus")
AddElementTag("front", $shape=RoundedBoxShape(), $bgColor="navy", $fontColor="white", $legendText="Front-End Module")

Person(listener, "Слушатель", "Посетитель конференции")
Person(speaker, "Докладчик", "Докладчик")
Person(reviewer, "Модератор", "Обрабатывает заявки, отвечает на комментарии")
Person(master, "Администратор", "Создает новые конференции, осуществляет настройку параметров конференции")

System_Boundary(c, "HelloConf") {
   System_Boundary(u, "UserContext") {
      Container(userWeb, "User Front-End Module", "Angular/NodeJS", "Модуль управления регистрациями, участниками", $tags = "front")
      Container(userService, "User Service", "Java, Spring Boot", "Сервис управления пользователями", $tags = "microService")  
      
      ContainerDb(userServiceDb, "User Database", "PostgreSQL", "Хранение пользовательских данных", $tags = "storage")    
   }

   System_Boundary(cs, "ConferenceContext") {
       Container(conferenceWeb, "Conference Front-End Module", "Angular/NodeJS", "Модуль управления конференциями и докладами", $tags ="front")
       Container(conferenceService, "Conference Service", "Java, Spring Boot", "Сервис управления конференциями и докладами", $tags = "microService")      
       ContainerDb(conferenceServiceDb, "Conference Database", "PostgreSQL", "Хранение данных о конференции и докладах", $tags = "storage")
   }


   System_Boundary(busContext, "Bus Context (Shared Kernel)") { 
     Container(messageBus, "Message Bus", "RabbitMQ", "Транспорт для бизнес-событий", $tags = "bus")
   }


   System_Boundary(sc, "SocializingContext") {
       Container(commentWeb, "Comment/Socializing Front-End Module", "Angular/NodeJS", "Модуль социальных коммуникаций", $tags = "front")
       Container(commentService, "Comment Service", "Java, Spring Boot, Cassandra", "Сервис хранения комментариев", $tags = "microService")
       ContainerDb(cassandra, "Social Activity Db", "Cassandra", "Хранение данных о социальных активностях пользователей", $tags = "storage")
       Rel_D(commentService, cassandra, "")
   }

}

System_Ext(mtsSso, "SSO System", "Авторизация как пользователя МТС")
System_Ext(streamingSystem, "WASD", "Стриминговая платформа")  
System_Ext(sometubeSystem, "Video Hosting", "Платформа хостинга offline-видео")  

Rel(listener, userWeb, "Регистрация, получения подтверждения о регистраци и уведомлений", "HTTPS")
Rel(speaker, conferenceWeb, "Отправка заявки на доклад, получение обратной связи", "JSON, HTTPS")
Rel(reviewer, conferenceWeb, "Просмотр заявки, отправка обратной связи, модерация комментариев", "JSON, HTTPS")
Rel(master, conferenceWeb, "Создание новые конференций, заполнение информации")

Rel(conferenceWeb, conferenceService, "Работа с докладами и конференциями")
Rel(userWeb, userService, "Авторизация и регистрация")
BiRel(commentWeb, commentService, "Получение и сохранение комметариев")
Rel_L(conferenceService, streamingSystem, "Получение потока данных Live")
Rel_R(conferenceService, sometubeSystem, "Получение видео")

BiRel(userService, mtsSso, "Авторизация и получение основной информации")

Rel_L(conferenceService, messageBus, "События модерации доклада и изменение его статуса", "AMPQ")
Rel_R(messageBus, commentService, "Получение событий жизненного цикла доклада, конференции")

BiRel(conferenceService, conferenceServiceDb, "Сохранение и редактирование данных о конференции, докладе", "Hibernate, SQL")

BiRel(userService, userServiceDb, "Хранение расширенных данных пользователя")

SHOW_LEGEND()
@enduml
```

## Список компонентов
| Компонент             | Роль/назначение                  |
|:----------------------|:---------------------------------|
| *Сервис работы с конференциями* | *Создание конференции, работа с заявками на доклад, работа с расписанием* |
| *Сервис работы с участниками* | *Регистрация пользователей, интеграция с SSO, уведомления о событиях* |
| *Сервис социальной активности* | *Поддержка возможности для пользователей оставлять комментарии, реакции и ответы* |