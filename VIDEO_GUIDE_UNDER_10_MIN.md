# Видеозащита лабораторной: один дубль до 10 минут

Для **Zhanabergen Akku, IT2-2309, Student ID 37667**. Исходное задание рекомендует 10–20 минут; этот сценарий по вашему запросу рассчитан на **9 минут 40 секунд**. Покажи собственный экран и говори своим голосом. Начни запись только после того, как на Mac выполнен `MAC_M1_SETUP.md` и Jenkins хотя бы один раз завершился `Finished: SUCCESS`.

## Подготовка до начала записи — не входит в 9:40

1. Открой Docker Desktop и дождись **Engine running**. Открой Терминал Mac в `~/devops/zhanabergen_akku`; проверь, что Linux- и Jenkins-контейнеры запущены:

   ```sh
   cd "$HOME/devops/zhanabergen_akku"
   docker ps --filter name=zhanabergen-akku-linux
   docker ps --filter name=zhanabergen-akku-jenkins
   ```

2. Открой три вкладки браузера: [репозиторий GitHub](https://github.com/akkuzhanabergen/zhanabergen-akku-devops), [Jenkins](http://127.0.0.1:8081/) и [приложение](http://127.0.0.1:8002/). В Jenkins заранее открой Job `Zhanabergen_Akku_DevOps`. Если потребуется войти в Jenkins, сделай это **до записи**, чтобы не показывать пароль.
3. Держи открытыми файлы `Zhanabergen_Akku_info.txt`, `.gitignore`, `Dockerfile`, `docker-compose.yml`, `Jenkinsfile`. Увеличь шрифт Терминала и браузера так, чтобы строки читались на записи.
4. Убедись, что свободен порт `8002` после теста Compose; последняя Jenkins-сборка может держать учебный контейнер — это нормально, его удаление показано в Docker-сегменте.
5. Держи блоки команд этого файла под рукой и вставляй их группами. Задание разрешает подготовить проект заранее; в видео достаточно показать результаты и объяснить их, а не печатать каждую команду посимвольно.

### OBS на Mac

1. В OBS открой **OBS Studio → Review App Permissions** и разреши **Screen Recording** и **Microphone**. Добавь источник захвата экрана и вход микрофона; увидь движение шкалы микрофона, когда говоришь. [Разрешения OBS на macOS](https://obsproject.com/kb/macos-permissions-guide).
2. В **Settings → Output → Recording** выбери папку сохранения (например, `Movies`) и формат **MKV**. Он рекомендован OBS для надёжной записи; после остановки можно выполнить **File → Remux Recordings** и получить MP4 без монтажа. [Руководство OBS по записи](https://obsproject.com/kb/standard-recording-output-guide).
3. Сделай короткую пробную запись: видно ли экран, слышно ли голос. Останови её, открой файл и проверь. После этого начни **новую** непрерывную запись для сдачи. Веб-камера не требуется заданием.

## 0:00–0:35 — представление и проект

**На экране:** открой `Zhanabergen_Akku_info.txt` и покажи пять строк. Затем покажи корень проекта в Терминале Mac.

```sh
cd "$HOME/devops/zhanabergen_akku"
cat Zhanabergen_Akku_info.txt
ls
```

**Скажи:** «Меня зовут Акку Жанаберген, группа IT2-2309, Student ID 37667. Это моя лабораторная работа DevOps. Здесь я показываю Linux, Git, GitHub, Docker и Jenkins на MacBook Air M1».

## 0:35–2:35 — Linux: файлы, лог, права, скрипт, процессы

**На экране:** войди в отдельный Linux-контейнер; команды после входа выполняются внутри Linux.

```sh
docker exec -it zhanabergen-akku-linux sh
cd /root/devops/zhanabergen_akku
pwd
ls -ld app scripts config logs backup
cat Zhanabergen_Akku_info.txt
```

**Скажи:** «Это Linux-папка `~/devops/zhanabergen_akku`. `pwd` показывает текущий путь, `ls` — файлы. Папки `app`, `scripts`, `config`, `logs`, `backup` требуются заданием».

Быстро покажи создание, копирование, перемещение и удаление **только временных файлов внутри `backup`**:

```sh
mkdir -p backup/demo
touch backup/demo/one.txt
cp backup/demo/one.txt backup/demo/two.txt
mv backup/demo/two.txt backup/demo/renamed.txt
ls backup/demo
rm backup/demo/renamed.txt
head -n 3 Zhanabergen_Akku_info.txt
tail -n 2 Zhanabergen_Akku_info.txt
```

**Скажи:** «`mkdir` создаёт папку, `touch` — пустой файл, `cp` копирует, `mv` переименовывает, `rm` удаляет. `cat`, `head`, `tail` читают файл целиком, с начала и с конца. `cd` меняет текущую папку».

Покажи поиск и лог:

```sh
find . -name application.log
grep ERROR logs/application.log
grep WARNING logs/application.log
grep -c ERROR logs/application.log
tail -n 5 logs/application.log
```

**Ожидается:** путь `./logs/application.log`, строки `ERROR` и `WARNING`, число `2`, последние пять записей. **Скажи:** «`find` ищет файл, `grep` выбирает строки, `grep -c` считает ошибки. Лог содержит не менее десяти строк».

Покажи права, скрипт и процесс:

```sh
chmod 600 private.txt
chmod 644 public.txt
ls -l private.txt public.txt
chmod +x scripts/Zhanabergen_Akku_system.sh
ls -l scripts/Zhanabergen_Akku_system.sh
./scripts/Zhanabergen_Akku_system.sh
ps aux
top -b -n 1 | head -n 12
exit
```

**Скажи:** «У `private.txt` права `600`: только владелец читает и пишет. У `public.txt` права `644`: другие могут читать. `r`, `w`, `x` — чтение, запись, выполнение; права задаются владельцу, группе и остальным. `chmod +x` разрешает запуск скрипта. Скрипт показывает мои данные, имя пользователя, хост, дату, ОС, диск, память и проверяет файл информации. `ps` показывает снимок процессов, `top` — обновляемые CPU и память; PID — номер процесса». Укажи пальцем на одну строку `top` (например, `sleep`) и назови показанные там PID, владельца, процент CPU и процент памяти/виртуальной памяти; значения считай с экрана, не выдумывай.

## 2:35–3:50 — Git, ветка, GitHub

**На экране:** ты снова в Терминале Mac. Выполни:

```sh
cd "$HOME/devops/zhanabergen_akku"
git status
git log --oneline --graph --all -n 14
git branch -a
cat .gitignore
git check-ignore -v logs/application.log backup/example.txt .env
git remote -v
```

Покажи в браузере [GitHub-репозиторий](https://github.com/akkuzhanabergen/zhanabergen-akku-devops), файлы `Dockerfile`, `Jenkinsfile`, README и список коммитов. **Скажи:** «Git сохраняет изменения в осмысленных коммитах. Ветка `development` использовалась для изменения и была объединена с `main`; ветки позволяют работать отдельно. `.gitignore` исключает `*.log`, `backup/` и `.env`. GitHub хранит публичный проект; Jenkins получает код оттуда. `git remote -v` показывает адрес репозитория, `git push` отправляет коммиты на GitHub».

## 3:50–5:40 — Docker и Docker Compose

**На экране:** открой `Dockerfile`, затем `docker-compose.yml`. Покажи строки `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`, переменные окружения и порт `8002:8000`.

**Скажи:** «Dockerfile создаёт образ с приложением. Образ — шаблон, контейнер — запущенный экземпляр образа. Переменные окружения передают имя, группу и ID при запуске; секреты нельзя записывать прямо в образ. Compose описывает запуск приложения в одном YAML-файле».

В Терминале Mac покажи уже собранный образ и текущий контейнер:

```sh
docker images zhanabergen-akku-devops
docker ps -a --filter name=zhanabergen-akku-container
docker logs zhanabergen-akku-container
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' zhanabergen-akku-container | grep '^STUDENT_'
docker stop zhanabergen-akku-container
docker start zhanabergen-akku-container
docker rm -f zhanabergen-akku-container
docker compose up -d --build
docker compose ps
curl -i http://127.0.0.1:8002/health
docker compose down
```

**Ожидается:** образ, студентские переменные и лог, затем после Compose — HTTP `200`. **Скажи:** «`docker logs` выводит журнал, `stop` останавливает, `start` запускает, `rm` удаляет контейнер. `docker exec` запускает команду внутри контейнера. Compose поднимает и останавливает приложение; сейчас я освобождаю порт, чтобы Jenkins сам запустил контейнер».

## 5:40–8:30 — Jenkins: Job, пять стадий, успешная сборка

**На экране:** открой локальный Jenkins `http://127.0.0.1:8081/`, покажи Dashboard и Job с точным именем **`Zhanabergen_Akku_DevOps`**. В конфигурации Job покажи ссылку GitHub, ветку `*/main` и путь `Jenkinsfile`; пароль не показывай. В GitHub или редакторе открой `Jenkinsfile` и покажи пять стадий.

**Скажи:** «Jenkins берёт `Jenkinsfile` из моего GitHub-репозитория. `Checkout` получает код; `Build` проверяет компиляцию; `Test` выполняет четыре теста; `Docker Build` создаёт образ; `Docker Run` запускает контейнер и проверяет `/health`».

Нажми **Build Now**. Пока сборка идёт, коротко покажи команды проверки на Mac:

```sh
git rev-parse --short HEAD
docker ps --filter name=zhanabergen-akku-container
```

Вернись к Jenkins, открой новую сборку → **Pipeline Steps** (все пять стадий) → **Console Output**. Найди в выводе Git commit, `Ran 4 tests`, `Student: Akku Zhanabergen`, `Group: IT2-2309`, `Student ID: 37667`, `Finished: SUCCESS`. Покажи `docker images zhanabergen-akku-devops`, `docker ps --filter name=zhanabergen-akku-container` и страницу <http://127.0.0.1:8002/>.

**Скажи:** «Jenkins собрал именно коммит из GitHub, вывел мои переменные, выполнил тесты, создал Docker-образ и запустил контейнер. Зелёная сборка и `Finished: SUCCESS` подтверждают результат».

Если первая сборка длится долго, **не вырезай ожидание**: перед зачётной записью сначала сделай одну успешную сборку для загрузки зависимостей, затем в видео запусти следующую. Запись должна оставаться непрерывной.

## 8:30–9:40 — связь технологий и вывод

**На экране:** вернись к Jenkins Console Output и GitHub; последним кадром оставь `Finished: SUCCESS` и имя Job.

**Скажи:** «Linux даёт оболочку, файлы и права. Git хранит историю изменений, GitHub — удалённый репозиторий. Jenkins скачивает конкретный коммит с GitHub и последовательно выполняет сборку и тесты. Затем Jenkins собирает Docker-образ и запускает из него контейнер. Если стадия не проходит, дальнейшие стадии останавливаются, а причина остаётся в Console Output. Я проверила приложение, логи, Docker Compose и успешный Pipeline. Спасибо».

Нажми **Stop Recording** до 10:00. Если записала MKV, в OBS выбери **File → Remux Recordings**, выбери файл и получи MP4. Открой конечный файл целиком или хотя бы начало, середину и конец: голос должен быть слышен, текст читаем, `Finished: SUCCESS` виден, длительность меньше 10 минут. Отправь GitHub-ссылку, PDF и видео по требованиям преподавателя. Если для видео предусмотрена отдельная учебная платформа, загружай туда; сохрани исходную непрерывную запись.
