#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import urllib.request
import urllib.error
import socket
import time
from concurrent.futures import ThreadPoolExecutor

SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/Unk1nown/ProxyLists/refs/heads/main/free-proxy-list.txt",
    "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocolipport&format=text&ssl=yes&anonymity=elite"
]

REGEX_PATTERN = r"\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b"

def fetch_proxies_from_source(url):
    proxies = set()
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8', errors='ignore')
            matches = re.findall(REGEX_PATTERN, content)
            for match in matches:
                proxies.add(match)
    except Exception:
        pass
    return proxies

def verify_proxy(proxy_str):
    ip, port = proxy_str.split(":")
    start_time = time.perf_counter()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2.0)
        result = sock.connect_ex((ip, int(port)))
        sock.close()
        
        if result == 0:
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            return proxy_str, latency_ms
    except Exception:
        pass
    return None

def save_proxies(active_proxies):
    if not active_proxies:
        print("[!] No hay proxies funcionales para guardar.")
        return

    print("\n[?] ¿Deseas descargar/guardar los proxies funcionales? (s/n):")
    sys.stdout.flush()
    try:
        save_input = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        return

    if save_input.startswith('s') or save_input.startswith('y'):
        filename = "active_proxies.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for proxy, ms in active_proxies:
                f.write(f"{proxy}\n")
        print(f"[+] ¡Guardado con éxito! {len(active_proxies)} proxies guardados en '{filename}'")

def start_scraper():
    print("[*] --- NOXBREACH PROXY ENGINE ---")
    print("[?] ¿Want to ON the ProxyScraper? (s/n):")
    sys.stdout.flush()

    try:
        check_input = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Proceso cancelado.")
        return

    should_check = check_input.startswith('s') or check_input.startswith('y')

    print(f"\n[*] Starting...")
    sys.stdout.flush()

    all_proxies = set()
    for source in SOURCES:
        found = fetch_proxies_from_source(source)
        all_proxies.update(found)
        print(f"[+] Founded {len(found)} in {source[:45]}...")
        sys.stdout.flush()

    print("--------------------------------------------------")
    print(f"[+] Total Proxies Found: {len(all_proxies)}")
    print("--------------------------------------------------")
    sys.stdout.flush()

    if should_check and all_proxies:
        print("[*] Verifying proxies via Sockets...")
        sys.stdout.flush()
        
        active_proxies = []
        proxy_list = list(all_proxies)[:10000]

        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(verify_proxy, proxy_list)
            for res in results:
                if res:
                    proxy, ms = res
                    active_proxies.append((proxy, ms))
                    print(f"[+] PROXY ACTIVE: {proxy} [{ms}ms]")
                    sys.stdout.flush()

        print("--------------------------------------------------")
        print(f"[+] Working Proxies: {len(active_proxies)}")
        print("--------------------------------------------------")
        sys.stdout.flush()

        save_proxies(active_proxies)

if __name__ == "__main__":
    start_scraper()
