# LOG IN INTO OUR PSQL
psql -U <username> -h <hostname> -p <port>
psql -U REALSTATEPRODADMIN -h localhost -p 5432

# CREATING A SQL BACKUP FROM OUTSIDE A CONTAINER
docker exec -t <container_id> pg_dump --dbname=<database_name> --file=/root/backup/dump_.sql -U 

# COPY OUR DATABASE INTO OUR DOCKER CONTAINER
docker cp realstate.sql 1855168fead7:/

# LOGIN INTO OUR DROPLET USING AN SPECIFIC SSH NAME
ssh root@143.198.63.104 -i droplet_realstate

# LOGIN INTO OUR DROPLET WITH NOTHING THANT USERNAME AND THE IP
ssh root@143.198.63.104 

# COPY A FILE FROM OUR DROPLET INTO OUR LOCAL MACHINE USING AN SPECIFIC SSH NAME
scp -i droplet_realstate root@:143.198.63.104:/root/realstate.sql /Users/edwingiovanni/Desktop

# IMPORTING OUT BACKUP DATABASE INTO OUR POSTGRES SYSTEM
psql -U REALSTATEPRODADMIN -d REALSTATEPRODDB3 -f realstate.sql

psql -U REALSTATEPRODADMIN -d REALSTATEPRODDB

createdb -U <USER_DB_NAME> <DB_NAME>
