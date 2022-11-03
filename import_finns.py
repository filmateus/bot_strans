# import packages
import pandas as pd
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import chromedriver_binary
import pyodbc
import datetime
from pyodbc import Error
from datetime import timedelta, date
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from datetime import timedelta, date
from datetime import date

# login and passaword
f=open("account.txt","r")
lines=f.readlines()
username=lines[0]
password=lines[1]
site = lines[2]
site_login = lines[3]
f.close()


def login_acess_Menu():
  print("login called")
  if driver.current_url == site_login:
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'usuario')))       
        element.send_keys(username)
        element = driver.find_element(By.ID, "password")
        element.send_keys(password)
        element = driver.find_element_by_id('Entrar')
        element.click()
        WebDriverWait(driver, 12).until(EC.invisibility_of_element((By.CLASS_NAME, 'loading-root')))
        print("Login successfully")
    except Exception as e:
        print("Login failed")
    try:
        #acess the search of the taxs
        element = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
        'body > div.bg > div > div.bg.ng-scope > div.ng-scope > header > nav > div > ul > li.menu-principal.menu-dropdown')))
        element.click()
        element = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.CSS_SELECTOR, 
        'body > div > div > div.bg.ng-scope > div.ng-scope > header > nav > div > ul > li.menu-principal.menu-dropdown.open > ul > div > li:nth-child(1) > ul > li:nth-child(1) > a')))
        element.click()
        element = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.ID,'abaBuscaAvancada')))
        element.click()
        print("Acess Menu successfully")
    except:
        print("Acess Menu failed")


# list for append 
finn = []

def get_list_finn():
    print("get_list_finn caled")
    WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, 'loading-root')))
    time.sleep(5)
    table_id = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#vm\.id > tbody')))
    rows = table_id.find_elements(By.TAG_NAME, "tr") 
    for row in rows:
        auto = row.find_elements(By.TAG_NAME, "td")[1]
        finn.append(auto.text)
        print(auto.text)
    try:
        element =  WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.ID, "vm.id_next")))
        element.click()
        get_list_finn()
    except:
        print('Fail')
        

def interval_day():
    print("interval days called")
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'inicioInfracao')))   
        today = date.today()
        end_date = today - datetime.timedelta(days=3)
        element.send_keys(end_date.strftime("%d/%m/%Y"))
        element = driver.find_element(By.ID, "fimInfracao")
        element.send_keys(today.strftime("%d/%m/%Y"))
        print("Último dia: ", end_date.strftime("%d/%m/%Y"))
        Select(driver.find_element(By.ID, "cbxTamanhoPagina")).select_by_value('100')
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnBuscaAvancada')))
        element.click()
        get_list_finn()
    except Exception as e:
        print(f"Fim da infrações. Total: '{len(finn)}'")


def souce_finn(auto):
    driver.find_element(By.ID, 'inicioInfracao').clear()
    driver.find_element(By.ID, "fimInfracao").clear()

    print("souce called")
    if auto[:2] == 'TR':
        origin = "Radar"
    else:
        origin = "DOFT"
    print(origin)
    try:
        print("Start Search")
        time.sleep(0.75)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'codigo')))
        element.clear()
        element.send_keys(str(auto))
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'btnBuscaAvancada')))
        time.sleep(0.5)
        element.click()
        element = WebDriverWait(driver, 12).until(EC.invisibility_of_element((By.CLASS_NAME, 'loading-root')))
        table_id = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#vm\.id > tbody')))
        driver.implicitly_wait(10)
        print("Information SEI:")
        rows = table_id.find_elements(By.TAG_NAME, "tr") 
        for row in rows:
            sei = row.find_elements(By.TAG_NAME, "td")[11]
            print(sei.text)
        
        for row in rows:
            placa = row.find_elements(By.TAG_NAME, "td")[7]
            print(placa.text)

        
        print("Accessing the info box")
        
        driver.implicitly_wait(10)
        element = WebDriverWait(driver, 12).until(EC.invisibility_of_element((By.CLASS_NAME, 'loading-root')))
        element = WebDriverWait(driver, 12).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vm.id"]/tbody/tr/td[2]')))
        element.click()
        time.sleep(0.75)

        # get adress
        adress = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[5]/div/div[1]')[0].text
        if adress == '':
            adress = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[5]/div/div[2]')[0].text
        if adress == '':
            adress = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[6]/div/div[2]')[0].text
        adress = adress.split(': ', 1)[1]
        print(adress)
        

        code = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[6]/div/div[1]')[0].text
        if code == '':
            code =  driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[7]/div/div[1]')[0].text
        code = code.replace(' - ', '')
        code = code.split(': ', 1)[1]
        print(code)
        
        # get reg
        reg = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[6]/div/div[7]')[0].text
        if "Matrícula" not in reg:
            reg = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[7]/div/div[7]')[0].text
        reg = reg.split(': ', 1)[1]
        print(reg)

        # get  date and hours
        date_hour = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[5]/div/div[5]')[0].text
        if date_hour == '':
            date_hour = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[6]/div/div[5]')[0].text
        date_hour = date_hour.split(': ', 1)[1]
        print(date_hour)

        type_car = driver.find_elements_by_xpath('//*[@id="imprimirMulta"]/fieldset[2]/div/div[1]')[0].text
        type_car = type_car.split(': ', 1)[1]
        print(type_car)

        print("all informations load")
    except Exception as e:
        print(e)
        print("Erro in informations load")
    try:
        print("Saving the information")
        
        command = f"""INSERT INTO autos_strans(NUM_AUTO, NAM_PLACA, NAM_ENDERECO, DT_DATA_HORA ,COD_INFRACAO, COD_MATRICULA, CH_SNE, CH_ORIGIN, TIP_CARRO) 
                                        VALUES('{auto}', '{placa.text}',' {adress}', '{date_hour}', {code}, {reg}, '{sei.text}', '{origin}', '{type_car}')"""
        cursor.execute(command)
        print("Saved information")
    except Exception as e:
      print(e)
      print("don't save")
    try:
        WebDriverWait(driver, 12).until(EC.invisibility_of_element((By.CLASS_NAME, 'loading-root')))
        time.sleep(0.7)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnFecharDetalhe"))).click()
    except Exception as e:
      print(e)
      print("ERROR")


try:
    con = pyodbc.connect(
    r'Driver={SQL Server};'
    r'Server=DESKTOP-R02SDIT;'
    r'Database=BD_STRANS;')
    print("SQL Server Database connection successful")
except Error as err:
    print(f"Error: '{err}'")


driver = webdriver.Edge() 
driver.get(site)

login_acess_Menu()

interval_day()

get_list_finn()

cursor = con.cursor()

for auto in finn:
    # origin_list.append(origin)   
    print("Auto:", auto)
    souce_finn(auto)
    
cursor.close()
con.commit()
con.close()
driver.close()