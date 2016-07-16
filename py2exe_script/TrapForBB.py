#!
#--* coding=utf-8 *--
import urllib2
from bs4 import BeautifulSoup as bs
import base64
import subprocess
import re
import time
import logging
import os, sys

# Define
FILE_PATH = "./web_links.txt"
URLDICT = {
    u"南宁市科技局": "http://www.nnst.gov.cn",
    u"南宁市工信委": "http://219.159.80.227/info/infopen.htm",
    u"南宁市发改委": "http://fgw.nanning.gov.cn",
    u"南宁市农业局": "http://www.nnny.gov.cn",
    u"南宁市环保局": "http://www.nnhb.gov.cn",
    u"南宁市商务局": "http://sw.nanning.gov.cn",
    u"广西工信委": "http://www.gxgxw.gov.cn",
    u"广西科技厅": "http://www.gxst.gov.cn",
    u"广西发改委": "http://www.gxdrc.gov.cn",
    u"广西农业信息网": "http://www.gxny.gov.cn",
    u"广西商务厅": "http://www.gxswt.gov.cn",
    u"南宁市中小企业信息网": "http://www.smenn.gov.cn",
    u"广西中小企业信息网": "http://www.smegx.gov.cn",
}
KEYWORD = [u'申报', u'项目', u'通知', u'验收', u'立项', u'资金', u'课题']
AVOIDWORD = [u'通知公告', u'在线申报', u'招商项目', u'项目申报指南', u'项目申报',
             u'农村经济项目', u'招商项目']

# define logger
logger = logging.getLogger(u"Excavator")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)

def readLinks(file_path):
    print u"开始读取网站列表".encode('utf-8')
    with open(file_path, 'r') as f:
        lines = f.readlines()
    result_dict = {}
    for i in lines:
        print i
        site_name = i.split("=")[0].strip("\n")
        site_url = i.split("=")[1].strip("\n")
        result_dict[site_name] = site_url
    return result_dict



def checkWebLinks(file_path):
    """
    check if web links file exists. if not, will reset a default one
    """
    sleep_time = 10
    if not os.path.exists(file_path):
        print u"找不到网站列表,已经重新生存web_links.txt。".encode("utf-8")
        with open('./web_links.txt', 'w') as f:
            for k, v in URLDICT.items():
                f.write('%s=%s\n' % (k.encode('utf-8'),v))
        print u"%d 秒后将读取默认列表..." % sleep_time
        time.sleep(sleep_time)
    url_dict = readLinks(file_path)
    return url_dict


def trapAllLinks(URLDICT):
    result_list = {}
    for website, url in URLDICT.items():
        # logger.debug("Digging %s..." % website)
        try:
            page_content = urllib2.urlopen(url)
            soup = bs(page_content)
            links_in_pages = soup.find_all('a')
            result_list[website] = links_in_pages
            # logger.debug("Dug %s, got %d links." % (website, len(links_in_pages)))
        except:
            logger.debug("Dug %s Failed" % website)
            pass
    return result_list


def parseURL(website, a_soup):
    result_dict = {}
    for key_word in KEYWORD:
        for link in a_soup:
            # Title less than 8 characters will be drop
            if key_word in link.text and len(link.text.strip()) > 8:
                result_dict[link.text.strip()] = sillyURLReformat(
                    website, link['href'])
    return result_dict


def sillyURLReformat(website, url):
    """
    The silly website doesn't use stand url format so need to assembling again
    """
    if website == u"南宁市工信委":
        url = "http://219.159.80.227/" + url
    if url.startswith("./"):
        url = URLDICT[website] + url.replace("./", "/")
    elif url.startswith("http://"):
        pass
    elif not url.startswith("/"):
        url = URLDICT[website] + '/' + url
    elif 'java' in url:
        pass
    elif URLDICT[website] in url:
        pass
    else:
        url = URLDICT[website] + url
    return url


def exportToHTML(result_dict):
    table_container = ""
    for website, title_and_link in result_dict.items():
        website_line = "<tr><td><H2>" + website + "</H2></td></tr>"
        for title, link in title_and_link.items():
            link_line = "<tr><td>" + \
                "<a href=\"%s\" target=_blank>%s</a>" % (link, title) + "</td></tr>"
            website_line += link_line
        website_line += "<tr><td></td></tr>"
        table_container += website_line
    html_container = u"""
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>旺旺的挖掘机</title>
        </head>
        <body>
        <table>
        %s
        </table>
        <hr>
        I'm a Robot of voostar@gmail.com!
        </body>
        </html>
        """ % table_container
    file_time = time.localtime()
    file_name = "%d-%d-%d %d%d.html" % (
        file_time.tm_year,
        file_time.tm_mon,
        file_time.tm_mday,
        file_time.tm_hour,
        file_time.tm_min,)
    with open('./' + file_name, 'w') as f:
        f.write(html_container.encode("utf-8"))


def main():
    start = time.time()
    print u"检查: 网站列表是否存在".encode('utf-8')
    checkWebLinks(FILE_PATH)
    print u"任务开始于 ".encode('utf-8') + time.ctime()
    result_dict = {}
    # get all links in target websites
    all_link_in_soup = trapAllLinks(URLDICT)
    for website, a_soup in all_link_in_soup.items():
        # logger.debug("Parsing %s..." % website)
        title_and_link = parseURL(website, a_soup)
        result_dict[website] = title_and_link
        # logger.debug("Parsed %s, Matched %d links." %
        #              (website, len(title_and_link)))

    # Show result
    print '=' * 80
    print 'Result'
    print '=' * 80
    for website, title_and_link in result_dict.items():
        print 'Result of %s : %s' % (website.encode("utf-8"), URLDICT[website])
        print '-' * 40
        for title, link in title_and_link.items():
            print '- %s' % title.encode("utf-8")
            print '- %s' % link
            print ''
        print '-' * 40
    print '=' * 80
    print 'EOF'
    print '=' * 80
    print '-> I\'m a Robot of longzhiw'
    end = time.time()
    print "Job finish at " + time.ctime()
    print "Cost time %s" % str(end - start)

    exportToHTML(result_dict)

if __name__ == '__main__':
    main()