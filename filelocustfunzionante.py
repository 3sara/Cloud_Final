from locust import HttpUser, task
from requests.auth import HTTPBasicAuth
import requests
import random

with open("output.txt", "a") as f:
    f.write(f"_________________________________________________\n")

class NextcloudUser(HttpUser):
    auth = None
    users_list = list(range(2,30))

    def on_start(self):
        random.shuffle(self.users_list)
        i = self.users_list.pop()
        self.user = 'user' + '{:d}'.format(i)
        self.password = 'password_of_user_'+'{:d}'.format(i)
        self.auth = HTTPBasicAuth(self.user, self.password)
        self.verify_authentication()


    def verify_authentication(self):
        response = self.client.head("/remote.php/dav", auth=self.auth)
        if response.status_code != 200:
            with open("output.txt", "a") as f:
                f.write(f"Authentication failed for user {self.user}: {response.text}.\n")
            raise Exception(f"Authentication failed for user {self.user}")


    @task
    def propfind(self):
        try:
            response = self.client.request("PROPFIND", "/remote.php/dav", auth=self.auth)
            response.raise_for_status()
        except Exception as e:
            with open("output.txt", "a") as f:
                f.write(f"Error during PROPFIND request: {e} for user {self.user}.\n")


    @task
    def upload_small(self):
        filename = "into-the-wild.png"
        with open(filename, 'rb') as f:
            response = self.client.put("/remote.php/dav/files/" + self.user + "/" + filename,
                                       auth=self.auth, data=f, name="/remote.php/dav/files/[user]/into-the-wild.png")

        if response.status_code != 201 and response.status_code != 204 :
            with open("output.txt", "a") as f:
                f.write(f"Error during PUT request: {response.status_code} for user {self.user}.\n")
            return

        for i in range(0, 5):
            self.client.get("/remote.php/dav/files/" + self.user + "/" + filename,
                            auth=self.auth, name="/remote.php/dav/files/[user]/into-the-wild.png")

        self.client.delete("/remote.php/dav/files/" + self.user + "/" + filename,
                           auth=self.auth, name="/remote.php/dav/files/[user]/into-the-wild.png")


"""



    @task
    def upload_medium(self):
        filename = "Lecture01.pdf"  # Change the filename
        with open('/app/files/' + filename, 'rb') as f:
            response = self.client.put("/remote.php/dav/files/" + self.user + "/" + filename,
                                    auth=self.auth, data=f, name="/remote.php/dav/files/[user]/Lecture01.pdf")

        if response.status_code != 201 and response.status_code != 204:
            with open("/mnt/locust/output.txt", "a") as f:
                f.write(f"Error during PUT request: {response.status_code} for user {self.user}.\n")
            return

        for i in range(0, 5):
            self.client.get("/remote.php/dav/files/" + self.user + "/" + filename,
                            auth=self.auth, name="/remote.php/dav/files/[user]/Lecture01.pdf")

        self.client.delete("/remote.php/dav/files/" + self.user + "/" + filename,
                        auth=self.auth, name="/remote.php/dav/files/[user]/Lecture01.pdf")


    @task
    def upload_large(self):
        filename = "train_mini.csv"
        with open('/app/files/' + filename, 'rb') as f:
            response = self.client.put("/remote.php/dav/files/" + self.user + "/" + filename,
                                       auth=self.auth, data=f, name="/remote.php/dav/files/[user]/train_mini.csv")

        if response.status_code not in (201, 204):
            with open("/mnt/locust/output.txt", "a") as f:
                f.write(f"Error during PUT request: {response.status_code} for user {self.user}.\n")
            return

        
        self.client.get("/remote.php/dav/files/" + self.user + "/" + filename,
                        auth=self.auth, name="/remote.php/dav/files/[user]/train_mini.csv")

        self.client.delete("/remote.php/dav/files/" + self.user + "/" + filename,
                        auth=self.auth, name="/remote.php/dav/files/[user]/train_mini.csv")
"""
