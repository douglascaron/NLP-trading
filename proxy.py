import queue
import requests
from colorama import init, Fore
init(autoreset=True)

q = queue.Queue()

with open("proxy.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)

def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            print(f"{Fore.CYAN}[ROTATING PROXY]{Fore.RESET} Searching for proxy...")
            res = requests.get("https://google.com", timeout=3)
            print(f"{Fore.CYAN}[ROTATING PROXY]{Fore.RESET} Proxy found!")
            print(f"{Fore.GREEN}[PROXY USED]{Fore.RESET} {proxy}")
        except requests.RequestException:
            continue
        if res.status_code == 200:
            return proxy
