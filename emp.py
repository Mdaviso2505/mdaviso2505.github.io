import requests
from bs4 import BeautifulSoup
import time
import string
import random

random_alpha = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

url = "https://en.mrproblogger.com/shimul"
country_code = random.choice(["US", "BE", "GB", "CA", "BR", "NZ", "AU", "SE", "FR", "ES", "DE", "IN"])
proxies = {
    "https": "socks5h://gf2452822202-region-"+country_code+"-period-1440-sid-"+random_alpha+":qbz4xwk7xs@59ax82obyh.g.go2proxy.net:16888"
}

headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'sec-ch-ua': "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
  'sec-ch-ua-mobile': "?1",
  'sec-ch-ua-platform': "\"Android\"",
  'upgrade-insecure-requests': "1",
  'sec-fetch-site': "cross-site",
  'sec-fetch-mode': "navigate",
  'sec-fetch-dest': "document",
  'referer': "https://themezon.net/",
  'accept-language': "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7",
  'priority': "u=0, i",
  'Cookie': "lang=en_US; _ga=GA1.1.1621600059.1745842090; __ppIdCC=nrprovkoffer_xon217458469.973.; _clck=s5dq39%7C2%7Cfvg%7C0%7C1944; _ga_YWLL2122G2=GS1.1.1745842090.1.1.1745842111.0.0.0"
}

response = requests.get(url, headers=headers, proxies=proxies)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")
cookies = response.cookies.get_dict()

url2 = "https://en.mrproblogger.com/links/go"

payload2 = {
  '_method': "POST",
  '_csrfToken': soup.find("input", {"name": "_csrfToken"})["value"],
  'ad_form_data': soup.find("input", {"name": "ad_form_data"})["value"],
  '_Token[fields]': soup.find("input", {"name": "_Token[fields]"})["value"],
  '_Token[unlocked]': soup.find("input", {"name": "_Token[unlocked]"})["value"]
}

headers2 = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
  'Accept': "application/json, text/javascript, */*; q=0.01",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'sec-ch-ua-platform': "\"Android\"",
  'x-requested-with': "XMLHttpRequest",
  'sec-ch-ua': "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
  'sec-ch-ua-mobile': "?1",
  'origin': "https://en.mrproblogger.com",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': url,
  'accept-language': "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7",
  'priority': "u=1, i",
  'Cookie': "lang=en_US; _ga=GA1.1.1621600059.1745842090; __ppIdCC=nrprovkoffer_xon217458469.973.; AppSession="+cookies["AppSession"]+"; csrfToken="+cookies["csrfToken"]+"; app_visitor="+cookies["app_visitor"]+"; ab=2; _ga_YWLL2122G2=GS1.1.1746095415.2.0.1746095415.0.0.0; _clck=s5dq39%7C2%7Cfvj%7C0%7C1944; clever-counter-89823=0-1; prefetchAd_7737531=true; __viCookieActive=true; _clsk=1r6zroc%7C1746095417913%7C1%7C1%7Ci.clarity.ms%2Fcollect"
}
time.sleep(12)
response2 = requests.post(url2, data=payload2, headers=headers2, proxies=proxies)

print(response2.status_code)
print(response2.json()["message"])