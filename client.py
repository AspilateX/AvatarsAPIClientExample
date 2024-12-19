import requests
from models import CommandsContainer, ContainerStatus

class AvatarClient:
    avatar_endpoint = "avatar"
    command_endpoint = "command"
    def __init__(self, base_url):
        """
        Инициализация клиента.
        :param base_url: Базовый URL API
        """
        self.base_url = base_url.rstrip('/')

    def initialize_avatar(self, name: str, media_output_url: str):
        url = f"{self.base_url}/{self.avatar_endpoint}"
        body = {
            "name": name,
            "media_output_url": media_output_url
        }
        response = requests.post(url, json=body, verify=False)
        data = response.json()
        return data.get("uuid")

    def dispose_avatar(self, uuid: str):
        url = f"{self.base_url}/{self.avatar_endpoint}/{uuid}"
        requests.delete(url, verify=False)

    def next_container(self, uuid: str, container_id: str = ""):
        url = f"{self.base_url}/{self.avatar_endpoint}/{uuid}/{self.command_endpoint}/next"
        headers = {
            "container_id": container_id
        }
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code != 200:
            return None

        container = CommandsContainer.model_validate_json(response.json())
        return container
    
    def update_container_status(self, uuid: str, container_id: str, status: ContainerStatus):
        url = f"{self.base_url}/{self.avatar_endpoint}/{uuid}/{self.command_endpoint}/status"
        headers = {
            "container_id": container_id
        }
        body = {
            "status": status
        }
        requests.put(url, json=body, headers=headers, verify=False)