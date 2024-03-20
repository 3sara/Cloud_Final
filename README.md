# Cloud_Final

This is the repository of Carpenè Sara for the final project of Cloud Computing course

To test this project the steps to be performed are:

1. Setup of the containers with
 ```bash
docker-compose up -d
```
using the file [`docker-compose.yml`](docker-compose.yml).
Once performed this step it is possible to connect to http://localhost:8080 and perform the operations described in the report.

2. Creation of users with the bash script in [`UserCreation.sh`](UserCreation.sh)
  
3. Creation of the test files, modifying the parameters, with
 ```bash 
 dd if=/dev/zero of=deletable.txt bs=1M count=1
 ```
4. Run the  [`filelocust.py`](filelocust.py) with
 ```bash locust -f filelocust.py ```
Once performed this step it's possible to accede to the http://localhost:8089 to manage number of users, ramp up and to start the test.
