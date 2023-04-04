import requests
response = requests.get("https://arca.live/b/hotdeal")
if response.status_code != 200: #if response code is 200(normal response)
	exit() #exit the program
else:
	content = response.content #return error message

from bs4 import BeautifulSoup 
items = [] #contain the info.
items_ended = []

#finding ALL the items
soup = BeautifulSoup(content, 'html.parser') #parsing the content
item_html_list = soup.find_all(class_="vrow hybrid") #1. find all items with class="vrow hybrid"

for item in item_html_list: #start categorizing
    title = item.find("a", class_="title").get_text().strip() #get the title
    site_link = item.find("a", class_="title")["href"] #get the link
    price = item.find("span", class_="deal-price").get_text().strip() #get the price
    badge = item.find("a", class_="badge").get_text().strip() #get the badge(category)
    delPrice = item.find("span", class_="deal-delivery").get_text().strip() #get the delivery price
    items.append(dict(
        name = title, price = price, 
        type = badge, 
        delPrice = delPrice, 
        link = "https://arca.live"+site_link))
    #append to item_list with dictionary

#finding ended(or ded) items
soup = BeautifulSoup(content, 'html.parser') #parsing the content
item_ded_list = soup.find_all(class_="vrow-top deal deal-close") #you can see it is closed

for ded in item_ded_list:
    ded_add = ded.find("a", class_ = "title") #get the title
    items_ended.append(ded_add.get_text().strip()) #and add it to ended_list


#in order to check if the item is ended
for b in range(len(items_ended)):
    for a in range(len(items)):
        if(items[a]['name'] == items_ended[b]):
            del items[a]
            break

''' 
출력
for a in range(len(items)):
    print(items[a]['name'], items[a]['price'], items[a]['type'], items[a]['delPrice'], items[a]['link']) '''

'''
name: 제품 이름
price: 제품 가격
delPrice: 배송비
type: 제품의 종류
(생활용품, 식품, PC/하드웨어, SW/게임, 전자제품, 의류, 화장품, 상품권/쿠폰, 기타)
asdf
'''