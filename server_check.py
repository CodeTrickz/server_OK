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
    response = ping(addr) % 2
    if response != False:
        return "Online"
    else:
        return "Offline"


def generate_html_report():
    servers = load_servers()

    with open("reports/server_status_report.html", "r") as html:
        template = html.read()

    table_start = template.find("<table>")
    table_end = template.find("</table>")
    table_data = template[table_start:table_end]

    updated_table = "<table><tr><th>Server Name</th><th>Server Address</th><th>Status</th></tr>"
    for server in servers:
        updated_table += f"<tr><td>{server['name']}</td><td>{server['address']}</td><td>{server['status']}</td></tr>"

    report = template.replace(table_data, updated_table)

    with open("reports/server_status_report.html", "w") as report_file:
        report_file.write(report)


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
