# LOG IN INTO OUR PSQL
psql -U <username> -h <hostname> -p <port>
psql -U REALSTATEPRODADMIN -h localhost -p 5432

# CREATING A SQL BACKUP FROM OUTSIDE A CONTAINER
docker exec -t <container_id> pg_dump --dbname=<database_name> --file=/root/backup/dump_.sql -U <username>

docker exec -t 6cd905909c48 pg_dump --dbname=REALSTATEPRODDB --file=/dump_realstate.sql -U REALSTATEPRODADMIN

# COPY OUR DATABASE INTO OUR DOCKER CONTAINER
docker cp 6cd905909c48:/dump_realstate.sql /root/

docker cp /Users/edwingiovanni/Desktop/dump_realstate.sql 157f080ee393:/

docker cp 6cd905909c48:/dump_realstate.sql /root/backup

# LOGIN INTO OUR DROPLET USING AN SPECIFIC SSH NAME
ssh root@143.198.63.104 -i droplet_realstate

# LOGIN INTO OUR DROPLET WITH NOTHING THANT USERNAME AND THE IP
ssh root@143.198.63.104 

# COPY A FILE FROM OUR DROPLET INTO OUR LOCAL MACHINE USING AN SPECIFIC SSH NAME
scp -i droplet_realstate root@143.198.63.104:/root/dump_realstate.sql /Users/edwingiovanni/Desktop

# IMPORTING OUT BACKUP DATABASE INTO OUR POSTGRES SYSTEM
psql -U REALSTATEPRODADMIN -d REALSTATEPRODDB3 -f dump_realstate.sql

psql -U <USER_DB_NAME> -d <DB_NAME>

createdb -U <USER_DB_NAME> -h localhost -p 5432 <DB_NAME>

psql -U <username> -d <database_name>

psql -U <USER_DB_NAME> -d <database_name>

CREATE ROLE devuser;
