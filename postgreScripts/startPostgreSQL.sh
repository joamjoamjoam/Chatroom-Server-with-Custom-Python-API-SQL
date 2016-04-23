#! /bin/bash
rm -rf /tmp/$USER/data
mkdir /tmp/$USER/data
echo " export PGDATA=/tmp/$USER/data " >> ~/.profile
source ~/.profile
initdb
echo " export PGPORT=1024" >> ~/.profile
source ~/.profile
pg_ctl -o -i -o "-p $PGPORT" -D $PGDATA -l logfile start
pg_ctl status
echo " export DB_NAME=mydb" >> ~/.profile
source ~/.profile
pg_ctl status
echo PGPORT: $PGPORT
echo PGDATA: $PGDATA
echo DB_NAME: $DB_NAME
echo USER: $USER
pg_ctl status
