# 📨 Сервис управления рассылками

Веб-приложение на Django для управления рассылками сообщений клиентам. Позволяет создавать клиентов, сообщения и рассылки, а также отправлять их вручную через интерфейс или командную строку.

---

## 📌 О проекте

**Сервис управления рассылками** — это учебный проект, разработанный в рамках курса по Django. Приложение демонстрирует применение фреймворка для создания CRUD-интерфейса, работы с моделями, связями «многие ко многим», отправки email и ведения статистики попыток рассылок.

### Текущий этап разработки

- ✅ Настройка проекта и виртуального окружения
- ✅ Создание приложения `mailing`
- ✅ Модели: `Client`, `Message`, `Mailing`, `MailingAttempt`
- ✅ CRUD для всех моделей через CBV
- ✅ Главная страница со статистикой
- ✅ Формы через `ModelForm`
- ✅ Логика отправки (`services.py`)
- ✅ Management command `send_mailing`
- ✅ Админка для всех моделей
- ✅ Конфигурация через `.env`
- 🔄 В разработке (Часть 2): аутентификация, права доступа, кэширование

---

## 🛠 Технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| Python | 3.10+ | Язык программирования |
| Django | 4.2+ | Веб-фреймворк |
| SQLite | 3 | База данных (разработка) |
| Bootstrap | 5.3 | CSS-фреймворк |
| python-dotenv | 1.0+ | Переменные окружения |
| Git | — | Система контроля версий |

---

## 📂 Структура проекта
```
Mailing_service/
├── manage.py
├── requirements.txt
├── .env
├── .env.template
├── .gitignore
├── README.md
├── db.sqlite3
│
├── config/ # Настройки проекта
│ ├── init.py
│ ├── settings.py # Настройки (БД, EMAIL, TEMPLATES)
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
└── mailing/ # Приложение "Рассылки"
├── init.py
├── admin.py # Регистрация моделей в админке
├── apps.py
├── models.py # Client, Message, Mailing, MailingAttempt
├── forms.py # ModelForm для всех моделей
├── views.py # CBV + send_mailing_view
├── urls.py # Маршруты приложения
├── services.py # Логика отправки рассылки
├── tests.py
├── migrations/
├── management/
│ └── commands/
│ ├── init.py
│ └── send_mailing.py # Команда отправки по ID
└── templates/mailing/
├── base.html # Базовый шаблон
├── home.html # Главная со статистикой
├── client_list.html
├── client_form.html
├── client_confirm_delete.html
├── message_list.html
├── message_form.html
├── message_confirm_delete.html
├── mailing_list.html
├── mailing_form.html
└── mailing_confirm_delete.html

```

---

## 🌐 Доступные страницы

### Основные

| Страница | URL | Контроллер |
|:---------|:----|:-----------|
| Главная (статистика) | `/` | `HomeView` |
| Клиенты | `/clients/` | `ClientListView` |
| Сообщения | `/messages/` | `MessageListView` |
| Рассылки | `/mailings/` | `MailingListView` |
| Админка | `/admin/` | — |

### CRUD

| Действие | Клиенты | Сообщения | Рассылки |
|:---------|:--------|:----------|:---------|
| Создать | `/clients/create/` | `/messages/create/` | `/mailings/create/` |
| Редактировать | `/clients/<int:pk>/update/` | `/messages/<int:pk>/update/` | `/mailings/<int:pk>/update/` |
| Удалить | `/clients/<int:pk>/delete/` | `/messages/<int:pk>/delete/` | `/mailings/<int:pk>/delete/` |
| Отправить | — | — | `/mailings/<int:pk>/send/` |

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/mailing-service.git
cd mailing-service
```
### 2. Создание виртуального окружения
Windows:

```bash
python -m venv venv
venv\Scripts\activate
macOS/Linux:
```
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Настройка .env
~~~
Создайте .env на основе .env.template:

~~~
### 5. Применение миграций
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Создание суперпользователя
```bash
python manage.py createsuperuser
```
### 7. Запуск сервера
```bash
python manage.py runserver
```
Откройте http://127.0.0.1:8000/ — главная страница со статистикой.

## 📨 Отправка рассылки
### Через интерфейс
#### 1. Создайте клиента (/clients/create/)

#### 2. Создайте сообщение (/messages/create/)

#### 3. Создайте рассылку (/mailings/create/) — выберите сообщение и получателей

#### 4. На странице /mailings/ нажмите кнопку 📤

## Через командную строку
```bash
python manage.py send_mailing <id>
```
### Пример:

```bash
python manage.py send_mailing 1
```
## Как это работает
#### 1. Для каждого получателя вызывается send_mail()

#### 2. При успехе создаётся MailingAttempt со статусом success

#### 3. При ошибке — MailingAttempt со статусом failed и текстом ошибки

#### 4. Если рассылка была created, статус меняется на started

# 📋 Модели данных

### Client (Получатель)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `email` | `EmailField` | Email (уникальный) |
| `full_name` | `CharField` | Ф. И. О. |
| `comment` | `TextField` | Комментарий |

### Message (Сообщение)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `subject` | `CharField` | Тема письма |
| `body` | `TextField` | Тело письма |

### Mailing (Рассылка)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `start_time` | `DateTimeField` | Дата и время первой отправки |
| `end_time` | `DateTimeField` | Дата и время окончания отправки |
| `status` | `CharField` | Статус (`created`, `started`, `completed`) |
| `message` | `ForeignKey` | Сообщение |
| `recipients` | `ManyToManyField` | Получатели |

### MailingAttempt (Попытка рассылки)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `attempt_time` | `DateTimeField` | Дата и время попытки |
| `status` | `CharField` | Статус (`success`, `failed`) |
| `server_response` | `TextField` | Ответ почтового сервера |
| `mailing` | `ForeignKey` | Рассылка |

---

## 🔧 Команды для разработки

| Команда | Описание |
|:--------|:---------|
| `python manage.py runserver` | 🚀 Запуск сервера |
| `python manage.py makemigrations` | 📦 Создание миграций |
| `python manage.py migrate` | 🗄️ Применение миграций |
| `python manage.py createsuperuser` | 👑 Создание администратора |
| `python manage.py shell` | 💻 Интерактивная оболочка |
| `python manage.py send_mailing <id>` | 📨 Отправка рассылки по ID |
| `pip freeze > requirements.txt` | 📋 Обновление зависимостей |
# 📝 Лицензия
### Этот проект является учебным и не предназначен для коммерческого использования.

# 👤 Автор
### Имя: Геннадий Кокаулин

### Email: Genchik691@gmail.com

### GitHub: https://github.com/genchik691