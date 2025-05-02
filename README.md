
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
* `/film_size` `GET` Получить количество фотопленок
  * `Ответ`
  ```json
  {
    "error": ... ,
    "message": ...,
    "content": количество фотопленки
  }
  ```

* `/film_list` `POST` Получить список фотопленок
  * `Запрос`
  ```json
    {
      "start": стартовая позиция,
      "end": конечная позиция 
    }
    ```
  * `Ответ` 
  ```json 
    {
      "error": ... ,
      "message": ...,
      "content": {
        "len" "размер_списка",
        "list"[
          ["name":]
        ]   
      }    
    }
    ```
* `/recepts_by_name` `POST` Получить рецепт определенной фотопленки
  * `Запрос`
  ```json
    {
      "name": "Название фотопленки",
      "idx" ...
    }
    
    "idx" - индекс записи рецепта в бд. для итерации. -1 вернет весь список
    ```
  * `Ответ`
  ```json
    {
      "error": ... ,
      "message": ...,
      "content": [
        рецепт 1,
        рецепт 2,
        ...
        ] 
    }
  ```


## Docker
### 1. Сборка
```bash
sudo docker build --network=host -t aaf_server .
```

### 2. Запуск
```bash
sudo docker run -d -p 5000:5000  aaf_server
```