1 Вариант
***

# Описание Backend-приложения

## Технический стек
- **Язык программирования**: Python 3.11
- **Фреймворк**: Django REST Framework (DRF)
- **База данных**: SQLite3
- **Документация**: drf-spectacular (OpenAPI/Swagger)
- **Контейнеризация**: Docker
- **CI/CD**: GitHub Actions
- **Хостинг**: PythonAnywhere

## Развертывание
Приложение контейнеризировано с использованием Docker и развернуто на платформе PythonAnywhere. Настроены GitHub Actions для автоматизированного тестирования и сборки:
- `build.yml`: Отвечает за сборку Docker-образа и тестирование
- `python-tests.yml`: Запускает Python-тесты при push/pull запросах в ветки master и dev

## API Endpoints (Конечные точки)

### Аутентификация и пользователи
- Регистрация и аутентификация пользователей
- Управление профилями пользователей
- Контроль доступа на основе ролей (RBAC)
- Аутентификация на основе токенов

### Управление проектами
- **Проекты**: CRUD операции для проектов
- **Задачи**: Управление задачами с отслеживанием статуса
- **Комментарии**: Система комментирования задач
- **Элементы чек-листа**: Функционал чек-листов задач
- **Теги**: Тегирование и фильтрация задач

### Управление пользователями
- **Профили**: Управление профилями пользователей
- **Навыки**: Отслеживание навыков пользователей
- **Роли**: Управление ролями (Организатор, Руководитель и т.д.)
- **Заявки**: Обработка заявок
- **Отзывы**: Система рассмотрения заявок

### Отслеживание статуса и прогресса
- **Статусы**: Управление статусами задач
- **Эффективность**: Отслеживание эффективности пользователей
- **Результаты**: Отслеживание результатов задач
- **Направления**: Управление направлениями проектов

### Настройка
- **Кастомизация**: Настройки интерфейса
- **Оценки**: Система оценивания

## Функции безопасности
- Контроль доступа на основе разрешений
- Аутентификация по токенам
- Авторизация на основе ролей
- Защищенные конечные точки API

## Документация API
API документировано с использованием drf-spectacular, предоставляющего документацию OpenAPI/Swagger для всех конечных точек. Каждая конечная точка имеет теги и включает подробные описания, схемы запросов/ответов и требования к аутентификации.

## Тестирование
Автоматизированное тестирование реализовано через GitHub Actions, обеспечивая качество кода и функциональность:
- Модульные тесты
- Интеграционные тесты
- Тесты сборки Docker

Приложение следует принципам REST и предоставляет комплексное backend-решение для управления проектами и пользователями с широким функционалом API.


***
***
2 Вариант
***


# Описание Backend-приложения

Данное backend-приложение разработано на языке программирования Python версии 3.11 с использованием фреймворка Django REST Framework (DRF). В качестве базы данных используется SQLite3, что обеспечивает простоту в развертывании и обслуживании. Приложение контейнеризировано с помощью Docker, что гарантирует стабильную работу в любой среде развертывания.

Для обеспечения качества кода и автоматизации процессов разработки используется GitHub Actions, который автоматически запускает тесты при каждом push-запросе или pull request в ветки master и dev. Приложение развернуто на хостинг-платформе PythonAnywhere, что обеспечивает стабильный доступ к API.

API приложения предоставляет широкий спектр функциональности для управления проектами и пользователями. Основные возможности включают управление проектами (создание, редактирование, удаление), систему аутентификации и авторизации пользователей, управление задачами и их статусами. Реализована система ролей пользователей (организатор, руководитель, куратор), что позволяет гибко настраивать права доступа к различным функциям системы.

Безопасность приложения обеспечивается через систему токенов и разграничение прав доступа на основе ролей пользователей. Каждый endpoint API защищен соответствующими разрешениями, что гарантирует безопасность данных и корректное распределение доступа к функционалу.

Для удобства разработки и интеграции API полностью документировано с использованием drf-spectacular, что предоставляет автоматически генерируемую Swagger-документацию. Это позволяет легко понимать структуру API и тестировать различные endpoints.

Приложение поддерживает работу с проектами, включая управление участниками, задачами, комментариями и статусами выполнения. Реализована система оценивания и отслеживания прогресса, что позволяет эффективно контролировать ход выполнения проектов и оценивать работу участников.

Архитектура приложения следует принципам REST, что обеспечивает простоту интеграции с различными клиентскими приложениями и масштабируемость системы. Все компоненты системы хорошо структурированы и следуют современным практикам разработки.


