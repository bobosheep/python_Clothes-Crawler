
import time
import queue
import datetime
import pickle
import base64

from bs4 import BeautifulSoup
from selenium import webdriver
from scrapy.selector import Selector
from ParseLativ import ParseLativ
from ParseNet import ParseNet
from Parse50percent import Parse50Percent
from ParseUniqlo import ParseUniqlo

from elasticsearch import Elasticsearch


es = Elasticsearch()

def Parser(cur_url, pageSource, crawl_config):
    soup = BeautifulSoup(pageSource, 'html.parser')
    response = Selector(text=pageSource)
    item = dict()
    if cur_url.find('lativ') > 0:
        #lativ website
        item = ParseLativ(cur_url, response)
        
    #End of if cur_url.find('lativ') > 0
    if cur_url.find('net-fashion') > 0:
        # net website
        item = ParseNet(cur_url, response)
    #End of if cur_url.find('net-fashion') > 0
    if cur_url.find('50-shop') > 0:
        # 50 percent website
        item = Parse50Percent(cur_url, response)
    #End of if cur_url.find('50-shop') > 0
    if cur_url.find('uniqlo') > 0:
        # 50 percent website
        item = ParseUniqlo(cur_url, response)
    #End of if cur_url.find('uniqlo') > 0


    if item['name'] != [] and item['name'] is not None and item['name'] is not '':

        if crawl_config['insertDB']:
            id=base64.urlsafe_b64encode(str.encode(item['img_url'])).decode('ascii')
            es.index(index='clothes', doc_type='clothes', body=item, id=id)
        else:    
            with open(crawl_config['output_dir'] + crawl_config['output_file'], "a+", encoding='utf8') as fopen:
                for key in item :
                    line = '@' + key + ':' + str(item[key]) + '\n'
                    #line = json.dumps(dict(item),ensure_ascii=False) + "\n"
                    fopen.write(line)
                fopen.write('\n')
    
    find_links = soup.find_all('a')
    return find_links





