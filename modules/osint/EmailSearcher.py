import os
import sys
import asyncio
import aiohttp
from typing import Dict, List, Tuple

COLOR_RED = "\033[1;31m"
COLOR_DARK_RED = "\033[31m"
COLOR_TEXT_RED = "\033[38;2;220;50;50m"
COLOR_GRAY = "\033[1;30m"
COLOR_RESET = "\033[0m"

SERVICES = [
    ("Twitter / X", "https://api.twitter.com/i/users/email_available.json?email={email}", "get", "taken", True),
    ("GitHub", "https://github.com/signup_check/username?email={email}", "get", "already taken", True),
    ("Instagram", "https://www.instagram.com/api/v1/web/accounts/web_create_page/attempt_registered_email/", "post", "email_is_taken", True),
    ("Spotify", "https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}", "get", "1", True),
    ("Pinterest", "https://www.pinterest.com/v3/users/check_email/?email={email}", "get", "exists", True),
    ("Imgur", "https://imgur.com/signin/check_email", "post", "has_account", True),
    ("Adobe", "https://auth.services.adobe.com/signin/v2/users/accounts", "post", "type", True),
    ("WordPress", "https://wordpress.com/wp-json/rest/v1.1/users/email/{email}", "get", "exists", True),
    ("Patreon", "https://www.patreon.com/api/credentials/check_email", "post", "is_registered", True),
    ("Discourse", "https://meta.discourse.org/u/check_username.json?email={email}", "get", "taken", True),
    ("Duolingo", "https://www.duolingo.com/2017-06-30/users?email={email}", "get", "users", True),
    ("Tumblr", "https://www.tumblr.com/svc/account/register", "post", "taken", True),
    ("Medium", "https://medium.com/m/api/users/email", "post", "value", True),
    ("Quora", "https://www.quora.com/api/logged_out_signup_flow", "post", "success", True),
    ("Vimeo", "https://vimeo.com/api/v2/user/check_email", "get", "is_taken", True),
    ("SoundCloud", "https://api-v2.soundcloud.com/users/check-email/{email}", "get", "status", True),
    ("Trello", "https://trello.com/1/authentication/saml/checkProvider", "post", "account", True),
    ("GitLab", "https://gitlab.com/users/check_email", "get", "taken", True),
    ("Bitbucket", "https://bitbucket.org/site/master/api/1.0/users/{email}", "get", "username", True),
    ("DockerHub", "https://hub.docker.com/v2/users/login", "post", "message", True),
    ("Slack", "https://slack.com/api/users.checkEmail", "post", "ok", True),
    ("Dropbox", "https://www.dropbox.com/ajax_check_email", "post", "exists", True),
    ("Evernote", "https://www.evernote.com/Registration.action", "post", "error", True),
    ("Figma", "https://www.figma.com/api/email_check", "post", "exists", True),
    ("Canva", "https://www.canva.com/api/signup/check-email", "post", "taken", True),
    ("Notion", "https://www.notion.so/api/v3/checkEmailValid", "post", "hasPassword", True),
    ("Chess.com", "https://www.chess.com/callback/email/check?email={email}", "get", "used", True),
    ("Riot Games", "https://authenticate.riotgames.com/api/v1/login", "post", "error", True),
    ("Twitch", "https://passport.twitch.tv/register/check", "post", "email_taken", True),
    ("Steam", "https://store.steampowered.com/join/checkemailavailable", "post", "is_available", False),
    ("Etsy", "https://www.etsy.com/api/v3/ajax/bespoke/member/check-email", "post", "registered", True),
    ("eBay", "https://www.ebay.com/usr/api/checkemail", "post", "status", True),
    ("AliExpress", "https://passport.aliexpress.com/check_email.htm", "get", "isSuccess", True),
    ("PayPal", "https://www.paypal.com/auth/flow/login", "post", "auth", True),
    ("Stripe", "https://dashboard.stripe.com/register/check_email", "post", "exists", True),
    ("Mailchimp", "https://login.mailchimp.com/signup/check-email", "post", "taken", True),
    ("HubSpot", "https://app.hubspot.com/api/signup/v1/check-email", "post", "exists", True),
    ("Zoho", "https://accounts.zoho.com/register/checkemail", "post", "status", True),
    ("ProtonMail", "https://mail.proton.me/api/users/check", "get", "Code", True),
    ("Mega", "https://g.api.mega.co.nz/cs", "post", "error", True),
    ("Archive.org", "https://archive.org/account/signup", "post", "status", True),
    ("Scribd", "https://www.scribd.com/check_email", "post", "in_use", True),
    ("Wattpad", "https://www.wattpad.com/api/v3/users/check_email", "get", "exists", True),
    ("Goodreads", "https://www.goodreads.com/user/check_email", "get", "used", True),
    ("TripAdvisor", "https://www.tripadvisor.com/UserCheck", "post", "exists", True),
    ("Airbnb", "https://www.airbnb.com/api/v2/phone_or_email_validations", "post", "is_valid", True),
    ("Booking.com", "https://account.booking.com/api/check-email", "post", "has_account", True),
    ("Lastpass", "https://lastpass.com/check_email.php", "post", "exists", True),
    ("1Password", "https://my.1password.com/api/v1/checkemail", "post", "status", True),
    ("Bitwarden", "https://api.bitwarden.com/accounts/prelogin", "post", "Kdf", True),
    ("Keybase", "https://keybase.io/_/api/1.0/user/lookup.json?email={email}", "get", "them", True)
]

