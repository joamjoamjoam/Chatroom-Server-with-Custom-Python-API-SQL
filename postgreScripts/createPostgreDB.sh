# /bin/bash
source ~/.bashrc
createdb -p $PGPORT $DB_NAME
pg_ctl status

psql mydb < database.sql
