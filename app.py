import time
from client import AvatarClient
from models import ContainerStatus, Command

# Чтобы HTTPS не выдаавал варнинги: InsecureRequestWarning: Unverified HTTPS request is being made to host. Adding certificate verification is strongly advised.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client = AvatarClient("https://localhost:7241/api/v1")
uuid = None

def main():
    global uuid, client
    uuid = client.initialize_avatar("Python test client", "")
    print(f"Avatar created (ID: {uuid})")

    active_container_id = ""
    next_command_index = 0
    print("Awaiting commands")
    try:
        while True:
            time.sleep(1)
            container = client.next_container(uuid)
            
            # Если очередь контейнеров пуста
            if not container:
                continue

            # Если пришел новый контейнер, обновляем статус на PROCESSING т.к. работаем с ним, начиная с первой команды
            if container.id != active_container_id:
                client.update_container_status(uuid, container.id, ContainerStatus.PROCESSING)
                next_command_index = 0
            
            # Если в полученном контейнере столько же или меньше команд, чем мы уже выполнили, то пропускаем
            if (len(container.commands) <= next_command_index):
                continue

            active_container_id = container.id

            # Начинаем от текущей команды пока не выполним все новые команды
            for i in range(next_command_index, len(container.commands)):
                handle_command(container.commands[i])
    except Exception as ex:
        print(ex)
        client.dispose_avatar(uuid)
        uuid = None
        print(f"Avatar disposed (ID: {uuid})")

def handle_command(command: Command):
    time.sleep(1)
    print(f"I'm saying: {command.message}")

if __name__ == "__main__":
    main()

def __exit__(self, exc_type, exc_value, traceback):
    global uuid, client
    if uuid and client:
        client.dispose_avatar(uuid)