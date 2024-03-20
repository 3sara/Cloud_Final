# Cloud_Final

To test this project the steps to be performed are:

1. Setup of the containers with
 ```bash
docker-compose up -d
```
using the file [`docker-compose.yml`](docker-compose.yml).

2. Creation of the users with the bash script in [`UserCreation.sh`](UserCreation.sh)
  
3. Creation of the test files, modifying the parameters, with
 ```bash 
 dd if=/dev/zero of=deletable.txt bs=1M count=1
 ```
4. Run the  [`filelocust.py`](filelocust.py) with
 ```bash locust -f filelocust.py ```
