# Контекст решения
<!-- Окружение системы (роли, участники, внешние системы) и связи системы с ним. Диаграмма контекста C4 и текстовое описание. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375783261
-->
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

LAYOUT_WITH_LEGEND()

Person(visitor, "Visitor", "An offline participant (visitor) of the conference")
Person(listener, "Listener", "An online participant (registered) of the conference")
Person(speaker, "Speaker", "A person who presents his topic")
Person(moderator, "Moderator", "A person who supports conference request processing - approving, communicating and scheduling")

System(helloconf, "HelloConf conference platform", "Brand new modern conference platform")
System(streaming, "Streaming platform providing real-time audio/video broadcasting")
System(sometube, "Video hosting platform to store video presentation afterwards")
System(email, "E-mail gateway", "Send notification to the all type of users: request workflow-related events, confirmation events etc")
System(sms, "SMS gateway", "Send notifications to speakers in case of important updates")
ContainerDb(db, "Database", "PostgresSQL", "Storage for the conference model entities")


Rel(visitor, helloconf, "Registers and writes feedback")
Rel(listener, helloconf, "Registers")
Rel(speaker, helloconf, "Registers and receives request lifecycle notifications")
Rel(moderator, helloconf, "Processes requests")
Rel(helloconf, streaming, "Uses for streaming live video")
Rel(helloconf, sometube, "Uses for storing edited video")
Rel(helloconf, email, "Delivers email notifations")
Rel(helloconf, sms, "Delivers urgent notifications")
Rel(helloconf, db, "Handled CRUD operations")
Rel(email, visitor, "Receives confirmations of participance")
Rel(email, speaker, "Receives confirmation of participance and workflow-related events")
Rel(sms, speaker, "Receives workflow-related events")
@enduml
```
