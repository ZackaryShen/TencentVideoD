#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Zackary
# @Software: PyCharm
# @Email   : szbltyy@hotmail.com
# @Time    : 2019/9/28 23:28

"""
This is an simple crawler which could download the videos from
Tencent video (http://www.v.qq.com). This just a program for
entertainment.
"""

from urllib import request
from urllib.parse import quote
import string
from bs4 import BeautifulSoup
import json
from selenium import webdriver  # used to simulate the action of web browser
from selenium.webdriver import ActionChains  # used to simulate the action of mouse
import time  # used to get a delay
from selenium.webdriver.common.keys import Keys  # used to simulate the action of keyboard
import win32clipboard as wc  # used to get the conten from clipboard
import win32con
import pyautogui
import os


class Spider:
    """
    A class that could crawl the video from url
    The API of Tencent video searching is
    'http://v.qq.com/x/search/?q=[keyword]'
    """

    # Init the information of crawler
    def __init__(self, keyword):
        # urllib.request.urlopen() do not support the url both have English and Chinese
        # So we should use urllib.parse.quote to split the url
        # That we make sure urllib could open the url correctly
        url = 'http://v.qq.com/x/search/?q=' + keyword
        url_s = quote(url, safe=string.printable)
        self.keyword = keyword
        self.url = url_s

    def Get_list(self):
        """
        Get the video list from html
        !!!Remember:
        This part can not crawl the correct link from different page
        So when you want to crawl the video, you need to inspect the label of html
        and rewrite this part so that you can get the correct link from page
        :return:
        """
        # get the html by keyword
        main_res = request.urlopen(self.url)
        result_html = main_res.read()
        # change the encode
        main_data = result_html.decode("utf-8")
        main_soup = BeautifulSoup(main_data, 'html.parser')
        # get the first video from album
        href = main_soup.find_all('a', attrs={'_stat': 'video:poster_num'})[0]['href']

        # jump to the play page
        play_res = request.urlopen(href)
        play_html = play_res.read()
        play_data = play_html.decode("utf-8")
        play_soup = BeautifulSoup(play_data, 'html.parser')

        # Get all the link of page
        # The first link is incorrect
        self.links = []
        for list in play_soup.find_all('a', attrs={'_stat': "videolist:click"})[5:]:
            self.links.append('https://v.qq.com' + list['href'])

    # ==========================================================================================================
    # This functon is used to download the free video from tencent
    # But it's only support download the 270p and 480p
    def free_Downloader(self):
        """
        Download the video using urllib.request and BeautifulSoup
        # @ http://vv.video.qq.com/getinfo : the API that get 270p json from v.qq.com
        # @ http://vv.video.qq.com/getkey  : the API that get 480p json from v.qq.com
        :return:
        """

        self.Get_list()
        root = "D:\\" + self.keyword + '\\'
        if os.path.exists(root) is False:
            os.mkdir(root)
        num = 1

        for link in self.links:
            # Split the id of video
            vid = ((link.split('.', 5)[-2]).split('/'))[-1]
            get_json = request.urlopen("http://vv.video.qq.com/getinfo?vids=" + vid +
                                       "&platform=101001&charge=0&otype=json&defn=shd")
            get_json = get_json.read().decode('utf-8')[len('QZOutputJson='): -1]
            tempStr = json.loads(get_json)
            # v_270p_url = tempStr['vl']['vi'][0]['ul']['ui'][0]['url']+\
            #              tempStr['vl']['vi'][0]['fn']+"?vkey="+tempStr['vl']['vi'][0]['fvkey']

            # get the 480p
            filename = vid + '.mp4'
            file_n = 'filename=' + filename
            get_json2 = request.urlopen('http://vv.video.qq.com/getkey?format=2' +
                                        '&otype=json&vt=150&vid=' + vid + '&ran=0\%2E9477521511726081' +
                                        '\\&charge=0&' + file_n + '&platform=11')
            get_json2 = get_json2.read().decode('utf-8')[len('QZOutputJson='): -1]
            tempStr2 = json.loads(get_json2)
            v_480p_url = tempStr['vl']['vi'][0]['ul']['ui'][0]['url'] + filename + '?vkey=' + tempStr2['key']

            res = request.urlopen(v_480p_url).read()
            files = self.keyword + '第' + str(num) + '集.mp4'
            num += 1
            print("Downloading: " + root + files + ".....")
            with open(root + filename, 'wb') as f:
                f.write(res)
            print("Download completed!")

        print('All videos of the album have been downloaded!')

    # ==========================================================================================================

    def vip_Downloader(self):
        """
        Use API download the vip video using selenium
        !!!Remember:
        Different videos have different result by using different API
        So if it doesn't work by using one
        you need to change to another
        API can be got from the API.py
        :return:

        """

        self.Get_list()
        root = "D:\\" + self.keyword + '\\'
        if os.path.exists(root) is False:
            os.mkdir(root)
        num = 1

        for link in self.links:
            url = 'http://yun.360dy.wang/jx.php?url=' + link
            # use webdriver simulate the action of chrome
            browser = webdriver.Chrome(executable_path='./chromedriver.exe')
            browser.get(url)
            time.sleep(10)  # wait the url loading
            right_click = browser.find_element_by_tag_name('div')
            # ActionChain could simulate the action of mouse and keyboard
            rightclick = ActionChains(browser)

            # double right click, get the menu
            rightclick.context_click(right_click)
            rightclick.context_click(right_click).perform()
            time.sleep(1)

            # choose the "copy video address..." option
            pyautogui.typewrite(['down', 'down', 'down', 'down', 'down'])
            time.sleep(1)
            # it must write the "enter", else the choice can't be chosen
            pyautogui.typewrite(['enter'])
            time.sleep(1)
            video_url = str(self.get_clipboard())[2:]

            res = request.urlopen(video_url).read()
            filename = self.keyword + '第' + str(num) + '集.mp4'
            print("Downloading: " + root + filename + ".....")
            with open(root + filename, 'wb') as f:
                f.write(res)
            print("Download completed!")
            num += 1
            time.sleep(5)
        browser.close()
        browser.quit()

    def get_clipboard(self):
        """
        To get the content of clipboard
        so we can get the real url of video
        :return:
        """
        wc.OpenClipboard()
        url = wc.GetClipboardData(win32con.CF_TEXT)
        wc.CloseClipboard()  # it must be close, else we will get the same url from clipboard
        return url

if __name__ == '__main__':
    spider = Spider('假面骑士创骑')
    spider.vip_Downloader()