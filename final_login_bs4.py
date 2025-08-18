import requests
from bs4 import BeautifulSoup
import random




def get_working_proxies():
    url = "https://free-proxy-list.net/en/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"class": "table table-striped table-bordered"})

    working_proxies = []

    for row in table.tbody.find_all("tr"):
        cols = row.find_all("td")
        ip = cols[0].text.strip()
        port = cols[1].text.strip()
        country = cols[3].text.strip()
        https = cols[6].text.strip()

        proxy = f"{ip}:{port}"

        if https != "yes":
            continue  # Only HTTPS proxies

        proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        try:
            resp = requests.get("https://httpbin.org/ip", proxies=proxy_dict, timeout=5)
            if resp.status_code == 200:
                #print(f"[Working] {proxy} | Country: {country}")
                return {"proxy": proxy, "country": country}  # return one at a time
            break
        except:
            pass

# Create session (handles cookies automatically)


session = requests.Session()

login_url = "https://mit.s.dk/studiebolig/login/"

# 1. GET login page → extract CSRF token
resp = session.get(login_url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(resp.text, "html.parser")


csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
#print("CSRF token:", csrf_token)


# 2. Prepare payload
payload = {
    "csrfmiddlewaretoken": csrf_token,
    "username": "mdabdullah",      # your username
    "password": "@#ABdullah298"    # your password
}

user_agents = [
    # Chrome (Windows, Mac, Linux)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    # Firefox (Windows, Mac, Linux)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",

    # Edge (Windows, Mac)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",

    # Safari (Mac, iPhone, iPad)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.1 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/537.36",

    # Mobile Chrome & Firefox
    "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 6) Gecko/115.0 Firefox/115.0",
]
random_user_agent = random.choice(user_agents)
headers = {
    "User-Agent": random_user_agent,
    "Referer": login_url   # Django requires Referer to match
}
login_resp = session.post(login_url, data=payload, headers=headers)
soup_login = BeautifulSoup(login_resp.text, "html.parser")


if "hello" in soup_login.text.lower():
    print("Login Done")
else:
    print("Login Unsuccessful")


logout_url = "https://mit.s.dk/studiebolig/logout/"
logout_resp = session.get(logout_url)#, headers={"Referer": home_url})

# --- 5. Print the page content after logout ---
# soup_after_logout = BeautifulSoup(logout_resp.text, "html.parser")
# print(soup_after_logout.text)