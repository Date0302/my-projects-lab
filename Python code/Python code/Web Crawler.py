import jieba.posseg as pseg
import matplotlib.pyplot as plt
from os import path
import requests
from scipy.misc import imread
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import time
from lxml import etree
import random
from fake_useragent import UserAgent
import tkinter
from tkinter import ttk
# from PIL import Image


'''
def xici_ip(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    for num_page in range(1, page+1):
        url_part = "http://www.xicidaili.com/wn/"
        url = url_part + str(num_page)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            trs = soup.find_all('tr')
            for i in range(1,len(trs)):
                tr = trs[i]
                tds = tr.find_all('td')
                ip_item = tds[1].text + ':' + tds[2].text
                print('抓取第' + str(page) + '页第' + str(i) + '个：' + ip_item)
                with open('get_xici_ip.txt', 'a', encoding='utf-8') as f:
                    f.writelines(ip_item + '\n')
                time.sleep(1)
            return ('储存成功')

def get_ip():
    with open('get_xici_ip.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return random.choice(lines)

def check_ip():
    # good_ip = []
    good = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    proxies = {'HTTPS': 'HTTPS://' + get_ip().replace('\n', '')}
    try:
        r = requests.get('http://www.baidu.com', headers=headers, proxies=proxies, timeout=10)
        if r.status_code == 200:
            # good_ip.append(proxies)
            return good.append(proxies)
            # return proxies
    except Exception as e:
        print(e)

def main():
    # xici_ip(1)
    try:
        # return check_ip()
        print(check_ip())
    except Exception as e:
        print(e)
        check_ip()
'''


