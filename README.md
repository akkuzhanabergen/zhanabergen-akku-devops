# DevOps laboratory work 1

Student: Akku Zhanabergen, IT2-2309, ID 37667. Course: DevOps.

For a MacBook Air M1, follow [the local setup guide](MAC_M1_SETUP.md). For the required screen recording, use [the under-10-minute video guide](VIDEO_GUIDE_UNDER_10_MIN.md).

This repository demonstrates Linux file operations, Git and GitHub, a Docker application, Docker Compose, and a five-stage Jenkins Pipeline. The application displays student data supplied by environment variables, with the student's data as defaults.

## Project structure

- `app/` - Python application.
- `scripts/Zhanabergen_Akku_system.sh` - student and Linux system information.
- `config/app.conf` - application configuration example.
- `logs/` - local application log; `*.log` is ignored by Git.
- `backup/` - local backups; ignored by Git.
- `tests/` - application checks used by Jenkins.

## Local checks

From the project root:

```sh
python3 -m compileall -q app
python3 -m unittest discover -s tests -v
docker build -t zhanabergen-akku-devops .
docker run -d --name zhanabergen-akku-container -p 8002:8000 \
  -e STUDENT_NAME=Akku -e STUDENT_SURNAME=Zhanabergen \
  -e STUDENT_GROUP=IT2-2309 -e STUDENT_ID=37667 \
  zhanabergen-akku-devops
docker logs zhanabergen-akku-container
docker ps
docker ps -a
docker stop zhanabergen-akku-container
docker start zhanabergen-akku-container
docker rm -f zhanabergen-akku-container
docker compose up -d --build
docker compose ps
docker compose down
```

The application is available at `http://localhost:8002/`; `http://localhost:8002/health` returns `OK`. Run the direct container and Compose demonstration one after the other because they use the same container name and port.

## Linux demonstration

Use a Linux shell and place the repository at `~/devops/zhanabergen_akku`. From its root:

```sh
./scripts/prepare_linux.sh
pwd
ls -la
cd scripts && cd ..
mkdir -p backup/demo
touch backup/demo/example.txt
cp backup/demo/example.txt backup/demo/copy.txt
mv backup/demo/copy.txt backup/demo/renamed.txt
rm backup/demo/renamed.txt
cat Zhanabergen_Akku_info.txt
head -n 3 Zhanabergen_Akku_info.txt
tail -n 2 Zhanabergen_Akku_info.txt
find . -name application.log
grep ERROR logs/application.log
grep WARNING logs/application.log
grep -c ERROR logs/application.log
tail -n 5 logs/application.log
chmod 600 private.txt
chmod 644 public.txt
ls -l private.txt public.txt
chmod +x scripts/Zhanabergen_Akku_system.sh
./scripts/Zhanabergen_Akku_system.sh
ps
ps aux
top
```

The preparation script creates `logs/application.log` with ten messages after cloning because Git ignores `*.log`. `private.txt` is readable and writable by its owner only; `public.txt` can also be read by the group and others.

## Git and Jenkins

The `development` branch contains a functional change that was merged into `main`. Use `git status`, `git log --oneline --graph`, `git branch`, `git check-ignore -v logs/application.log backup/example.txt .env`, and `git remote -v` to show the repository state. Jenkins reads the GitHub `main` branch and runs `Checkout`, `Build`, `Test`, `Docker Build`, and `Docker Run` from `Jenkinsfile`. The pipeline prints the student's name, group, and ID, then verifies the running container's health endpoint.
