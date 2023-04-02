import requests
response = requests.get("https://arca.live/b/hotdeal")
if response.status_code != 200: #if response code is 200(normal response)
	exit() #exit the program
else:
	content = response.content #return error message

from bs4 import BeautifulSoup 
item_lists = [] #contain the info.
ended_lists = []

#finding ALL the items
soup = BeautifulSoup(content, 'html.parser') #parsing the content
item_html_list = soup.find_all(class_="vrow hybrid") #1. find all items with class="vrow hybrid"

for item in item_html_list: #start categorizing
    title = item.find("a", class_="title").get_text().strip() #get the title
    price = item.find("span", class_="deal-price").get_text().strip() #get the price
    badge = item.find("a", class_="badge").get_text().strip() #get the badge(category)
    delPrice = item.find("span", class_="deal-price").get_text().strip() #get the delivery price
    item_lists.append(dict(name = title, price = price, type=badge, delPrice = delPrice))
    #append to item_list with dictionary

#finding ended(or ded) items
soup = BeautifulSoup(content, 'html.parser') #parsing the content
item_ded_list = soup.find_all(class_="vrow-top deal deal-close") #you can see it is closed

for ded in item_ded_list:
    ded_add = ded.find("a", class_ = "title") #get the title
    ended_lists.append(ded_add.get_text().strip()) #and add it to ended_list

is_ded = False #in order to check if the item is ended
for a in range(len(item_lists)):
    for b in range(len(ended_lists)):
        if(item_lists[a]['name'] == ended_lists[b]): #compare the item
            is_ded = True #it is ded item lol. do not print it
            break
    if(not is_ded): #not ded: print it
        print(item_lists[a]['name'], item_lists[a]['price'], item_lists[a]['type'], item_lists[a]['delPrice'])

'''
name: 제품 이름
price: 제품 가격
delPrice: 배송비
type: 제품의 종류
(생활용품, 식품, PC/하드웨어, SW/게임, 전자제품, 의류, 화장품, 상품권/쿠폰, 기타)
asdf
'''