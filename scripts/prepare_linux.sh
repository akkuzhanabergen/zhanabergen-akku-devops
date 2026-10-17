#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
mkdir -p "$project_dir/logs" "$project_dir/backup"
cat > "$project_dir/logs/application.log" <<'LOG'
INFO Application started
INFO User logged in
WARNING Configuration file missing
INFO Database connected
ERROR Database connection failed
INFO Application restarted
WARNING Memory usage is high
INFO Request received
ERROR Request failed
INFO Application stopped
LOG
chmod 600 "$project_dir/private.txt"
chmod 644 "$project_dir/public.txt"
chmod +x "$project_dir/scripts/Zhanabergen_Akku_system.sh"
printf '%s\n' 'Created ten log messages and applied file permissions.'
