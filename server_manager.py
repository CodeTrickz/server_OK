import json

SERVERS_FILE = "data/servers.json"

def add_server():
    while True:
        server_name = input("Enter the server name: ")
        server_address = input("Enter the server IP address or hostname: ")

        server_data = {
            "name": server_name,
            "address": server_address,
            "status": "Unknown"
        }

        servers = load_servers()
        servers.append(server_data)
        save_servers(servers)
        

        another = input("Do you want to add another server? (yes/no): ")
        if another.lower() != 'yes':
            break
        

def remove_server():
    servers = load_servers()
    if not servers:
        print("No servers to remove.")
        return

    print("Existing servers:")
    for i in range(len(servers)):
        server = servers[i]
        print(f"{i + 1}. {server['name']} - {server['address']}")

    while True:
        try:
            server_index = int(input("Enter the index of the server to remove: ")) - 1
            if 0 <= server_index < len(servers):
                removed_server = servers.pop(server_index)
                print(f"Removed server: {removed_server['name']} - {removed_server['address']}")
                save_servers(servers)
                break
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

def list_servers():
    servers = load_servers()
    if not servers:
        print("No servers registered.")
    else:
        print("Registered servers:")
        for i in range(len(servers)):
            server = servers[i]
            print(f"{i + 1}. Name: {server['name']} - IP/host: {server['address']} - Status: {server['status']}")

def load_servers():
    try:
        with open(SERVERS_FILE, 'r') as file:
            servers = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        servers = []
    return servers

def save_servers(servers):
    with open(SERVERS_FILE, 'w') as file:
        json.dump(servers, file)
