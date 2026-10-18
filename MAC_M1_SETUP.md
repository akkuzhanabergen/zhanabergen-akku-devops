# Лабораторная DevOps на MacBook Air 13″ с Apple M1

Локальный запуск Linux-контейнера, приложения и Jenkins. Команды выполняются в терминале macOS; команды внутри Linux отмечены отдельно. План записи: [VIDEO_GUIDE_UNDER_10_MIN.md](VIDEO_GUIDE_UNDER_10_MIN.md).

## 1. Проверь Mac и установи три программы

Открой Терминал (`⌘ + Пробел` → «Терминал») и проверь чип:

```sh
uname -m
sw_vers -productVersion
```

Ожидаемое значение первой команды — `arm64`. Для Docker Desktop и OBS нужен поддерживаемый ими выпуск macOS; актуальные требования показаны на их официальных страницах ниже.

### Git

Проверь `git --version`. Если macOS предлагает установить инструменты разработчика, согласись. Иначе выполни:

```sh
xcode-select --install
```

Дождись окончания установки и вновь выполни `git --version`. Полный Xcode и Homebrew для этой лабораторной не нужны. [Инструкция Apple](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools/).

### Docker Desktop

1. Открой [официальную страницу Docker Desktop для Mac](https://docs.docker.com/desktop/setup/install/mac-install/) и скачай вариант **Mac with Apple silicon**, не Intel.
2. Открой `.dmg`, перетащи Docker в «Программы» и запусти Docker Desktop. Дождись состояния **Engine running**.
3. В Docker Desktop открой **Settings → Advanced** и включи **Allow the default Docker socket to be used**. Подтверди системным паролем Mac, если он запрошен. Это нужно, чтобы Jenkins-контейнер мог выполнять `docker build` и `docker run` через `/var/run/docker.sock`. [Объяснение Docker](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/).
4. Вернись в Терминал и проверь:

```sh
docker version
docker compose version
test -S /var/run/docker.sock && echo 'Docker socket OK'
```

Должны отобразиться версии клиента/сервера и строка `Docker socket OK`. Если `docker` не найден, перезапусти Терминал после установки Docker Desktop. Если сокет не найден, включи настройку из шага 3 и перезапусти Docker Desktop.

### OBS Studio

Скачай [OBS Studio для **arm64 / Apple Silicon**](https://obsproject.com/download) и перетащи его в «Программы». В OBS открой **OBS Studio → Review App Permissions** и разреши **Screen Recording** и **Microphone**; без этого не запишутся экран или голос. [Инструкция OBS](https://obsproject.com/kb/macos-permissions-guide). Настройка записи приведена во втором файле.

## 2. Скачай проект и проверь данные

```sh
mkdir -p "$HOME/devops"
cd "$HOME/devops"
git clone https://github.com/akkuzhanabergen/zhanabergen-akku-devops.git zhanabergen_akku
cd "$HOME/devops/zhanabergen_akku"
git status
git branch -a
cat Zhanabergen_Akku_info.txt
```

`git status` и `git branch -a` показывают состояние рабочей копии и доступные ветки. Файл информации должен содержать `Akku`, `Zhanabergen`, `IT2-2309`, `37667` и `DevOps`. Для клонирования публичного репозитория вход в GitHub не нужен.

Если будешь делать новые коммиты **на этом Mac**, задай свою личность только в этом проекте:

```sh
git config --local user.name 'Akku Zhanabergen'
git config --local user.email 'akkuwka145@gmail.com'
```

## 3. Подготовь отдельный Linux-контейнер

Linux-команды лабораторной выполняются в Alpine-контейнере.

```sh
docker run -d --name zhanabergen-akku-linux alpine:3.21 sleep infinity
docker exec zhanabergen-akku-linux sh -c 'apk add --no-cache git && mkdir -p /root/devops && git clone https://github.com/akkuzhanabergen/zhanabergen-akku-devops.git /root/devops/zhanabergen_akku && cd /root/devops/zhanabergen_akku && sh scripts/prepare_linux.sh'
docker exec -it zhanabergen-akku-linux sh
```

Теперь приглашение Терминала находится **внутри Linux**. Выполни:

```sh
cd /root/devops/zhanabergen_akku
pwd
ls -la
ls -ld app scripts config logs backup
cat Zhanabergen_Akku_info.txt
find . -name application.log
grep ERROR logs/application.log
grep WARNING logs/application.log
grep -c ERROR logs/application.log
tail -n 5 logs/application.log
ls -l private.txt public.txt
./scripts/Zhanabergen_Akku_system.sh
ps aux
top -b -n 1 | head -n 12
```

Ожидается: пять папок, лог из 10 строк, счётчик `ERROR` равен `2`, права `private.txt` — `-rw-------`, `public.txt` — `-rw-r--r--`; системный скрипт показывает данные студента и компьютера Linux. Для демонстрации команд `mkdir`, `touch`, `cp`, `mv`, `rm` используй временную папку `backup/demo` по разделу README. Выйди из Linux командой `exit`.

Если позже выключишь Linux-контейнер, запускай `docker start zhanabergen-akku-linux`, затем `docker exec -it zhanabergen-akku-linux sh`. Повторно клонировать проект не требуется.

## 4. Проверь приложение, Docker и Compose

Вернись в Терминал Mac и в корень проекта:

```sh
cd "$HOME/devops/zhanabergen_akku"
docker build -t zhanabergen-akku-devops .
docker images zhanabergen-akku-devops
docker run -d --name zhanabergen-akku-container -p 8002:8000 \
  -e STUDENT_NAME=Akku -e STUDENT_SURNAME=Zhanabergen \
  -e STUDENT_GROUP=IT2-2309 -e STUDENT_ID=37667 \
  zhanabergen-akku-devops
docker ps --filter name=zhanabergen-akku-container
docker logs zhanabergen-akku-container
curl -i http://127.0.0.1:8002/health
```

Страница <http://127.0.0.1:8002/> должна показать данные Akku. `/health` должен вернуть HTTP `200` и `OK`. Контейнер использует переменные окружения, поэтому значения не зашиваются только в Docker-образ.

Перед проверкой Compose удали **только этот учебный контейнер**, чтобы имя и порт `8002` освободились:

```sh
docker rm -f zhanabergen-akku-container
docker compose up -d --build
docker compose ps
curl -i http://127.0.0.1:8002/health
docker compose down
```

`docker compose down` остановит приложение Compose. Jenkins затем запустит контейнер приложения. Не запускай Compose и Jenkins-сборку одновременно — они используют одинаковые имя контейнера и порт.

## 5. Установи Jenkins локально в Docker

Jenkins на Mac не требует отдельной установки Java или Python: `jenkins/Dockerfile` собирает Jenkins с Python, Git, Docker CLI и Pipeline/Git-плагинами. Официальный образ Jenkins публикуется для `linux/arm64`, подходящего M1. Первая сборка образа скачает зависимости и может занять несколько минут.

```sh
cd "$HOME/devops/zhanabergen_akku"
docker build -f jenkins/Dockerfile -t zhanabergen-akku-jenkins jenkins
docker run -d --name zhanabergen-akku-jenkins \
  -p 127.0.0.1:8081:8080 \
  -v zhanabergen_jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  zhanabergen-akku-jenkins
docker ps --filter name=zhanabergen-akku-jenkins
```

Подожди, пока откроется <http://127.0.0.1:8081/>. Для **первой** настройки Jenkins получи одноразовый пароль локально:

```sh
docker exec zhanabergen-akku-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Вставь его на странице Unlock Jenkins. Выбери **Install suggested plugins**, затем создай собственного администратора и сохрани пароль у себя. Пароль не должен попадать в запись экрана. Jenkins доступен только с этого Mac через `127.0.0.1:8081`; GitHub-репозиторий доступен отдельно через интернет.

Создай Job в веб-интерфейсе:

1. **New Item** → имя **`Zhanabergen_Akku_DevOps`** → тип **Pipeline** → **OK**.
2. В разделе **Pipeline** выбери **Definition: Pipeline script from SCM**.
3. **SCM: Git**; **Repository URL:** `https://github.com/akkuzhanabergen/zhanabergen-akku-devops.git`; **Credentials:** `none` (репозиторий публичный).
4. **Branch Specifier:** `*/main`; **Script Path:** `Jenkinsfile` → **Save**.
5. Нажми **Build Now**, открой появившуюся сборку → **Pipeline Steps** и **Console Output**.

Должны пройти `Checkout`, `Build`, `Test`, `Docker Build`, `Docker Run`. В конце Console Output должно быть `Finished: SUCCESS`, а также `Student: Akku Zhanabergen`, `Group: IT2-2309`, `Student ID: 37667`. Проверь контейнер и приложение:

```sh
docker ps --filter name=zhanabergen-akku-container
docker images zhanabergen-akku-devops
curl -i http://127.0.0.1:8002/health
```

Номер сборки и SHA коммита в Jenkins относятся к текущему запуску и могут отличаться от приведённых в PDF-отчёте.

## 6. Что открыть перед записью видео

- Терминал Mac в `~/devops/zhanabergen_akku`.
- Терминал Linux через `docker exec -it zhanabergen-akku-linux sh`.
- [GitHub-репозиторий](https://github.com/akkuzhanabergen/zhanabergen-akku-devops).
- Локальный [Jenkins](http://127.0.0.1:8081/) и [приложение](http://127.0.0.1:8002/).
- Файлы `.gitignore`, `Dockerfile`, `docker-compose.yml`, `Jenkinsfile` в редакторе или GitHub.

## 7. Если что-то не запустилось

| Признак | Что проверить |
| --- | --- |
| `Cannot connect to the Docker daemon` | Docker Desktop должен показывать **Engine running**; повтори `docker version`. |
| Нет `/var/run/docker.sock` | Docker Desktop → Settings → Advanced → **Allow the default Docker socket to be used**. |
| `port is already allocated` для `8002` | Выполни `docker ps`, останови/удали **свой** `zhanabergen-akku-container` или Compose через `docker compose down`. Если порт занят другой программой, не останавливай её без проверки. |
| Jenkins не открывается на `8081` | `docker ps --filter name=zhanabergen-akku-jenkins` и `docker logs zhanabergen-akku-jenkins`; дождись полной загрузки. |
| Jenkins: `docker: command not found` или ошибка сокета | Убедись, что собран именно `jenkins/Dockerfile`, смонтирован `/var/run/docker.sock`; проверь `docker exec zhanabergen-akku-jenkins docker version`. |
| Jenkins: нет `Jenkinsfile` | Проверь URL GitHub, ветку `*/main` и `Script Path: Jenkinsfile`. |
| Лог `application.log` отсутствует | В Linux-контейнере повтори `cd /root/devops/zhanabergen_akku && sh scripts/prepare_linux.sh`: `*.log` намеренно исключён из Git. |

Для следующего запуска после выключения Mac сначала открой Docker Desktop, затем:

```sh
docker start zhanabergen-akku-linux zhanabergen-akku-jenkins
```

Jenkins Job сохранён в отдельном Docker volume; повторная установка и повторное создание Job не нужны. Учебный контейнер приложения при необходимости запускается кнопкой **Build Now** в Jenkins.

Официальные основы: [Docker Desktop на Mac](https://docs.docker.com/desktop/setup/install/mac-install/), [Jenkins в Docker](https://www.jenkins.io/doc/book/installing/docker/), [Pipeline из Git](https://www.jenkins.io/doc/book/pipeline/getting-started/), [OBS на Mac](https://obsproject.com/kb/mac-installation).
