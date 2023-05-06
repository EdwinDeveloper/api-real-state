
#BACKUP OF THE DATABASE LOCATED IN OUR DOCKER VOLUME
docker exec -t <container_id> pg_dump --dbname=<database_name> --file=/root/backup/dump_.sql -U <db_user_access>

#COPY OUR FILES NAMED "dump_.sql" into /root/backup ROUTE
docker cp <container_id>:/dump_.sql /root/backup