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
    if response < 0:
        return "Offline"
    else:
        return "Online"


def generate_html_report():
    servers = load_servers()

    with open("reports/server_status_report.html", "w") as html:
        html.write(
            "<html><head><title>Server Status Report</title></head><body>")
        html.write("<h1>Server Status Report</h1>")
        html.write("<table>")
        html.write(
            "<tr><th>Server Name</th><th>Server Address</th><th>Status</th></tr>")

        for server in servers:
            html.write("<tr>")
            html.write(f"<td>{server['name']}</td>")
            html.write(f"<td>{server['address']}</td>")
            html.write(f"<td>{server['status']}</td>")
            html.write("</tr>")

        html.write("</table>")
        html.write("</body></html>")


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
