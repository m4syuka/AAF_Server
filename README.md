
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
	"ISO"	TEXT,
	"mm35"	TEXT,
	"mm120"	TEXT,
	"Sheet"	TEXT,
	"Temp"	TEXT,
	"Notes"	TEXT,
	"Film_selector"	TEXT,
	"Myself_recept"	TEXT,
	"Forward"	TEXT
);
```
Таблица `Film_selector_name`
```SQL
CREATE TABLE "Film_selector_name" (
	"url"	TEXT,
	"name"	TEXT
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


* `/get_selector_list` `GET` Получить список фотопленок из селектора
  * `Ответ` Cписок фотопленок из селектора


* `/get_recepts_by_selector`  `POST` Получить список рецептов фотопленок
    * `Запрос`
    ```json
    {
    "selector": "название фотопленки из селектора"
    }
    ```

  * `Ответ` Список рецептов фотопленок


* `/forward` `GET` Список избранных рецептов


* `/myself` `GET` Список созданных мной рецептов