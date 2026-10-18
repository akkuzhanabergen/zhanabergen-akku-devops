# План демонстрации DevOps

Zhanabergen Akku, IT2-2309, Student ID 37667. План на 9–10 минут.

Перед записью: выполнить [настройку Mac](MAC_M1_SETUP.md) и проверить успешную сборку Jenkins.
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
5. Проверь команды перед записью.

### OBS на Mac

1. В OBS открой **OBS Studio → Review App Permissions** и разреши **Screen Recording** и **Microphone**. Добавь источник захвата экрана и вход микрофона; увидь движение шкалы микрофона, когда говоришь. [Разрешения OBS на macOS](https://obsproject.com/kb/macos-permissions-guide).
2. В **Settings → Output → Recording** выбери папку сохранения (например, `Movies`) и формат **MKV**. Он рекомендован OBS для надёжной записи; после остановки можно выполнить **File → Remux Recordings** и получить MP4 без монтажа. [Руководство OBS по записи](https://obsproject.com/kb/standard-recording-output-guide).
3. Сделай короткую пробную запись: видно ли экран, слышно ли голос. Останови её, открой файл и проверь. После этого начни **новую** непрерывную запись для сдачи. Веб-камера не требуется заданием.

## 0:00–0:35 — представление и проект

Открой `Zhanabergen_Akku_info.txt` и покажи пять строк. Затем покажи корень проекта в Терминале Mac.

```sh
cd "$HOME/devops/zhanabergen_akku"
cat Zhanabergen_Akku_info.txt
ls
```

## 0:35–2:35 — Linux: файлы, лог, права, скрипт, процессы

Войди в отдельный Linux-контейнер; команды после входа выполняются внутри Linux.

```sh
docker exec -it zhanabergen-akku-linux sh
cd /root/devops/zhanabergen_akku
pwd
ls -ld app scripts config logs backup
cat Zhanabergen_Akku_info.txt
```

Файловые операции в `backup/demo`:

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

Покажи поиск и лог:

```sh
find . -name application.log
grep ERROR logs/application.log
grep WARNING logs/application.log
grep -c ERROR logs/application.log
tail -n 5 logs/application.log
```

Результат: путь `./logs/application.log`, строки `ERROR` и `WARNING`, число `2`, последние пять записей.

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

## 2:35–3:50 — Git, ветка, GitHub

Ты снова в Терминале Mac. Выполни:

```sh
cd "$HOME/devops/zhanabergen_akku"
git status
git log --oneline --graph --all -n 14
git branch -a
cat .gitignore
git check-ignore -v logs/application.log backup/example.txt .env
git remote -v
```

Покажи в браузере [GitHub-репозиторий](https://github.com/akkuzhanabergen/zhanabergen-akku-devops), файлы `Dockerfile`, `Jenkinsfile`, README и список коммитов.

## 3:50–5:40 — Docker и Docker Compose

Открой `Dockerfile`, затем `docker-compose.yml`. Покажи строки `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`, переменные окружения и порт `8002:8000`.

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

Результат: образ, студентские переменные и лог, затем после Compose — HTTP `200`.

## 5:40–8:30 — Jenkins: Job, пять стадий, успешная сборка

Открой локальный Jenkins `http://127.0.0.1:8081/`, покажи Dashboard и Job с точным именем **`Zhanabergen_Akku_DevOps`**. В конфигурации Job покажи ссылку GitHub, ветку `*/main` и путь `Jenkinsfile`; пароль не показывай. В GitHub или редакторе открой `Jenkinsfile` и покажи пять стадий.

Нажми **Build Now**. Пока сборка идёт, коротко покажи команды проверки на Mac:

```sh
git rev-parse --short HEAD
docker ps --filter name=zhanabergen-akku-container
```

Вернись к Jenkins, открой новую сборку → **Pipeline Steps** (все пять стадий) → **Console Output**. Найди в выводе Git commit, `Ran 4 tests`, `Student: Akku Zhanabergen`, `Group: IT2-2309`, `Student ID: 37667`, `Finished: SUCCESS`. Покажи `docker images zhanabergen-akku-devops`, `docker ps --filter name=zhanabergen-akku-container` и страницу <http://127.0.0.1:8002/>.

## 8:30–9:40 — результаты

Вернись к Jenkins Console Output и GitHub; последним кадром оставь `Finished: SUCCESS` и имя Job.

После записи проверь звук, читаемость команд и длительность. Для преобразования MKV в MP4: **File → Remux Recordings** в OBS.
