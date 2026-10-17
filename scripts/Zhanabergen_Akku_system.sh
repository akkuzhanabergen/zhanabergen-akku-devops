#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

printf '%s\n' '==============================' 'Student Information' '=============================='
printf 'Name: %s\nSurname: %s\nGroup: %s\nStudent ID: %s\n' \
  'Akku' 'Zhanabergen' 'IT2-2309' '37667'
printf '%s\n' '==============================' 'System Information' '=============================='
printf 'Username: %s\n' "$(whoami)"
printf 'Hostname: %s\n' "$(hostname)"
printf 'Current Date: %s\n' "$(date)"
printf 'Operating System: %s\n' "$(uname -srm)"
printf 'Disk Usage: %s\n' "$(df -h "$project_dir" | tail -n 1)"
printf 'Memory Usage: %s\n' "$(free -h | head -n 2 | tail -n 1)"

if [ -f "$project_dir/Zhanabergen_Akku_info.txt" ]; then
  printf '%s\n' 'Student information file exists.'
else
  printf '%s\n' 'Student information file does not exist.'
fi
