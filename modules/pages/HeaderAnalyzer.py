#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.request
import urllib.error

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]

def analyze_headers(target_url):
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    print(f"\n[*] Connecting to: {target_url}")
    sys.stdout.flush()

    req = urllib.request.Request(
        target_url, 
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            headers = response.info()
            print("--------------------------------------------------")
            print("[+] SECURITY HEADERS ANALYSIS")
            print("--------------------------------------------------")

            for header in SECURITY_HEADERS:
                value = headers.get(header)
                if value:
                    print(f"[✓] {header}: {value}")
                else:
                    print(f"[✗] {header}: NOT CONFIGURABLE / MISSING")
            
            sys.stdout.flush()

    except urllib.error.URLError as e:
        print(f"[!] Connection error: {e.reason}")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

def start_module():
    print("[*] --- NOXBREACH HEADER ANALYZER ---")
    print("[?] Enter target domain or URL:")
    sys.stdout.flush()

    try:
        target = input().strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Process cancelled.")
        return

    if target:
        analyze_headers(target)
    else:
        print("[!] No target provided.")

if __name__ == "__main__":
    start_module()
