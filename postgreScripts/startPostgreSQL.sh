#! /bin/bash
rm -rf /tmp/$USER/data
mkdir /tmp/$USER/data
echo " export PGDATA=/tmp/$USER/data " >> ~/.bashrc
source ~/.bashrc
initdb
echo " export PGPORT=1024" >> ~/.bashrc
source ~/.bashrc
pg_ctl -o -i -o "-p $PGPORT" -D $PGDATA -l logfile start
pg_ctl status
echo " export DB_NAME=mydb" >> ~/.bashrc
source ~/.bashrc
pg_ctl status
echo PGPORT: $PGPORT
echo PGDATA: $PGDATA
echo DB_NAME: $DB_NAME
echo USER: $USER
pg_ctl status
