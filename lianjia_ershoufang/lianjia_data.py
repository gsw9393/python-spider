import requests
from lxml import etree
from bs4 import  BeautifulSoup
base_url = "https://tj.lianjia.com"

def get_region_url_of_tianjing():
    xiaoqu_url = ['/xiaoqu/nankai/']
    target = base_url + xiaoqu_url[0]
    r = requests.get(target)

    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(r.text)

    ret = []
    parser = etree.HTMLParser(encoding='utf-8')
    html = etree.parse('test.html', parser=parser)
    res = html.xpath('/html/body/div[3]/div[1]/dl[2]/dd/div/div/a/@href')
    for region_url in res:
        ret.append(base_url + region_url)

    return ret

def get_region_detail_info(region_url):
    resp = requests.get(region_url)
    soup = BeautifulSoup(resp.text)
    tag = soup.find_all('div', attrs={'class':'page-box house-lst-page-box'})
    dicStr = tag[0]['page-data']

    # find the total page of the region ershoufang
    Index01 = dicStr.find(':')
    Index02 = dicStr.find(',')
    totalPage = dicStr[Index01 + 1 : Index02]

    ret = []
    base_url = 'https://tj.lianjia.com/xiaoqu/heping/'
    for i in range(int(totalPage) + 1):
        if i == 0:
            pass
        elif i == 1:
            ret = [base_url]
        else:
            pageIndex = str(i)
            ret.append(base_url + 'pg' + pageIndex + '/')
    return ret

def get_detail_xiaoquUrl_info(xiaoqu_url):
    resp = requests.get(xiaoqu_url)
    soup = BeautifulSoup(resp.text)
    xiaoqus = soup.find_all('li', attrs = {'clear xiaoquListItem'})
    ret_xiaoqu_urls = []
    for xiaoqu in xiaoqus:
        links = xiaoqu.find('a')
        ret_xiaoqu_urls.append(links['href'])

    return ret_xiaoqu_urls


def get_xiaoqu_info(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)

    ret = {}
    xiaoquInfos = soup.find_all('div', attrs={'class':'xiaoquInfo'})

    for xiaoquInfo in xiaoquInfos:
        items = xiaoquInfo.find_all('div')
        for item in items:
            spanInfos = item.find_all('span')
            ret[spanInfos[0].text] = spanInfos[1].text

    return ret



print(get_xiaoqu_info('https://tj.lianjia.com/xiaoqu/1211046425881/'))