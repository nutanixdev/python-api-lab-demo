#!/usr/bin/env python3.8

import sys
import requests
from requests.auth import HTTPBasicAuth


class ApiClient:
    def __init__(
        self,
        method,
        cluster_ip,
        request,
        body,
        entity,
        username,
        password,
        version="v3",
        root_path="api/nutanix",
    ):
        self.method = method
        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.base_url = f"https://{self.cluster_ip}:9440/{root_path}/{version}"
        self.request_url = f"{self.base_url}/{request}"
        self.body = body
        self.entity = entity

    def get_info(self):

        headers = {"Content-Type": "application/json; charset=utf-8"}
        try:
            if self.method == "post":
                r = requests.post(
                    self.request_url,
                    data=self.body,
                    verify=False,
                    headers=headers,
                    auth=HTTPBasicAuth(self.username, self.password),
                    timeout=60,
                )
            else:
                r = requests.get(
                    self.request_url,
                    verify=False,
                    headers=headers,
                    auth=HTTPBasicAuth(self.username, self.password),
                    timeout=60,
                )
        except requests.ConnectTimeout:
            print(
                f"Connection timed out while connecting to {self.cluster_ip}. Please check your connection, then try again."
            )
            sys.exit()
        except requests.ConnectionError:
            print(
                f"An error occurred while connecting to {self.cluster_ip}. Please check your connection, then try again."
            )
            sys.exit()
        except requests.HTTPError:
            print(
                f"An HTTP error occurred while connecting to {self.cluster_ip}. Please check your connection, then try again."
            )
            sys.exit()

        if r.status_code >= 500:
            print(f"An HTTP server error has occurred ({r.status_code}, {r.text})")
        else:
            if r.status_code == 401:
                print(
                    f"An authentication error occurred while connecting to {self.cluster_ip}. Please check your credentials, then try again."
                )
                sys.exit()

        return r.json()
