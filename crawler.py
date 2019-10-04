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
from selenium import webdriver


class Spider:
    """
    A class that could crawl the video from url
    The API of Tencent video searching is
    'http://v.qq.com/x/search/?q=[keyword]'
    """

    # Init the information of crawler
    def __init__(self, url):
        self.name = "Zackaree"
        # urllib.request.urlopen() do not support the url both have English and Chinese
        # So we should use urllib.parse.quote to split the url
        # That we make sure urllib could open the url correctly
        url_s = quote(url, safe=string.printable)
        self.url = url_s

    def Get_list(self):
        """
        Get the video list from html
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

    def free_Downloader(self):
        """
        Download the video
        # @ http://vv.video.qq.com/getinfo : the API that get 270p json from v.qq.com
        # @ http://vv.video.qq.com/getkey  : the API that get 480p json from v.qq.com
        :return:
        """
        self.Get_list()


        for link in self.links:
            # Split the id of video
            vid = ((link.split('.', 5)[-2]).split('/'))[-1]

            # ==================================================================================================
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
            root = "D:\\"
            print("Downloading: " + root + filename + ".....")
            with open(root + filename, 'wb') as f:
                f.write(res)
            print("Download completed!")

    def vip_Downloader(self):
        """
        # @ https://play.fo97.cn/?url=  : 全网vip
        # @ http://www.guandianzhiku.com/v/s/?url= : 智库解析
        # @ https://www.ckmov.vip/api.php?url= : 解析系统
        :return:

        """
        self.Get_list()

        link = self.links[1]
        # This part can download the vip video from v.qq.com
        url = 'https://www.ckmov.vip/api.php?url= ' + link

        browser = webdriver.Chrome(executable_path='./chromedriver')
        vip_html = browser.get(url)
        print(vip_html)
        # browser.close()
        # browser.quit()

        # for list in vip_soup.find_all('video'):
        #    print(list)


if __name__ == '__main__':
    spider = Spider('http://v.qq.com/x/search/?q=假面骑士创骑')
    spider.vip_Downloader()
