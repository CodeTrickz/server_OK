import argparse 
import sys
import logging

from server_check import run_checks, generate_html_report
from server_manager import add_server, remove_server, list_servers
from rich.console import Console
from rich.logging import RichHandler

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

def main():
    parser = argparse.ArgumentParser(description="Server Monitoring Tool")
    parser.add_argument("-e", action="store_true", help="Enter Edit Mode")
    parser.add_argument("-c", action="store_true", help="Enter Check Mode")
    args = parser.parse_args()
    if args.e:
        console.print("Server Edit mode", style="bold blue")
        while True:
            action = console.input("Enter 'add', 'remove', or 'list' to manage servers , use 'exit' to exit menu: ")
            ServerEditMenu(action)
    if args.c:
        console.print("Server Check mode",style="bold blue")
        run_checks()
        log.info("checks completed")
        generate_html_report()
        log.info("html with results is created")
    else:
         console.print("command used without any arguments, for more information try to run it with [bold red blink] -h [/] or [bold red blink] --help [/] flag", style="bold blue")
def ServerEditMenu(action):
    if action == 'add':
        add_server()
    elif action == 'remove':
        remove_server()
    elif action == 'list':
        list_servers()
    elif action == 'exit':
        sys.exit(0)
    else:
        log.error("[bold red blink]Invalid input. Please try again![/]", extra={"markup": True})
    

if __name__ == "__main__":
     main()