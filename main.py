import logging
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import telebot
import schedule
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
import random



#logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#    datefmt='[%d.%m.%Y-%H:%M:%S]',
#    level=logging.DEBUG,
    #filename="log.log",
    #filemode='w',
    #encoding='utf-8'
#    )


#kld_door_send_bot
#6753878735:AAH7bfqhXVIwI0wSLTp-mjMb6kjeuAqF3OY
#438152630 #chat_id

def read_from_file(filename) -> list:
    pass


def write_to_file(link_list: list):
    pass


def write_to_database():
    pass


#sending the url to telegram
def send_to_telegram(message:str):
    token = '6753878735:AAH7bfqhXVIwI0wSLTp-mjMb6kjeuAqF3OY'
    bot = telebot.TeleBot(token)
    chat_id = '438152630'
    bot.send_message(chat_id, message)

def time_now():
    now = datetime.now() 
    current_time = now.strftime("%H:%M:%S") 
    return current_time

def get_page_data(url):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('log-level=3') #убирает инфо сообщения селениум
        options.add_argument("--headless=new")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        
        
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    '''
    })
        
        driver.get(url)
        
        try:
            element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 't12nw7s2_pdp')))
        finally:

        #time.sleep(random.randint(8, 12))
        #driver.maximize_window()
        #driver.get_screenshot_as_file("screenshot.png")
            article = driver.find_element(By.CLASS_NAME, 't12nw7s2_pdp').text.split()[1]
            title = driver.find_element(By.TAG_NAME, 'h1').text
            price = driver.find_element(By.CSS_SELECTOR, "div[data-testid='prices_mf-pdp']").text.split('\n')
            if len(price) == 1:
                price = price[0].split('₽')[0].replace(' ', '')
            else:
                price = price[1].split('₽')[0].replace(' ', '')
                

            print(article)
            print(title)
            print(price)
            
    except Exception as ex:
        print(ex)


def main():
    query_list = [
        'https://kaliningrad.leroymerlin.ru/product/radiator-rifar-monolit-500-100-bimetall-8-sekciy-bokovoe-podklyuchenie-cvet-belyy-12876448/',
        'https://kaliningrad.leroymerlin.ru/product/sifon-dlya-moyki-equation-d-90-mm-s-vypuskom-perelivom-i-otvodom-dlya-stiralnoy-mashiny-18550959/',
        'https://kaliningrad.leroymerlin.ru/product/vodonagrevatel-nakopitelnyy-100-l-zanussi-splendore-zwh-s-2-kvt-vertikalnyy-gorizontalnyy-nerzhaveyushchaya-stal-mokryy-ten-82108182/',
        'https://kaliningrad.leroymerlin.ru/product/sol-tabletirovannaya-barer-universalnaya-25-kg-17895568/',
        'https://novorossiysk.leroymerlin.ru/product/sifon-dlya-vanny-equation-s-vypuskom-s-reviziey-18551011/',
        'https://novorossiysk.leroymerlin.ru/product/kran-sharovoy-20-mm-standartnyy-prohod-polipropilen-82222148/',
        'https://novorossiysk.leroymerlin.ru/product/vodonagrevatel-nakopitelnyy-35-l-aquaverso-es-15-kvt-vertikalnyy-emalirovannaya-stal-mokryy-ten-18669546/'
    ]
    
    with multiprocessing.Pool(processes=3) as mp:
        mp.map(get_page_data, query_list)
    
    #schedule.every(2).minutes.do(get_page_data)
    #while True:
    #    schedule.run_pending()

if __name__ == "__main__":
    
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    
    result_time = round((float(end_time - start_time) / 60), 1)

    send_to_telegram(f'Время выполнения парсинга: {result_time} минут!')
    
    #print('Время выполнения парсинга:', round((float(end_time - start_time) / 60), 1),' минут!')



