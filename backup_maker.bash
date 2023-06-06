POSTGRES_USER=mspp
POSTGRES_DB=mspp
CURRENT_DATE=$(date +%Y-%m-%d)
BACKUPS_PATH=/MSPP/dumps
KEEP_DAY=15

BACKUP_FOLDER=$BACKUPS_PATH
if [ ! -d "$BACKUP_FOLDER" ]; then
    mkdir -p "$BACKUP_FOLDER"
fi


echo 'Creating PostgreSQL backups...'
cd "$BACKUP_FOLDER"
if [ -f 'dump_'"$POSTGRES_DB"'_'"$CURRENT_DATE"'.sql' ]; then
   rm 'dump_'"$POSTGRES_DB"'_'"$CURRENT_DATE"'.sql'
fi

docker exec -t postgres_stage pg_dump -U $POSTGRES_USER $POSTGRES_DB > 'dump_'"$POSTGRES_DB"'_'"$CURRENT_DA>


find $BACKUP_FOLDER -mtime +$KEEP_DAY -delete
