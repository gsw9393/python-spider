import os
import argparse
import pickle
import prettytable
from lxml import etree
from DecryptLogin import login
from bs4 import  BeautifulSoup

'''
    命令行参数解析函数
'''
def parse_args():
    parser = argparse.ArgumentParser(description = "下载指定微博用户的所有微博数据")
    parser.add_argument('--username', dest='username', help='用户名', type=str, required=True)
    parser.add_argument('--password', dest='password', help='密码', type=str, required=True)
    args = parser.parse_args()
    return args

'''
    目标用户微博数据爬取
'''

class WeiboSpider():
    @staticmethod
    def login(username, password):
        lg = login.Login()
        _, session = lg.weibo(username, password, mode = 'mobile')
        return session

    def __init__(self, username, password, **kwargs):
        self.session = WeiboSpider.login(username, password)
        self.header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
        }
        self.save_dir = os.path.join(os.getcwd(), 'datas')

    '''
        save the contents of the specified user to the 
        right file folder
    '''
    def __save(self, weibo_dict, user_id):
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

        filepath = os.path.join(self.save_dir, user_id + '.pkl')
        with open(filepath, 'wb') as fd:
            pickle.dump(weibo_dict, fd)

        return filepath

    def start(self):
        while True:
            user_id = input('请输入目标用户ID(例如: 3261134763) ——>  ')
            url = f'https://weibo.cn/{user_id}'
            res = self.session.get(url, headers = self.header)
            selector = etree.HTML(res.content)

            base_infos = selector.xpath("//div[@class='tip2']/*/text()")
            num_wbs, num_followings, num_followers = \
                int(base_infos[0][3:-1]), int(base_infos[1][3:-1]), int(base_infos[0][3:-1])

            num_wb_pages = selector.xpath("//input[@name='mp']")
            num_wb_pages = int(num_wb_pages[0].attrib['value']) if len(num_wb_pages) > 0 else 1
            url = f'https://weibo.cn/{user_id}/info'
            res = self.session.get(url, headers = self.header)
            soup = BeautifulSoup(res.text, "lxml")
            nickname = soup.find_all('title')[0].text[0:4]

            tb = prettytable.PrettyTable()
            tb.field_names = ['用户名', '关注数量', '被关注数量', '微博数量', '微博页数']
            tb.add_row([nickname, num_followings, num_followers, num_wbs, num_wb_pages])
            print('获取的用户信息如下:')
            print(tb)
            is_download = input('是否爬取该用户的所有微博?(y/n, 默认: y) ——> ')
            if is_download == 'y' or is_download == 'yes' or not is_download:
                userinfos = {'user_id': user_id, 'num_wbs': num_wbs, 'num_wb_pages': num_wb_pages}
                #self.__downloadWeibos(userinfos)
            is_continue = input('是否还需下载其他用户的微博数据?(n/y, 默认: n) ——> ')
            if is_continue == 'n' or is_continue == 'no' or not is_continue:
                break

    def __downloadWeibos(self, userinfos):
        pass


if __name__ == '__main__':
    #args = parse_args()
    wb_spider = WeiboSpider('17792246949', 'gsw930216')
    wb_spider.start()