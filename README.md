# DevPayCheck
Данный скрипт позволяет просмотреть актуальную статистику по средней заработной плате, среди разработчиков популярных языков программирования.

## Как установить
Python 3.10+ должен быть уже установлен. Затем используйте `pip` для установки зависимостей:
```bash
pip install -r requirements.txt
```
Для разработки использовалась Python 3.10. Версии выше 3.10 не тестировались.

## Переменные окружения
Требуется создать файл `.env` и прописать следующие переменные окружения:
- SJ_SECRET_KEY=your_superjob_secret_key
- SJ_ACCESS_TOKEN=your_superjob_access_token

О том где их получить, подробнее [Здесь](https://api.superjob.ru/#gettin)

## Скрипты и их запуск
Для запуска, введите в консоль:
```bash
python main.py
```
Программа обрабатывает заработные платы вакансий в г.Москва по языкам программирования:
- Python 
- Javascript
- 1C
- ruby
- C
- C#
- C++
- PHP

Пример вывода:

![2025-04-19_01-37-07](https://github.com/user-attachments/assets/f93da95a-623c-45f4-a8e3-e19ab8eb0428)
