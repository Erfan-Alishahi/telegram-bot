import requests
from bs4 import BeautifulSoup


url = "https://www.gsme.sharif.ir/management-professors"
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print('!!!!!failed to load page!!!!!')

# h3 -->  name

soup = BeautifulSoup(html_content, "html.parser")

professors = soup.find_all("div", class_="professor-card")

data = []

for professor in professors:
    name = professor.find("h3").get_text(strip=True) if professor.find("h3") else None
    pic = professor.find("img")['src'] if professor.find("img") else None

    data.append({
        "Name": name,
        "pic": pic
    })

# نمایش داده ها

for i, prof in enumerate(data,start=1):
    print(f"{i}. {prof['Name']}^ {prof['pic']}")