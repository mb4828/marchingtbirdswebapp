#!/bin/bash
# Backs up the OpenShift PostgreSQL database for this application
# by Skye Book <skye.book@gmail.com>

NOW="$(date +"%Y-%m-%d")"
FILENAME="$OPENSHIFT_DATA_DIR/$OPENSHIFT_APP_NAME.$NOW.backup.sql.gz"
find $OPENSHIFT_DATA_DIR -name $OPENSHIFT_APP_NAME.*backup* -type f -mtime +30 -exec rm '{}' \;
pg_dump $OPENSHIFT_APP_NAME | gzip > $FILENAME