
# AAF рус. ААФ (Автоматическая Агитация Фотобачка) серверная часть
Данный проект является серверной реализацией AAF.

Сервер написан на Python3 с использованием Flask, SQLite (см [`requirements.txt`](./requirements.txt))
## БД
Таблица `Film_recept`
```SQL
CREATE TABLE "Film_recept" (
	"Film"	TEXT,
	"Developer"	TEXT,
	"Dilution"	TEXT,
	"ISO"	INTEGER,
	"mm35"	TEXT,
	"mm120"	TEXT,
	"Sheet"	TEXT,
	"Temp"	TEXT,
	"Notes"	TEXT,
	"Forword_recept"	TEXT
);
```
## Сервер
### Общее
Общение между клиентом и сервером осуществляется посредством `json`

`Ответ` имеет вид:
```json
{
"error": True/False,
"message" : "Сообщение",
"сontent" : "Контент"
}
```
### Роуты

* `/check` `GET` Проверка состояния сервера
  * `Ответ` ok

* `/forward` `GET` Список избранных рецептов


## Docker
### 1. Сборка
```bash

```