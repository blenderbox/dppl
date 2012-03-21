#!/bin/bash

# Bash colors
BOLD="$(tput bold)"

# Config
BACKUPS_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../backups"
POSTGRES_USER="postgres"
DATABASE="dppl"
FILENAME="$(date +"%Y%m%d").pgsql"

# Make the backups dir if it doesn't exist since it's gitignored
echo "Making backup dir if non existant '${BACKUPS_DIR}'..."
mkdir -p $BACKUPS_DIR

function backup_url () {
  heroku pgbackups | tail -n 1 | cut -d'|' -f 1
}

heroku pgbackups:capture --expire

echo "Downloading backup from Heroku..."
curl $(heroku pgbackups:url $backup_url) > temporary_backup.dump

echo "Restoring backup with Postgres User '${POSTGRES_USER}' and Database '${DATABASE}'..."
sudo -u $POSTGRES_USER pg_restore --clean --no-acl --no-owner -h localhost -d $DATABASE temporary_backup.dump

echo "Moving backup to backup directory with name '${FILENAME}'..."
mv temporary_backup.dump "${BACKUPS_DIR}/${FILENAME}"

echo "${BOLD}[ Complete ]${RESET}"
