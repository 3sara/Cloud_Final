from locust import HttpUser, task
from requests.auth import HTTPBasicAuth
import requests
import random

with open("output_modified.txt", "a") as f:
    f.write(f"_________________________________________________\n")

class CustomUser(HttpUser):
    credentials = None
    user_ids = list(range(2,30))

    def on_start(self):
        random.shuffle(self.user_ids)
        user_id = self.user_ids.pop()
        self.username = 'user' + '{:d}'.format(user_id)
        self.user_password = 'password_of_user_'+'{:d}'.format(user_id)
        self.credentials = HTTPBasicAuth(self.username, self.user_password)
        self.check_authentication()

    def check_authentication(self):
        response = self.client.head("/remote.php/dav", auth=self.credentials)
        if response.status_code != 200:
            with open("output_modified.txt", "a") as f:
                f.write(f"Authentication failed for user {self.username}: {response.text}.\n")
            raise Exception(f"Authentication failed for user {self.username}")

    @task
    def find_properties(self):
        try:
            response = self.client.request("PROPFIND", "/remote.php/dav", auth=self.credentials)
            response.raise_for_status()
        except Exception as e:
            with open("output_modified.txt", "a") as f:
                f.write(f"Error during PROPFIND request: {e} for user {self.username}.\n")


    @task
    def upload_file(self):
        file_name = "deletable.txt"
        with open(file_name, 'rb') as f:
            response = self.client.put("/remote.php/dav/files/" + self.username + "/" + file_name,
                    auth=self.credentials, data=f, name="/remote.php/dav/files/[user]/deletable.txt")

        if response.status_code not in [201, 204]:
            with open("output_modified.txt", "a") as f:
                f.write(f"Error during PUT request: {response.status_code} for user {self.username}.\n")
            return

        for i in range(0, 5):
            self.client.get("/remote.php/dav/files/" + self.username + "/" + file_name,
                            auth=self.credentials, name="/remote.php/dav/files/[user]/deletable.txt")
        try:
            response_delete = self.client.delete("/remote.php/dav/files/" + self.username + "/" + file_name,
                           auth=self.credentials, name="/remote.php/dav/files/[user]/deletable.txt")
            if response_delete.status_code not in [201, 204]:
                with open("output_modified.txt", "a") as f:
                    f.write(f"Error during DELETE request: {response_delete.status_code} for user {self.username}.\n")
                return
        except Exception as e:
            with open("output_modified.txt", "a") as f:
                f.write(f"Exception during DELETE request: {e} for user {self.username}.\n")


    @task
    def get_task(self):
        response = self.client.get("/remote.php/dav/files/" + self.username + "/", auth=self.credentials)
        if response.status_code != 200:
            with open("output_modified.txt", "a") as f:
                f.write(f"Error accessing user files for user {self.username}.\n")

