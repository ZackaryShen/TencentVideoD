## Tencent Video Downloader 
This is a project that could download the free or vip video from [Tencent video]("http://v.qq.com"). This just a little project for fun, please do not use it in commerce。

#### 1. lib
* **urllib.request**: to simulate the request
* **urllib.parse.quote**: transform the chinese character to utf-8 char
* **bs4.BeautifulSoup**: to extract the source from html
* **selenium.webdriver**: to simulate the action of web browser
* **selenium.webdriver.ActionChains**: to simulate the action of mouse
* **import win32clipboard**: to get the conten from clipboard
* **pyautogui**: click the browser

#### 2. the class: API
This class is used to get the API, only have these API can you download the vip video

#### 3. the class: crawler
*I define a class named Spider to crawl the video and download them*

1. **\_\_init\_\_(self, keyword)**
   > Initate the crawler, get the keyword, and change it to utf-8 code and save the keyword and the search url by splicing the api of tencent

2. **Get_list(self)**
   > To get the links of video from display album. **This part can not crawl the correct link from different page. So when you want to crawl the video, you need to inspect the label of html, and rewrite this part so that you can get the correct link from page**

3. **vip_Downloader(self)**
   > Use API download the vip video using selenium. Different videos have different result by using different API. **So if it doesn't work by using one, you need to change to another.** And API can be got from the API.py

#### 4. Shortage
1. You have to rewrite the function Get_list() when you want to download different video
2. You have to wait and do not move the mouse out of the browser which will get a wrong reslut
3. Didn't change the API automatically, you have to try which one can download the vip video.
4. Course the lib win32, the program only run in Windows!

#### 5. About
If you have any questions, email me in szbltyy@hotmail.com