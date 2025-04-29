
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
	"Forward_recept"	TEXT
);

CREATE UNIQUE INDEX "idx_full_unique" ON "Film_recept" (
	"Film",
	"Developer",
	"Dilution",
	"ISO",
	"mm35",
	"mm120",
	"Sheet",
	"Temp",
	"Notes",
	"Forward_recept"
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

* `/film_list` `GET` Получить список фотопленок
  * `Ответ` 
  * ```json 
    {
      "error": ... ,
      "message": ...,
      "content": {
        [recept],
        [recept],
        ...  
      }    
    }
    ```
* `/get_by_name` `GET` Получить рецепт определенной фотопленки
  * `Запрос`
  * ```json
    {
      "name": "Название фотопленки"
    }
    ```


## Docker
### 1. Сборка
```bash

```