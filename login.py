import requests
from selenium import webdriver
from seleniumbase import Driver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
import time
import re
import os
import pickle
import random
from pathlib import Path
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

###############
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

###############
directory = Path("downloaded_files")
driver_path = ChromeDriverManager().install()
if not directory.is_dir():
    driver_creation = Driver(uc=True, guest_mode=True, disable_cookies=True, headless=True)
else:
    pass



# Function to set up Selenium WebDriver with stealth mode
chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--headless")  # Run in headless mode (no UI)


headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'baggage': 'sentry-environment=production,sentry-release=leadgenie-app%4083027294aac3edfbb4c15f87b8ee7c3317bc18ee,sentry-public_key=86bb17dd8c2449719dd6b498f3431191,sentry-trace_id=2608c4d00bab4ec68645b78632d49b0a,sentry-sample_rate=0.001,sentry-transaction=%2F,sentry-sampled=false',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dwn-profiling': 'CgpBc2lhL0RoYWthEOgCGOgCIgtHb29nbGUgSW5jLigIONYKQIAGSgVXaW4zMlIGeDg2XzY0WgVlbi1VU2IFZW4tVVNiAmVuagZjaHJvbWVwAXoQhKigcKyL2volQp5f9KpxAoIBEPvJVXffeVPllzeTfVoXoxWIARiYAQGgAQCoAQCwAQC4AQjAAQDIAQDQAQDYAQDgAQH4AQGAAgGIAgCQAg2aAhDMAiCTB7HuPiFmeEvCHX5opQIAUBVDrQIAUBVDtQIAUBVDvQIABBBDxQIACPNCzQIAgBVB1QIA3BND2gIQwF4gK3R/VHBQM6mRQv2ObOACAOgCAPACKPgCAIADAZIDEC5+GGjmxg2eREWzDKy9cNaYAwWiAxDBQrN5ygGO9Za6Ttivx59LqgNVQU5HTEUgKEludGVsLCBJbnRlbChSKSBIRCBHcmFwaGljcyA0NjAwICgweDAwMDAwNDE2KSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKbIDE0dvb2dsZSBJbmMuIChJbnRlbCnAAwHIA4fOufXRMtAD/6/D9dEy2APo3+7v0TLiA3xNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUUvTWd3czFJeW80WG9TMFJESjgwS3l2MkFvQlNhV0VGQ3pGU3B4SGtpMGx2ZkY1ZW9KeFhpdnNqMmxPWG0rZms0TnQ3aDIxSk1obTFUZk5nQ05vQmhvZz096gNgTUVVQ0lRRGtKUEpUOU1tTFdSd0hBdk9uWWhNaWVCaFNyVnVpeEE2bGRUNDh6REtmM2dJZ1FYSGJvWmZMbFkrNDdmckF5SkRkL0oxTUFKWEh4dW12VWxvakFjR3N1V0U9igQgM2JkMGJkMGZmZWY5NDkzM2I3NDA5ZGI5Nzc3ZWZiNzKSBE0KBWVtYWlsGgR0ZXh0IgVlbWFpbCorbzc0Y2RiNzZlLTRlMTItNDRkNi1iZjNiLWEzOGQ1YzdhZTU0YS1pbnB1dFCL4sH10TJYAvABAZIE0wEKCHBhc3N3b3JkGghwYXNzd29yZCIIcGFzc3dvcmQqEGN1cnJlbnQtcGFzc3dvcmQ4AVDz3ML10TJYAngBwAEB2AEB+gEgCAEVAAAQwh0AABDCJQAAEMIt////fzX///9/PQAAAAD6ASAIAhUAAMBAHQAAcEIlAAAEQi0AAFhCNQAAcEI9AADYQfoBIAgDFQAA8MEdAADwwSUAAPDBLf///381////fz0AAAAA+gEgCAQVAADAQR0AAMBBJQAAwEEt////fzX///9/PQAAAACAArM2mgSaAggOEP/DBxgVIAVCIAgBFX0uTkEd3m64QyWyqj1DLUSrlkI1KhIeQz2/8cJCQiAIAhW56EVBHUnttkMl83w4Qy1TcJlCNZtHEkM9DsrFQkIgCAMVAABUQh0AQA9EJWIYb0MtAACIQjUAgA5DPYNsLENCIAgEFQ7xLz4duypuQCU9Qac/LSa8DT81lGNePz3TUI8/QiAIBRX+fDo5HfRcPD4lvJWsPC2tvmY7NTrMgzs9JkgkPUIgCAYVAAAAAB0AAAAAJQAAAAAtAAAAADUAAAAAPQAAAABCIAgHFQAAgD8dAACsQiXy2z1BLQAAgD81AAAwQT3SzMdAQiAICRUAAD1DHQAARUMlZmZBQy0AACBANQCAQEM9G21AQKoEBAgBEALCBCA1MmViNWE0OWU5MTk0YjZlODI3MTcyOTA1YTVkYWVhZcoEB2luZGV4RELSBAVFQ0RTQeIEB1dpbmRvd3PqBAE48gQGQ2hyb21l+gQDMTMzigUgOTY3ODM4OTJkNDZmNDQ3YTg3N2I2YjhhMzQ1ZTIyNmKSBR4VAADAQB0AAHRCJQAATEItAAAAADUAAHBCPWB2lkGaBRt2MS41LjE5LW1pbm9yMy1ob3RmaXgzLTE0NDeqBSYQ4Ia2SxiopLcpIP7fufXRMij9r8P10TIwiuLB9dEyUMbVwvXRMsIFBAECLgPKBQEB0AUB2AWHzrn10TLgBf+vw/XRMooGDjEwMy4xNDguOTQuMjAy',
    'origin': 'https://app.apollo.io',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.apollo.io/',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'bc9c4bb67ddd42d5b06f72917400b7c0-aa41348774136c22-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'x-csrf-token': 'EInZhu2GInjebcPqNPorQ5vmfX3qWfl8hkx7DZU9HlOnj_NGMBY2pc6dM8lMOVR6iTf0LAWfbsPrCY6hRozumw',
    # 'cookie': 'hubspotutk=9ca7476ca1baad58a0131a336f1ab705; __hssrc=1; _cioanonid=37ed9b33-f752-40ce-c317-d38af7ec0dca; intercom-device-id-dyws6i9m=3e865b8c-2873-44b8-93fc-be9c91b556a5; __hstc=21978340.9ca7476ca1baad58a0131a336f1ab705.1739964788639.1739964788639.1739973709833.2; zp__initial_referrer=https://app.apollo.io/; zp__initial_landing_page=https://www.apollo.io/sign-up; zp__utm_source=app.apollo.io; zp__initial_utm_source=app.apollo.io; _gcl_au=1.1.2083301737.1739975059; pscd=get.apollo.io; _ga=GA1.1.486573424.1739975060; _hjSession_3601622=eyJpZCI6ImY1OGQ4ODQ3LTkxODgtNGEzYS04ZTBlLTk4YjcwMDExNDU1MCIsImMiOjE3Mzk5NzUwNjAxODQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=; _fbp=fb.1.1739975060242.270887012264759929; __qca=P0-1582380679-1739975060425; _clck=11n0p7l%7C2%7Cftk%7C0%7C1876; blueID=5fab2d58-52d1-4425-8fef-c58a51f4da2c; _hjSessionUser_3601622=eyJpZCI6IjVmZjUwMDUxLTgyM2EtNWVhYS1iMGE3LTlmZTkwZGU5OThhYSIsImNyZWF0ZWQiOjE3Mzk5NzUwNjAxODEsImV4aXN0aW5nIjp0cnVlfQ==; ZP_Pricing_Split_Test_Variant=24Q4_UC_AA59_V2; __cf_bm=u2jP1Z0GKDAY69O6bAgs631z6aNEtVpY_7tOBCc.sPg-1739975977-1.0.1.1-xldayc1aZ_o7d9aI32PPAc7zpL9kdmU3aIMI1Eue4Orrc4M4Iwcjq.I9qIQvWA1RnBLHQc9eKhMA4zgnag70PA; ZP_LATEST_LOGIN_PRICING_VARIANT=24Q4_UC_AA59_V2; _cioid=67b5ed6cc2ee40001d40bd06; _uetsid=3583bc40eecd11ef8ffa557b82490e64; _uetvid=358447f0eecd11efb0eef7582ef58e91; _clsk=1xlp68z%7C1739976174782%7C5%7C1%7Cs.clarity.ms%2Fcollect; _ga_76XXTC73SP=GS1.1.1739975059.1.1.1739976412.60.0.1132395544; cf_clearance=ZLUaRqcqaJVaq1i2pN3xd3LFD2ko6ka3qY4JSEo2vHM-1739976457-1.2.1.1-WEAcfZFQwSk_yW8w.KZ_pwcEBy1IaplsuW0gH2EEUA1zGTz.07a5beHrPNVs58060ePMp5oawDleWzumApLSjYzUPWlhHZUq35Y6ANlp9NFc9WDfd_jgcid4hW2vYxT0tDrH4kwV_6RKVUGGB0kK80b3cV3A7eYfjoUyWCUbengYEnxu.pVxdO.yvgNzNHtS7uecSwrinZf0Uey8YoyuWXaVeGnogtGnnRRRTWwwqApJeudLMnVn5pAbdiJjaXCuIv48CxyXS4uJm5klIlUlJcfG.difUFOvAyjp1iIBdLNSZ5SwO8u2D2K33niuzdmHTTYFvKNdlFnUHWMyXe2lCg; intercom-session-dyws6i9m=eC8zVmZGRU9wb29WY1hiZU5aaW5kVEVVRkdtSVNNbVNrZVBrMERON1ltVVlOVkhudTdQTzVhdnZjZTBJWjMwMU9SSjdMdDNUT0w3cEhCL2I0NDRIaitZUVVLUWxnU0hlU3RvMzV3WXgzUTQ9LS01VjZoc3ZZZjBIQ2k5bEsvN3RVMjdnPT0=--52875230a57e6e5fac30723d15c848de3fd58ec2; GCLB=CLiY0dGaiaziPhAD; dwnjrn=b3635901e13e99e26cdec76608053f0c9a5ce84c73d7654210254a390c6fe63d; dwndvc=bd187e075dbf913403df1a9e38ed847e679cb66db74bc3e6db40c5d32a0a8ae6; amplitude_id_122a93c7d9753d2fe678deffe8fac4cfapollo.io=eyJkZXZpY2VJZCI6IjEyMGExNzU2LTRiYzYtNGIyOC05YTE5LThiZGVmMGFmMjNiNlIiLCJ1c2VySWQiOiI2N2I1ZWQ2Y2MyZWU0MDAwMWQ0MGJkMDYiLCJvcHRPdXQiOnRydWUsInNlc3Npb25JZCI6MTczOTk3MzcwOTQ0MCwibGFzdEV2ZW50VGltZSI6MTczOTk3NjUwMDg1MCwiZXZlbnRJZCI6MiwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjJ9; __hssc=21978340.15.1739973709833; X-CSRF-TOKEN=EInZhu2GInjebcPqNPorQ5vmfX3qWfl8hkx7DZU9HlOnj_NGMBY2pc6dM8lMOVR6iTf0LAWfbsPrCY6hRozumw; _leadgenie_session=0C7bMjJwbfIH6obuD1QVxY%2BpcwSfsk8DseJkjLEXdrT5NVZeFVW6qmsPvc11ibn29spPESd8AJT4fevgP8a8IuqWJW%2Fw%2FQgHsb25YWHeaZjWF7WSHlM9tU%2Bdm4AE6rBc41nvZxg79B%2BFdfKyS3hmNau13pDcNmt3DpYMBxE4PTdKc5yCl1ynTTROK72By6xu7MxKtAyp3EfUSH6uK%2F5Y9hOpqPVQxfJ1BuiuUuMUVKrsHdYTTP9pCVBr%2Bs4Rkktk6TvVzV8NjbewYGlJDIB8Hope%2FbMEEoIa7v4%3D--KYdubstZY3ufYeZD--juVl9hWYLomkvVlqSiTxZA%3D%3D; _dd_s=rum=0&expire=1739977560962',
}

chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--enable-webgl")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass detection
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--headless")
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
chrome_options.add_argument(f"user-agent={random_user_agent}")
chrome_options.add_argument("--headless")

data = get_working_proxies()
ip = data["proxy"]
country = data["country"]
#print(f"IP: {ip} | Country: {country}")

options = {
    'proxy': {
        'http': f'http://{ip}',
        'https': f'https://{ip}',
        'no_proxy': 'localhost,127.0.0.1'
    }
}
chrome_options.add_argument(f'--proxy-server=http://{ip}')
driver = uc.Chrome(driver_executable_path=driver_path, options=chrome_options, seleniumwire_options=options)
#driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": headers})
#url = "https://app.apollo.io/#/people?page=2&sortByField=%5Bnone%5D&sortAscending=false&qOrganizationKeywordTags[]=Car%20Dealership&qOrganizationKeywordTags[]=Dealership&qOrganizationKeywordTags[]=car&includedOrganizationKeywordFields[]=tags&includedOrganizationKeywordFields[]=name&organizationLocations[]=United%20States&organizationLocations[]=Dubai%2C%20United%20Arab%20Emirates&organizationLocations[]=Singapore&personLocations[]=United%20States&personLocations[]=Dubai%2C%20United%20Arab%20Emirates&personLocations[]=Singapore&contactEmailStatusV2[]=verified&personTitles[]=owner&personTitles[]=ceo&personTitles[]=cfo&personTitles[]=cto&personTitles[]=coo&prospectedByCurrentTeam[]=no&organizationNumEmployeesRanges[]=86%2C1200"
driver.get("https://httpbin.org/ip")
print(driver.page_source)
time.sleep(1000)


url = "https://mit.s.dk/studiebolig/login/"
driver.get(url)
driver.maximize_window()
user_id = "mdabdullah"
user_pass = "@#ABdullah298"
time.sleep(2)
driver.find_element(By.ID,"id_username").send_keys(user_id)
driver.find_element(By.ID,"id_password").send_keys(user_pass+Keys.ENTER)
if "Hello" in driver.page_source:
    print("✅ Login Successfull.")
else:
    print("❌ Login unsuccesful.")
driver.quit()