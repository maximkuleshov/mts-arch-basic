# Модель предметной области
<!-- Логическая модель, содержащая бизнес-сущности предметной области, атрибуты и связи между ними. 
Подробнее: https://confluence.mts.ru/pages/viewpage.action?pageId=375782602

Используется диаграмма классов UML. Документация: https://plantuml.com/class-diagram 
-->

```plantuml
@startuml
' Логическая модель данных в варианте UML Class Diagram (альтернатива ER-диаграмме).
namespace HelloConf {

enum AttendeeStatus
 {
  unconfirmed
  confirmed
  registered
  participated
  cancelled
 }

 enum TopicStatus {
    sent
    approving
    approved
    rejected
 }

 class User {
  id : string
  fullName: string
  phone: string
  email: string
  status: AttendeeStatus
 }

 class Listener extends User {
 }

 class Visitor extends User {
 }

 class Speaker extends User {
    about: string
    company: string
    position: string
 }

 class Topic {
    title : string
    pptFile: binary
    createDate: date
    speaker: Speaker
    status: TopicStatus
    url: string
 }

 class ReviewComment {
    comment: string
    createdAt: datetime
    createdBy: User
    replyTo: ReviewComment
 }

 class Request {
    createdAt: datetime
    topic: Topic
    speaker: Speaker
 }

 class Conference {
    id: string
    title: string
    description: string
    startDate: date
    endDate: date
 }

 class Participance {
    conference: Conference
    user: User
 }

 class Presentation {
    topic: Topic
    dateTime: dateTime
 }

 class Schedule {
    conference: Conference
 }

 class Partner {
    name: string
    description: string
 }

 class Feedback {
    topic: Topic
    author: User
 }

 ReviewComment "1" *-- "1" User
 ReviewComment "1" *-- "0..1" ReviewComment

 Request "1" o-- "*" ReviewComment
 Request "1" *-- "1" Topic
 Request "1" *-- "1" Speaker

 Conference "1" *-- "*" Participance

 Partner "*" *-- "*" Conference

 Participance "1" *-- "1" User

 Presentation "1" *-- "1" Conference
 Presentation "1" *-- "1" Speaker

 Schedule "1" o-- "*" Presentation
 Schedule "1" *-- "1" Conference

 Feedback "*" *-- "1" Topic
 Feedback "1" *-- "1" User
 
@enduml
```
