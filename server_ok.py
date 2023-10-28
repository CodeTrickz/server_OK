import argparse 
import sys
from server_check import run_checks, generate_html_report
from server_manager import add_server, remove_server, list_servers

def main():
    parser = argparse.ArgumentParser(description="Server Monitoring Tool")
    parser.add_argument("-e", action="store_true", help="Enter Edit Mode")
    parser.add_argument("-c", action="store_true", help="Enter Check Mode")
    args = parser.parse_args()
    if args.e:
        print("Server Edit mode")
        while True:
            action = input("Enter 'add', 'remove', or 'list' to manage servers , use 'exit' to exit menu: ")
            ServerEditMenu(action)
    if args.c:
        print("Server Check mode")
        run_checks()
        print("checks completed")
        generate_html_report()
        print("html with results is created")
    else:
         print("command used without any arguments, for more information try to run it with -h or --help flag")
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
        print("Invalid input. Please try again.") 
    

if __name__ == "__main__":
     main()