class Spider:
    ua = UserAgent(verify_ssl=False)

    def __init__(self):
        self.root = tkinter.Tk()

    def douban_comments(self):
        headers = {'User-Agent': Spider.ua.random}
        # proxies = main()
        # 豆瓣网top250书籍首页
        # url = "https://book.douban.com"
        url = url_input.get()
        if url == 'https://book.douban.com':
            for i in range(0, 1):
                urls = url + '/top250?start=' + 'str(i*25)'
                html = requests.get(urls, headers=headers).text
                page = etree.HTML(html)
                book_urls_list = page.xpath('//tr[@class="item"]/td/div/a/@href')
                book_name_list = page.xpath('//tr[@class="item"]/td/div/a/@title')
                for book_name in book_name_list:
                    log_msg1 = '匹配到《' + str(book_name) + '》' + '\n'
                    log_text.insert(tkinter.END, log_msg1)
                    log_text.see(tkinter.END)
                    log_text.update()
                print(book_urls_list)
                # 得到每一本书对应的评论url
                for book_urls in book_urls_list:
                    comments_urls = book_urls + 'comments/hot?p='
                    print(comments_urls)
                    # 获取每一本书前一百页的评论url
                    for j in range(1, 2):
                        comments_url = comments_urls + 'str(j)'
                        comments = requests.get(comments_url, headers=headers)
                        # print('开始爬取第{}页评论.'.format(j))
                        log_msg2 = '开始爬取第{}页评论.'.format(j) + '\n'
                        log_text.insert(tkinter.END, log_msg2)
                        log_text.see(tkinter.END)
                        log_text.update()

                        comments_soup = BeautifulSoup(comments.text, 'lxml')
                        pattern = comments_soup.find_all('p', 'comment-content')
                        with open('douban.txt', 'a+', encoding='utf-8') as f:
                            for s in pattern:
                                # print(s, type(s))
                                f.write(str(s))
                        j = j + 1
                        time.sleep(1)
                i = i + 1
                time.sleep(1)
            spi_end = '--------爬取完成--------' + '\n'
            log_text.insert(tkinter.END, spi_end)
            log_text.see(tkinter.END)
            log_text.update()
        elif url == 'https://hr.tencent.com':
            self.tencent_position()
        else:
            self.error_msg()

    @staticmethod
    def tencent_position():
        headers = {'User-Agent': Spider.ua.random}
        url = url_input.get()
        for i in range(0, 20):
            urls = url + '/position.php?&start=' + 'str(i*10)'
            html = requests.get(urls, headers=headers).text
            log_msg2 = '开始爬取第{}页职位.'.format(i) + '\n'
            log_text.insert(tkinter.END, log_msg2)
            log_text.see(tkinter.END)
            log_text.update()
            page = etree.HTML(html)
            for position in page.xpath('//tr[@class="even"]/td[1]/a/text() | //tr[@class="odd"]/td[1]/a/text()'):
                with open('tencent.txt', 'a+', encoding='utf-8') as f:
                    f.write(str(position))
            i = i + 1
            time.sleep(1)
        spi_end = '--------爬取完成--------' + '\n'
        log_text.insert(tkinter.END, spi_end)
        log_text.see(tkinter.END)
        log_text.update()

    @staticmethod
    def error_msg():
        msg = '请先输入正确的url~' + '\n'
        log_text.insert(tkinter.END, msg)
        log_text.see(tkinter.END)
        log_text.update()

    def make_image(self):
        make_image_text = '============================' + '\n' + '正在生成图片...请稍等...' + '\n'
        log_text.insert(tkinter.END, make_image_text)
        log_text.see(tkinter.END)
        log_text.update()
        global wordcloud_images
        url = url_input.get()
        if url == 'https://book.douban.com':
            with open('douban.txt', 'r', encoding='utf-8') as f:
                comment_subjects = f.readlines()
            stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
            commentlist = []
            for subject in comment_subjects:
                if subject.isspace():
                    continue
                # segment words line by line
                word_list = pseg.cut(subject)
                for word, flag in word_list:
                    if word not in stop_words and flag == 'n':
                        commentlist.append(word)
            d = path.dirname(__file__)
            timg_image = imread(path.join(d, "timg.png"))
            content = ' '.join(commentlist)
            wordcloud = ontWordCloud(f_path='simhei.ttf', background_color="grey",  mask=timg_image, max_words=40).generate(content)
            # Display the generated image:
            plt.imshow(wordcloud)
            plt.axis("off")
            wordcloud.to_file('wordcloud.gif')
            # plt.show()
            # wordcloud_image = Image.open('wordcloud.gif')
            wordcloud_images = tkinter.PhotoImage(file='wordcloud.gif')
            result_text.create_image(50, 50, anchor=tkinter.NW, image=wordcloud_images)
        elif url == 'https://hr.tencent.com':
            with open('tencent.txt', 'r', encoding='utf-8') as f:
                comment_subjects = f.readlines()
            stop_words = set(line.strip() for line in open('stopwords.txt', encoding='utf-8'))
            commentlist = []
            for subject in comment_subjects:
                if subject.isspace():
                    continue
                # segment words line by line
                word_list = pseg.cut(subject)
                for word, flag in word_list:
                    if word not in stop_words and flag == 'n':
                        commentlist.append(word)
            d = path.dirname(__file__)
            timg_image = imread(path.join(d, "timg.png"))
            content = ' '.join(commentlist)
            wordcloud = WordCloud(font_path='simhei.ttf', background_color="grey",  mask=timg_image, max_words=40).generate(content)
            # Display the generated image:
            plt.imshow(wordcloud)
            plt.axis("off")
            wordcloud.to_file('wordcloud_tencent.gif')
            # plt.show()
            # wordcloud_image = Image.open('wordcloud_tencent.gif')
            wordcloud_images = tkinter.PhotoImage(file='wordcloud_tencent.gif')
            result_text.create_image(50, 50, anchor=tkinter.NW, image=wordcloud_images)
        else:
            self.error_msg()

    def main(self):
        global url_input, log_text, result_text
        # 创建空白窗口,作为主载体
        # root = tkinter.Tk()
        self.root.title('爬虫工具')
        # 窗口的大小，后面的加号是窗口在整个屏幕的位置
        self.root.geometry('1068x715+10+10')
        # 创建菜单
        menubar = tkinter.Menu(self.root)
        fmenu = tkinter.Menu(menubar)
        # for each in ['新建', '打开', '保存', '另存为', '退出']:
        fmenu.add_command(label='新建')
        fmenu.add_command(label='打开')
        fmenu.add_command(label='保存')
        fmenu.add_command(label='另存为')
        fmenu.add_command(label='退出', command=self.root.quit, accelerator='(Ctrl+Q)')
        rmenu = tkinter.Menu(menubar)
        # for each in ['运行爬虫', '生成图片']:
        rmenu.add_command(label='运行爬虫', command=self.douban_comments, accelerator='(F11)')
        rmenu.add_command(label='生成图片', command=self.make_image, accelerator='(F12)')
        amenu = tkinter.Menu(menubar)
        for each in ['版权信息', '联系我们']:
            amenu.add_command(label=each)
        menubar.add_cascade(label='文件', menu=fmenu)
        menubar.add_cascade(label='运行', menu=rmenu)
        menubar.add_cascade(label='关于', menu=amenu)

        self.root['menu'] = menubar
        # 标签控件，窗口中放置文本组件
        tkinter.Label(self.root, text='请输入url:', font=("华文行楷", 20), fg='black').grid(row=0, column=0)

        # 定位 pack包 place位置 grid是网格式的布局
        tkinter.Label(self.root, text='输出结果:', font=("宋体", 20), fg='black').grid(row=1, column=12)
        tkinter.Label(self.root, text='爬取日志:', font=("宋体", 20), fg='black').grid(row=2, column=0)
        # Entry是可输入文本框
        # url_input = tkinter.Entry(self.root, font=("微软雅黑", 15))
        # url_input.grid(row=0, column=1)
        # 下拉框
        # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
        number = tkinter.StringVar()
        url_input = tkinter.ttk.Combobox(self.root, width=26, textvariable=number)
        # 设置下拉列表的值
        url_input['values'] = ('https://hr.tencent.com', 'https://book.douban.com')
        url_input.grid(column=1, row=0)


        # tkinter.Label(self.root, text='腾讯网url: https://hr.tencent.com', font=("微软雅黑", 10), fg='black').grid(row=2, column=1)
        # tkinter.Label(self.root, text='豆瓣网url: https://book.douban.com', font=("微软雅黑", 10), fg='black').grid(row=1, column=1)
        # 文本控件,打印日志
        log_text = tkinter.Text(self.root, font=('微软雅黑', 15), width=35, height=20)
        # columnspan组件所跨越的列数
        log_text.grid(row=4, column=0, rowspan=9, columnspan=10)
        # result_text = tkinter.Canvas(self.root, width=45, height=22)
        result_text = tkinter.Canvas(self.root, bg='white', width=550, height=600)
        result_text.grid(row=2, column=12, rowspan=15, columnspan=10)
        # 设置按钮 sticky对齐方式，N S W E
        tkinter.button = tkinter.Button(self.root, text='开始', font=("微软雅黑", 15), command=self.douban_comments).grid(row=13, column=0, sticky=tkinter.W)
        tkinter.button = tkinter.Button(self.root, text='退出', font=("微软雅黑", 15), command=self.root.quit).grid(row=13, column=10, sticky=tkinter.E)
        # 创建滚动条
        log_text_scrollbar_y = tkinter.Scrollbar(self.root)
        log_text_scrollbar_y.config(command=log_text.yview)
        log_text.config(yscrollcommand=log_text_scrollbar_y.set)
        log_text_scrollbar_y.grid(row=3, column=10, rowspan=9, sticky='NS')
        # 使得窗口一直存在
        tkinter.mainloop()


if __name__ == "__main__":
    spider = Spider()
    spider.main()


