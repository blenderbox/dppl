#!/bin/bash

# Bash colors
BOLD="$(tput bold)"

# Config
BACKUPS_DIR="$( cd -P "$( dirname "${BASH_SOURCE[0]}" )/../.tmp/backups" && pwd )"
POSTGRES_USER="postgres"
DATABASE="dppl"
FILENAME="${DATABASE}.$(date +"%Y%m%d").pgsql"

# Make the backups dir if it doesn't exist since it's gitignored
echo "Making backup dir if non existant '${BACKUPS_DIR}'..."
mkdir -p $BACKUPS_DIR

function backup_url () {
  heroku pgbackups | tail -n 1 | cut -d'|' -f 1
}

heroku pgbackups:capture --expire

echo "Downloading backup from Heroku..."
curl $(heroku pgbackups:url $backup_url) > "${BACKUPS_DIR}/${FILENAME}"

echo "Restoring backup with Postgres User '${POSTGRES_USER}' and Database '${DATABASE}'..."
pg_restore --clean --no-acl --no-owner -h localhost -d $DATABASE "${BACKUPS_DIR}/${FILENAME}"
