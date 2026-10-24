# 📨 Сервис управления рассылками

Веб-приложение на Django для управления рассылками сообщений клиентам. Позволяет создавать клиентов, сообщения и рассылки, отправлять их вручную, отслеживать статистику и разграничивать права доступа.

---

## 📌 О проекте

**Сервис управления рассылками** — учебный проект (курсовая работа) по Django. Приложение демонстрирует полный цикл разработки: модели, CRUD, формы, аутентификацию с подтверждением email, роли, отправку писем и кэширование.

### ✅ Что реализовано

| Часть | Функционал |
|:------|:-----------|
| **1. Разработка сервиса** | Модели, CRUD, отправка, batch-попытки, главная |
| **2. Расширение** | Аутентификация, роли, статистика, кэширование |
| **Финальные доработки** | Валидация времени, менеджерские функции |

---

## 🛠 Технологии

| Технология | Версия | Назначение |
|:-----------|:------:|:-----------|
| Python | 3.10+ | Язык программирования |
| Django | 4.2+ | Веб-фреймворк |
| SQLite | 3 | База данных (разработка) |
| Bootstrap | 5.3 | CSS-фреймворк |
| python-dotenv | 1.0+ | Переменные окружения |
| Git | — | Система контроля версий |

---

## 📂 Структура проекта
````
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
│ ├── settings.py # БД, EMAIL, CACHES, AUTH_USER_MODEL
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
└── mailing/ # Приложение "Рассылки"
├── init.py
├── admin.py # Регистрация моделей
├── apps.py
├── models.py # Client, Message, Mailing, MailingAttempt, User
├── forms.py # ModelForm + валидация
├── views.py # CBV + менеджерские функции
├── urls.py # Маршруты
├── services.py # Отправка рассылок
├── tests.py
├── migrations/
├── management/
│ └── commands/
│ ├── init.py
│ └── send_mailing.py # Команда отправки
└── templates/mailing/
├── base.html
├── home.html
├── register.html
├── login.html
├── password_reset.html
├── password_reset_done.html
├── password_reset_confirm.html
├── password_reset_complete.html
├── password_reset_email.html
├── client_list.html
├── client_form.html
├── client_confirm_delete.html
├── message_list.html
├── message_form.html
├── message_confirm_delete.html
├── mailing_list.html
├── mailing_form.html
├── mailing_detail.html
├── mailing_confirm_delete.html
├── statistics.html
└── user_list.html

````

---

## 🌐 Доступные страницы

### Основные

| Страница | URL | Доступ |
|:---------|:----|:------:|
| Главная (кэш 5 мин) | `/` | 🌍 |
| Статистика (кэш 5 мин) | `/statistics/` | 🔒 |
| Клиенты | `/clients/` | 🔒 |
| Сообщения | `/messages/` | 🔒 |
| Рассылки | `/mailings/` | 🔒 |
| Пользователи (менеджер) | `/users/` | 🔒 Менеджер |
| Админка | `/admin/` | 🔒 |

### CRUD

| Действие | Клиенты | Сообщения | Рассылки |
|:---------|:--------|:----------|:---------|
| Создать | `/clients/create/` | `/messages/create/` | `/mailings/create/` |
| Просмотр | — | — | `/mailings/<int:pk>/` |
| Редактировать | `/clients/<int:pk>/update/` | `/messages/<int:pk>/update/` | `/mailings/<int:pk>/update/` |
| Удалить | `/clients/<int:pk>/delete/` | `/messages/<int:pk>/delete/` | `/mailings/<int:pk>/delete/` |
| Отправить | — | — | `/mailings/<int:pk>/send/` |
| Отключить | — | — | `/mailings/<int:pk>/toggle/` |

### Аутентификация

| Страница | URL |
|:---------|:----|
| Регистрация | `/register/` |
| Вход | `/login/` |
| Выход | `/logout/` |
| Подтверждение email | `/confirm-email/<int:token>/` |
| Восстановление пароля | `/password-reset/` |

> 🌍 — доступно всем · 🔒 — только для авторизованных

---

## 🚀 Запуск проекта

### 1. Клонирование

```bash
git clone https://github.com/your-username/mailing-service.git
cd mailing-service
```
2. Виртуальное окружение
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
3. Зависимости
```bash
pip install -r requirements.txt
```
4. .env
Создайте .env на основе .env.template:

env
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@mailing-service.ru
5. Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Группа «Менеджеры»
```bash
python manage.py shell -c "from django.contrib.auth.models import Group; Group.objects.get_or_create(name='Менеджеры'); print('OK')"
```
7. Суперпользователь
```bash
python manage.py createsuperuser
```
8. Запуск
```bash
python manage.py runserver
Откройте http://127.0.0.1:8000/ — главная страница со статистикой.

📨 Отправка рассылки
Через интерфейс
Шаг	Действие
1	Создайте клиента (/clients/create/)
2	Создайте сообщение (/messages/create/)
3	Создайте рассылку (/mailings/create/)
4	Нажмите 📤 на странице /mailings/
```
Через командную строку
```bash
python manage.py send_mailing <id>
```
Пример:

```bash
python manage.py send_mailing 1
Логика отправки
Этап	Что происходит
1	Проверка start_time <= now <= end_time
2	Для каждого получателя — send_mail()
3	Успех → MailingAttempt(success)
4	Ошибка → MailingAttempt(failed) + текст ошибки
5	bulk_create() для всех попыток (batch)
6	update_status() для рассылки
```
## 📋 Модели данных

### 👤 Client (Получатель)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `email` | `EmailField` | Email (уникальный) |
| `full_name` | `CharField` | Ф. И. О. |
| `comment` | `TextField` | Комментарий |
| `owner` | `ForeignKey` | Владелец |

### ✉️ Message (Сообщение)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `subject` | `CharField` | Тема письма |
| `body` | `TextField` | Тело письма |

### 📨 Mailing (Рассылка)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `start_time` | `DateTimeField` | Дата и время первой отправки |
| `end_time` | `DateTimeField` | Дата и время окончания отправки |
| `status` | `CharField` | Статус (`created`, `started`, `completed`) |
| `message` | `ForeignKey` | Сообщение |
| `recipients` | `ManyToManyField` | Получатели |
| `owner` | `ForeignKey` | Владелец |

### 🔄 MailingAttempt (Попытка рассылки)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `attempt_time` | `DateTimeField` | Дата и время попытки |
| `status` | `CharField` | Статус (`success`, `failed`) |
| `server_response` | `TextField` | Ответ почтового сервера |
| `mailing` | `ForeignKey` | Рассылка |

### 👤 User (Пользователь)

| Поле | Тип | Описание |
|:-----|:----|:---------|
| `email` | `EmailField` | Email (уникальный, `USERNAME_FIELD`) |
| `username` | `CharField` | Имя пользователя |
| `password` | `CharField` | Пароль (хэшируется) |
| `is_email_confirmed` | `BooleanField` | Email подтверждён |
| `is_active` | `BooleanField` | Активен |
| `is_staff` | `BooleanField` | Доступ в админку |
| `is_superuser` | `BooleanField` | Суперпользователь |

---

## 🔐 Роли и права доступа

### 👤 Пользователь

| Действие | Доступ |
|:---------|:------:|
| Создание, просмотр, редактирование, удаление **своих** клиентов | ✅ |
| Создание, просмотр, редактирование, удаление **своих** рассылок | ✅ |
| Просмотр статистики по своим рассылкам | ✅ |
| Просмотр чужих клиентов/рассылок | ❌ |
| Редактирование/удаление чужих | ❌ |

### 🛡️ Менеджер (группа «Менеджеры»)

| Действие | Доступ |
|:---------|:------:|
| Просмотр всех клиентов и рассылок | ✅ |
| Просмотр списка пользователей | ✅ |
| Блокировка пользователей | ✅ |
| Отключение рассылок | ✅ |
| Редактирование/удаление чужих | ❌ |

> 👤 — обычный пользователь · 🛡️ — менеджер

## ⚡ Кэширование
### Настройки
``` python
# config/settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```
## ⚡ Что кэшируется

| Страница | Метод | Время |
|:---------|:------|------:|
| Главная | `@cache_page(60 * 5)` | 5 минут |
| Статистика | `@cache_page(60 * 5)` | 5 минут |
| Клиентское | `Cache-Control: public, max-age=300` | 5 минут |

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
| `python manage.py collectstatic` | 📁 Сбор статики |
| `pip freeze > requirements.txt` | 📋 Обновление зависимостей |

## ✅ Проверка работоспособности
```bash
# 1. Проверка синтаксиса и конфигурации
python manage.py check
# System check identified no issues (0 silenced).

# 2. Миграции
python manage.py makemigrations
python manage.py migrate

# 3. Запуск
python manage.py runserver
```
## ✅ Сценарии для проверки

| № | Сценарий | Ожидание |
|:-:|:---------|:---------|
| 1 | Рассылка с `start_time` в прошлом | ❌ Ошибка валидации |
| 2 | Рассылка с `start_time >= end_time` | ❌ Ошибка валидации |
| 3 | Отправка вне временного окна | ❌ Ошибка «Отправка запрещена» |
| 4 | Отправка в окне | ✅ Письма в консоли + попытки в БД |
| 5 | Пользователь A открывает клиента B | 🚫 403 Forbidden |
| 6 | Менеджер открывает `/users/` | ✅ Список пользователей |
| 7 | Менеджер блокирует пользователя | ✅ Пользователь не может войти |
| 8 | Менеджер отключает рассылку | ✅ Статус меняется |
| 9 | Главная и статистика | ⚡ Кэшируются 5 минут |

# 📝 Лицензия
#### Этот проект является учебным и не предназначен для коммерческого использования.
# 👤 Автор
### Имя: Геннадий Кокаулин
### Email: Genchik691@gmail.com
### GitHub: https://github.com/genchik691