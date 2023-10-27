import os
import json
from ping3 import ping

SERVERS_FILE = "data/servers.json"

def run_checks():
    print("server will be checked...")
    servers = load_servers()

    for server in servers:
        addr = server["address"]
        status = ping_server(addr)
        server["status"] = status

    save_servers(servers)

def ping_server(addr):
    print(f"{addr}: {ping(addr)}")
    response = ping(addr)
    if response == False:
        return "Online"
    else:
        return "Offline"

def update_status(server, status):
    print("status server")
def generate_html_report():
    print("maak html pagina")


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