def print_header():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{COLOR_RED}============================================================{COLOR_RESET}")
    print(f"{COLOR_TEXT_RED}          NOXBREACH - OSINT EMAIL                 {COLOR_RESET}")
    print(f"{COLOR_RED}============================================================{COLOR_RESET}\n")

async def check_service(session: aiohttp.ClientSession, name: str, url: str, method: str, match_key: str, match_condition: bool, email: str) -> Tuple[str, str]:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}
    target_url = url.format(email=email)
    try:
        if method == "get":
            async with session.get(target_url, headers=headers, timeout=5) as resp:
                text = await resp.text()
        else:
            async with session.post(target_url, headers=headers, data={"email": email}, timeout=5) as resp:
                text = await resp.text()
        
        found = (match_key in text) == match_condition
        if found:
            return (name, f"{COLOR_TEXT_RED}[+] REGISTERED{COLOR_RESET}")
        else:
            return (name, f"{COLOR_GRAY}[-] NOT FOUND{COLOR_RESET}")
    except Exception:
        return (name, f"{COLOR_DARK_RED}[!] ERROR / BLOCKED{COLOR_RESET}")

async def run_scan(email: str):
    print(f"{COLOR_TEXT_RED}[*] Target Email:{COLOR_RESET} {email}")
    print(f"{COLOR_TEXT_RED}[*] Loaded Services:{COLOR_RESET} {len(SERVICES)}")
    print(f"{COLOR_RED}------------------------------------------------------------{COLOR_RESET}")
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            check_service(session, name, url, method, key, cond, email)
            for name, url, method, key, cond in SERVICES
        ]
        
        results = await asyncio.gather(*tasks)
        
        found_count = 0
        for name, status in results:
            print(f"  {COLOR_RED}> {name:<20}{COLOR_RESET} : {status}")
            if "REGISTERED" in status:
                found_count += 1

    print(f"{COLOR_RED}------------------------------------------------------------{COLOR_RESET}")
    print(f"{COLOR_TEXT_RED}[+] Scan finished. Matches found: {found_count}/{len(SERVICES)}{COLOR_RESET}\n")

def main():
    print_header()
    while True:
        try:
            email = input(f"{COLOR_TEXT_RED}Enter Email Target > {COLOR_RESET}").strip()
            if not email:
                print(f"{COLOR_GRAY}[!] Empty input. Try again.{COLOR_RESET}")
                continue
            if "@" not in email or "." not in email:
                print(f"{COLOR_DARK_RED}[!] Invalid email format.{COLOR_RESET}")
                continue
            
            print()
            asyncio.run(run_scan(email))
            
            again = input(f"{COLOR_TEXT_RED}{COLOR_RESET}").strip().lower()
            if again != 'y':
                print(f"\n{COLOR_GRAY}[*] Returning to NoxBreach ...{COLOR_RESET}")
                break
            print_header()
        except KeyboardInterrupt:
            print(f"\n\n{COLOR_GRAY}[*] Session terminated.{COLOR_RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main()
