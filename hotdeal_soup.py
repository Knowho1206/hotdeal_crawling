import requests
response = requests.get("https://arca.live/b/hotdeal")
if response.status_code != 200:
	exit()
else:
	content = response.content

from bs4 import BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

item_html_list = soup.find_all(class_="vrow hybrid")
item_list = []

for item in item_html_list:
    title = item.find("a", class_="title").get_text().strip()
    price = item.find("span", class_="deal-price").get_text().strip()
    badge = item.find("a", class_="badge").get_text().strip()
    delivery_price = item.find("span", class_="deal-delivery").get_text().strip()
    ended = item.find("div", class_="vrow-top deal deal-close")
    item_list.append(dict(name = title, price = price, type=badge, delPrice=delivery_price))

for item in item_list:
    print(f'{item["name"]} - {item["price"]}({item["delPrice"]}) ,{item["type"]}')

'''
name: 제품 이름
price: 제품 가격
delPrice: 배송비
type: 제품의 종류
(생활용품, 식품, PC/하드웨어, SW/게임, 전자제품, 의류, 화장품, 상품권/쿠폰, 기타)
'''