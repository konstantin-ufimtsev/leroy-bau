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
from selenium.webdriver.common.action_chains import ActionChains
import logg
import input_xlsx

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
    logg.logging.info('Сообщение отправлено в телеграм')

def time_now():
    now = datetime.now() 
    current_time = now.strftime("%H:%M:%S") 
    return current_time

def get_driver(url: str):
    
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
    
    try:
        driver.get(url)
        logg.logging.info(f'Драйвер ЗАГРУЖЕН для страницы: {url}')
    except Exception as ex:
        logg.logging.info(f'Драйвер НЕ ЗАГРУЖЕН для страницы: {url} ,ошибка - {ex}')
    
    get_page_data(driver, url)
    

def get_page_data(driver, url:str):
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 't12nw7s2_pdp')))
        logg.logging.info(f'Цена ЗАГРУЖЕНА со страницы: {url}')
    except Exception as ex:
        logg.logging.info(f'Цена НЕ ЗАГРУЖЕНА со страницы {url}, ошибка - {ex}')

    try:
        driver.execute_script("window.scrollBy(0,800)")
        logg.logging.info(f'Скролл ВЫПОЛНЕН для страницы: {url}')
    except Exception as ex:
        logg.logging.info(f'Скролл НЕ ВЫПОЛНЕН для страницы: {url}, ошибка - {ex}')

    try:
        driver.find_element(By.CSS_SELECTOR, "div[class='sy2hk37_pdp']").click()
        logg.logging.info(f'Кнопка остатков НАЖАТА для страницы: {url}')
    except Exception as ex:
        logg.logging.info(f'Кнопка остатков НЕ НАЖАТА для страницы: {url}, ошибка - {ex}')
    
    #driver.get_screenshot_as_file("screenshot.png")
    try:
        article = driver.find_element(By.CLASS_NAME, 't12nw7s2_pdp').text.split()[1]
        title = driver.find_element(By.TAG_NAME, 'h1').text
        price = driver.find_element(By.CSS_SELECTOR, "div[data-testid='prices_mf-pdp']").text.split('\n')
        if len(price) == 1:
            price = price[0].split('₽')[0].replace(' ', '')
        else:
            price = price[1].split('₽')[0].replace(' ', '')
        logg.logging.info(f'Данные ПОЛУЧЕНЫ со страницы: {url}')
    except Exception as ex:
        logg.logging.info(f'Данные НЕ ПОЛУЧЕНЫ со страницы {url},ошибка {ex}')
    
    try:
        stocks = driver.find_element(By.CSS_SELECTOR, "div[class='sy2hk37_pdp']").find_elements(By.CSS_SELECTOR, "li[data-qa='stock-in-store-item']")
        
        qty_omsk = []
        qty_krasnodar = []
        
        kaliningrad = ['Леруа Мерлен Калининград']
        omsk = ['Леруа Мерлен Омск Мега', 'Леруа Мерлен Омск Амурская']
        krasnodar = ['Леруа Мерлен Краснодар СБС', 'Леруа Мерлен Краснодар Западный обход', 'Леруа Мерлен Краснодар Адыгея']
        novorossiysk = ['Леруа Мерлен Новороссийск']
        pushkino = ['Леруа Мерлен Пушкино']

        for stock in stocks:
            stock_list:list = stock.text.split('\n')
            if stock_list[1] == 'Нет в наличии':
                stock_list[1] = 0
            if stock_list[0] in kaliningrad:
                city:str = 'Калинниград'
                qty:float = float(stock_list[1].rsplit(' ',1)[0].replace(' ', ''))
                unit:str = stock_list[1].rsplit(' ',1)[1].replace('.', '')
                #print(city, qty, unit)
            elif stock_list[0] in novorossiysk:
                city:str = 'Новороссийск'
                qty = float(stock_list[1].rsplit(' ',1)[0].replace(' ', ''))
                unit:str = stock_list[1].rsplit(' ',1)[1].replace('.', '')
                #print(city, qty, unit)
            elif stock_list[0] in pushkino:
                city:str = 'Пушкино'
                qty = float(stock_list[1].rsplit(' ',1)[0].replace(' ', ''))
                unit:str = stock_list[1].rsplit(' ',1)[1].replace('.', '')
                #print(city, qty, unit)
            elif stock_list[0] in omsk:
                city:str = 'Омск'
                qty_omsk.append(float(stock_list[1].rsplit(' ',1)[0].replace(' ', '')))
                unit:str = stock_list[1].rsplit(' ',1)[1].replace('.', '')
                qty = sum(qty_omsk)
                #print(city, qty, unit)
            elif stock_list[0] in krasnodar:
                city:str = 'Краснодар'
                qty_krasnodar.append(float(stock_list[1].rsplit(' ',1)[0].replace(' ', '')))
                unit:str = stock_list[1].rsplit(' ',1)[1].replace('.', '')
                qty = sum(qty_krasnodar)
                #print(city, qty, unit)
        res = (city, article, title, price, qty, unit)
        
        logg.logging.info(f'Считали остатки товара:{url}')
        print(res)
    
    except Exception as ex:
        logg.logging.info(f'НЕ СЧИТАЛИ остатки товара: {url} - ошибка - {ex}')        
            
   
   
def main():

    query = input_xlsx.read_file()

    with multiprocessing.Pool(processes=3) as mp:
        mp.map(get_driver, query)
    
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



