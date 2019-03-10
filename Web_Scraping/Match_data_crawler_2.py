#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 21:10:16 2019

@author: donghoon
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 13:03:22 2019

@author: donghoon
지정한 시즌과 클럽의 정보를 가져옴.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
import time

'''
Function definition starts
'''

#이 함수는 모든 클럽을 돌면서 정보 수집하도록 바꿀 것
def club_match_nums(html,match_container,info): 
    #사이트 진입
    print("Scraping...")
    driver=webdriver.Chrome('/Users/donghoon/Downloads/chromedriver')
    driver.get(html)
    time.sleep(2)
    #광고가 떠있으면 제거
    try:
        elem=driver.find_element_by_xpath('//*[@id="advertClose"]')
        elem.click() 
    except:
        print("No Ad")
    #스크롤을 내림
    body=driver.find_element_by_tag_name("body")
    body.send_keys(Keys.PAGE_DOWN)
    #지정한 필터대로 로딩이 될 떄까지 기다림
    time.sleep(3)
    html=driver.page_source
    obj=soup(html,"html.parser")
    temp=obj.find('body').find('main',{"id":"mainContent"}).find("div",{"class":"tabbedContent"}).find("section",{"class":"pageFilter col-12 fixturePagefilter"}).find("div",{"data-dropdown-block":"teams"}).find("div",{"class":"current"}).text     
    info.append(temp)
    temp=obj.find('body').find('main',{"id":"mainContent"}).find("div",{"class":"tabbedContent"}).find("section",{"class":"pageFilter col-12 fixturePagefilter"}).find("div",{"data-dropdown-block":"compSeasons"}).find("div",{"class":"current"}).text     
    info.append(temp)
    print(info)
    container=obj.find("div",{"class":"tabbedContent"}).find_all("li",{"class":"matchFixtureContainer"})
    for i in container:
        match_container.append("https://www.premierleague.com/match/"+i.find('div')['data-matchid'])
    driver.quit()
    print(str(len(match_container))+" of matches found.")
    return None

#메치 데이터를 사용 가능한 형대로 만들 것.
def match_dat(match_html,info):
    #match_num의 주소로 들어가서 테이블에 나온 경기 정보들을 모두 긇어오는 함수이다.
    driver=webdriver.Chrome('/Users/donghoon/Downloads/chromedriver')
    #특정한 경기의 주소로 들어간다.
    driver.get(match_html)
    time.sleep(1)
    while True:
        body=driver.find_element_by_tag_name("body")
        #해당 페이지에서 stat이라는 버튼이 보이지 않으면 스크롤을 내림
        if bool(driver.find_element_by_xpath("//*[@id=\"mainContent\"]/div/section/div[2]/div[2]/div[1]/div/div/ul/li[3]"))==False:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
        #해당 페이지에서 stat이라는 버튼이 보이면 클릭
        elif driver.find_element_by_xpath("//*[@id=\"mainContent\"]/div/section/div[2]/div[2]/div[1]/div/div/ul/li[3]"):
            elem=driver.find_element_by_xpath("//*[@id=\"mainContent\"]/div/section/div[2]/div[2]/div[1]/div/div/ul/li[3]")
            elem.click()
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            table=[]
            #data_refined will give data on posession, SOT ratio, passes ratio
            data_refined=[]
            while len(table)==0:
                #인터넷이 느리면 이곳에서 터질 수 있으니 유의할 것.
                html=driver.page_source
                mcdat=soup(html,"html.parser")
                print("Scaping match stat")
                time.sleep(0.5)
                table=mcdat.find("div",{"class":"mcTabsContainer"}).find("tbody",{"class":"matchCentreStatsContainer"}).find_all("td")
                head=mcdat.find("div",{"class":"mcTabsContainer"}).find("thead").find_all("th")
            print("Successfully collected data!")
            if(info[0] in head[0].text):
                data_refined=home(table)
            else:
                data_refined=away(table)
            data_refined.insert(0, head[0].text)
            data_refined.insert(0, head[2].text)
            print(data_refined)
            driver.quit()
            break
        else:
            print("Unexpoected case occured.")
            break
    return data_refined

def home(array):
    temp=[]
    #possesion
    temp.append(float(array[0].text))
    #shots on target
    if float(array[5].text)!=0:
        temp.append(float(array[3].text)/float(array[5].text))
    else:
        temp.append(float(array[3].text))
    #passes
    temp.append(float(array[12].text)/float(array[14].text))
    return temp

def away(array):
    temp=[]
    #possesion
    temp.append(float(array[2].text))
    #shots on target
    if float(array[3].text)!=0:
        temp.append(float(array[5].text)/float(array[3].text))
    else:
        temp.append(float(array[5].text))
    #passes
    temp.append(float(array[14].text)/float(array[12].text))
    return temp

def get_club_stat(html,match_container):
    info=[]
    analyze=[]
    #참고로 info[0]에는 팀명이, info[1]에는 시즌이 저장된다.
    club_match_nums(html,match_container,info)
    for i in match_container:
        analyze.append(match_dat(i,info))
    for i in range(len(analyze)):
        print(analyze[i])
    return None
'''
Testing part starts
'''
Arsnal_1718=[]
get_club_stat('https://www.premierleague.com/results?co=1&se=210&cl=1',Arsnal_1718)

