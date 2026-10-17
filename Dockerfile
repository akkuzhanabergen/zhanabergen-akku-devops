FROM python:3.12-alpine

WORKDIR /project
COPY app/ ./app/
COPY scripts/ ./scripts/
COPY Zhanabergen_Akku_info.txt ./
RUN python -m compileall -q app && chmod +x scripts/Zhanabergen_Akku_system.sh
EXPOSE 8000
CMD ["python", "-u", "app/main.py"]
