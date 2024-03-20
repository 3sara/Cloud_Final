#!/bin/bash

URL="http://localhost:8080/ocs/v1.php/cloud/users"
MYNAME="user1"
MYPASSWORD="User1"


for i in {2..30}; do
    USER="user$i"
    USERPASSWORD="password_of_user_$i"
    docker exec -i -u 33 5e20aac8f1f7 bash -c "export OC_PASS=$USERPASSWORD && /var/www/html/occ user:add $USER --password-from-env" 
done
