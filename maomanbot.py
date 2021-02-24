from telegram.ext import Updater, MessageHandler, Filters  # import modules
import requests
from bs4 import BeautifulSoup

my_token = '1637024128:AAFeEEwtb4Ko1Vo-6PlV3QBWBnbGtdrzs8I'

print('start telegram chat bot')

def get_message(update, context):
    links = []
    #사용자로 부터 키워드를 입력받는다
    word = update.message.text
    keyword = "".join(word.split()) #키워드에 공백이 있을경우 이를 지워준다
    update.message.reply_text("{} 포함된 뉴스 기사 5개를 가져옵니다.".format(keyword))

    #링크 추출하기
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={keyword}'
    req = requests.get(url) #링크 주소를 통해 HTTP로부터 필요한 HTML정보를 가져온다
    html = req.text #그 중 text를 가져온다 여기서 text는 div~일케된 html구조의 부분이다
    #Beautifulsoup는 가져온 데이터를 파싱하도록 도와주는 매소드다
    #파싱이란 아직은 잘 모르겠으나 html의 문법구조를 변환시켜서 파이썬에 적용하도록 해주는 것 같다

    soup = BeautifulSoup(html, 'html.parser') #request를 통해 가져온 데이터를 알맞게 변환시킨다

    search_result = soup.select_one('#news_result_list') #news_result_list라는 객체 하나를 가져와서 search_result라는 변수에 넣는다?
    news_list = search_result.select('.bx > .news_wrap > a') #news_list는 최신뉴스 전부를 가져오는것 같다
    
    #select와 select_one의 차이는 select는 객체를 가져와 리스트에 저장한다.
    

    #담겨진 최근뉴스 처음부터 5개까지 for문을 돌린다
    for news in news_list[:5]:
        link = news['href'] #href는 뉴스의 링크를 담당한다. 링크들을 links라는 리스트에 하나씩 추가한다
        links.append(link)
    

    #뉴스 링크 출력
    for link in links:
        update.message.reply_text(link)




updater = Updater(my_token, use_context=True)

message_handler = MessageHandler(Filters.text, get_message)
updater.dispatcher.add_handler(message_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()
