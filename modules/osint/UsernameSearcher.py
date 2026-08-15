#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import urllib.request
import urllib.error
import time

PLATFORMS = {
    
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Medium": "https://medium.com/@{}",
    "Vimeo": "https://vimeo.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Twitch": "https://www.twitch.tv/{}",

    
    "DockerHub": "https://hub.docker.com/u/{}",
    "GitLab": "https://gitlab.com/{}",
    "Replit": "https://replit.com/@{}",
    "Codeberg": "https://codeberg.org/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "PyPI": "https://pypi.org/user/{}/",
    "Keybase": "https://keybase.io/{}",
    "NPM": "https://www.npmjs.com/~{}",

    
    "ModDB": "https://www.moddb.com/members/{}",
    "Itch.io": "https://{}.itch.io",
    "Speedrun.com": "https://www.speedrun.com/users/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "NameMC": "https://namemc.com/profile/{}",

    
    "Disqus": "https://disqus.com/by/{}/",
    "Pastebin": "https://pastebin.com/u/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "ArtStation": "https://www.artstation.com/{}",
    "Behance": "https://www.behance.net/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "About.me": "https://about.me/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "Letterboxd": "https://letterboxd.com/{}/",
    "Anilist": "https://anilist.co/user/{}/"
}

def start_search():
    print("[*] --- NOXBREACH USERNAME SEARCHER ---")
    print("[?] Put the nick for search:")
    sys.stdout.flush()

    try:
        username = input().strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[!] Search Canceled.")
        return

    if not username:
        print("[!] Please put a nick.")
        return

    print(f"\n[*] Scanning '<strong>{username}</strong>' in {len(PLATFORMS)}")
    print("--------------------------------------------------")
    sys.stdout.flush()

    found_count = 0
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}

    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username)
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=3.5) as response:
                if response.status == 200:
                    print(f"[+] {platform}: Founded -> {url}")
                    found_count += 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"[-] {platform}: No Founded")
            else:
                print(f"[!] {platform}:  HTTP {e.code}")
        except urllib.error.URLError:
            print(f"[!] {platform}: Timeout / Error ")
        except Exception:
            print(f"[!] {platform}: Error ")
        
        sys.stdout.flush()
        time.sleep(0.15)

    print("--------------------------------------------------")
    print(f"[+] Resumen: {found_count}/{len(PLATFORMS)} cuentas encontradas para '{username}'.")
    sys.stdout.flush()

if __name__ == "__main__":
    start_search()
