#나도 모르는 미지의 영역, 건들었다가는 *될지도 모르는 영역
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    #chrome_options.add_argument('--lang=ko_KR')
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument('--window-size=1920x1080')
    #chrome_options.add_argument(
    #    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)
    return driver
#여기서부터는 그래도 아는 영역

badges = [] #뱃지(상품 범위)를 담을 리스트
delivery_prices = [] #배송비를 담을 리스트
prices = [] #가격을 담을 리스트
titles = [] #제목을 담을 리스트
shops = [] #쇼핑몰 이름을 담을 리스트
shop_links = []
site_links = []
deleted_lists = [] #삭제된 핫딜 제품의 이름을 담을 리스트
badgeInput = ""

def list_maker(fromsoup, check, list_name):
    for check in fromsoup:
        if check.text.strip() != '':
            list_name.append(check.text.strip())
        elif check.text.strip() == '':
            list_name.append('카테고리 없음')
            
def hotdeal_main(page_num): #핫딜 함수
    url = "https://arca.live/b/hotdeal?p="+str(page_num) #핫딜채널에서
    
    driver = set_chrome_driver() #새 드라이버 세팅
    
    print(url) 
    
    driver.get(url)
    
    html_content = driver.page_source #페이지 소스를 가져온다
    soup = BeautifulSoup(html_content, 'html.parser') #그걸 파싱한다
    shop = soup.findAll("span", {'class': 'deal-store'}) #핫딜채널에서 쇼핑몰 이름을 가져온다
    title = soup.findAll("a", {'class': 'title'}) #핫딜채널에서 제목을 가져온다
    badge = soup.findAll("a", {'class': 'badge'}) #핫딜채널에서 뱃지를 가져온다
    price = soup.findAll("span", {'class': 'deal-price'}) #핫딜채널에서 가격을 가져온다
    delivery_price = soup.findAll("span", {'class': 'deal-delivery'}) #핫딜채널에서 배송비를 가져온다
    site_link = soup.findAll("a", {'class': 'title'}) #핫딜채널에서 링크를 가져온다
    deleted_list = soup.findAll("div", {'class': 'vrow-top deal deal-close'}) #지금은 핫딜이 아닌 리스트를 불러온다

    list_maker(shop, 'deal-store', shops) #쇼핑몰 이름을 리스트에 담는다
    list_maker(badge, 'badge', badges) #뱃지를 리스트에 담는다  
    list_maker(price, 'deal-price', prices) #가격을 리스트에 담는다
    list_maker(delivery_price, 'deal-delivery', delivery_prices) #배송비를 리스트에 담는다
        
    for deleted in deleted_list: #구조상 한 번 더 검색해야함
        deleted_add = deleted.find("a", {'class': 'title'})
        if deleted_add:
            deleted_lists.append(deleted_add.text.strip())
    
    for title_add in title: #title class의 구조상 핫딜 채널 이라는게 자동적으로 나옴, 그걸 제외하고 리스트에 담는다
        if title_add.text.strip() == '핫딜 채널':
            pass
        elif title_add.text.strip() != '':
            titles.append(title_add.text.strip())
        elif title_add.text.strip() == '':
            titles.append('제목 없음')

    for link_add in site_link:
        site_links.append(link_add.get('href'))
    driver.quit() #드라이버를 종료한다
    

def hotdeal_page(site_link): #쇼핑몰 링크 가져옴
    url = site_link #input으로 url 설정
    driver = set_chrome_driver() #드라이버 세팅
    driver.get(url) #드라이버로 받기
    
    html_content = driver.page_source #패이지 소스 가져옴
    soup = BeautifulSoup(html_content, 'html.parser') #파싱
    shop_link = soup.findAll("a", {"class": 'external'}) #쇼핑몰 링크 있는 a태그 가져옴
    shop_links.append(shop_link[0].get('href')) #그중 링크만 가져옴
    
    driver.quit()

print("웹 사이트 크롤링 중...") #메인 크롤링
if __name__ == "__main__":
    for page_num in range(1, 3):
        hotdeal_main(page_num)
print("분석 완료")

if __name__ == "__main__":
    for a in range(1, 3):
        hotdeal_page("https://arca.live" + site_links[a])

for a in range(0, len(shop_links)):
    shop_links[a] = "https://" + shop_links[a].strip("https://oo.pe/")

#badgeInput = input("원하는 핫딜 상품의 품목 입력: ")
for a in range(0, len(shop_links)): #리스트로 비교한다
    ''' if(badges[a]==badgeInput): #원하는 목록에 
        for b in range(0, len(deleted_lists)): 
            if(titles[a]!=deleted_lists[b]): #
                print("제목:", shops[a], titles[a])
                print("가격:", prices[a], "배송비:",delivery_prices[a])
                print("사이트:", 'arca.live'+links[a])
                break '''
    print(shop_links[a])
    

#shops[a], titles[a], badges[a], prices[a], delivery_prices[a],'arca.live'+links[a]