## Структура проекта

- Бизнес логика сервиса располагается в src/app/core/service.py
- Схемы для валидации данных в src/app/schemas/schemas.py
- Эндпоинты в src/app/ebdpoints/endpoints.py
- Тесты располагаются в src/tests/unit

## Настройка локального окружения

Для внесения изменений в репозиторий необходимо настроить работу внутри devcontainer-а.

### MacOS / Windows

- Устновить [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Установить [Visual Studio Code](https://code.visualstudio.com/download)
- [Настроить Visual Studio Code и Docker для использования Devcontainers](https://code.visualstudio.com/docs/devcontainers/containers#_getting-started)
- [Настроить Git и SSH для работы в Devcontainer](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials)
- [Установить шрифт Meslo Nerd Font для CLI в терминале](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#fonts)
- По необходимости установить и настроить kubectl, внутри контейнера будут использованы настройки с хоста
- Склонировать этот репозиторий на рабочую станцию
- Открыть директорию с репозиторием через Visual Studio Code
- Установить [рекомендуемые плагины](.vscode/extensions.json) Visual Studio Code
- Ввести `Ctrl+Shift+P` или `Cmd+Shift+P` и выбрать `Dev Containers: Rebuild and Reopen in Container`

### Миграции

Для наката миграций на базу данных необходимо добавить в файл .env переменные:
```
DB_HOST =
DB_PORT =
DB_NAME =
DB_USER =
DB_PASS =

POSTGRES_DB =
POSTGRES_USER =
POSTGRES_PASSWORD =
```
Затем запустить в терминале команду:
```sh
$ alembic upgrade head
```
ВАЖНО!
Перед накатом миграций в сервисах Transaction и FaceVerification необходимо накатить миграции из сервиса Auth.

При запуске пректа через docker-compose.yaml миграции накатятся автоматически, нужно только создать файл с переменными описанными выше.
