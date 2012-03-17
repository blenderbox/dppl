#!/bin/bash

POSTGRES_USER="postgres"
DATABASE="dppl"

heroku pgbackups:capture --expire

function backup_url () {
  heroku pgbackups | tail -n 1 | cut -d'|' -f 1
}

echo 'Downloading backup...'
curl $(heroku pgbackups:url $backup_url) > temporary_backup.dump
echo 'Restoring backup...'
sudo -u $POSTGRES_USER pg_restore --clean --no-acl --no-owner -h localhost -d $DATABASE temporary_backup.dump
# rm -f temporary_backup.dump
