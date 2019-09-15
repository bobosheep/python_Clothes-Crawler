
import time
import queue
import datetime

from scrapy.selector import Selector

def Parse50Percent(cur_url, response):

    item = dict({
                "site":"",
                "name":"",
                "gender":"",
                "category":"",
                "url":"",
                "objID":"",
                "image_urls":"",
                "price":"",
                "store_price":"",
                "color":"",
                "colors":"",
                "sizes":"",
                "last_updated":""
            })

    for obj in response.xpath('//*[@id="main_content"]'):
            
            name = response.xpath('//*[@id="products_intro_content"]/p[contains(@class, "item_name")]/text()').extract_first()
            color = response.xpath('//*[@id="colors"]/a[contains(@class, "selected")]/@color').extract_first()
            if name == [] or name is None:
                continue
            name = name.split('\n')
            name = ''.join(name)
            name = name.split(' ')
            name = ''.join(name)
            item['name'] = name
            item['site'] = 'fiftypercent'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            id = response.xpath('//*[@id="products_intro_content"]/span[contains(@class, "item_no")]/text()').extract_first()
            item['objID'] = id.split(' ')[1]
            print(item['obj_id'])
            item['image_urls'] = response.xpath('//*[@id="show-image"]/@src').extract_first() 
            item['colors'] = response.xpath('//*[@id="colors"]/a/@color').extract()
            item['sizes'] = response.xpath('//*[@id="sizes"]/a/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            check_gender = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_ucMain_navigator"]/text()').extract_first()

            if  check_gender.find('WOMEN') != -1:
                item['gender'] = '女'
            elif  check_gender.find('MEN') != -1:
                item['gender'] = '男'
            else :
                item['gender'] = 'None'

            nameSplit = [item['name']]
            #衣服類
            if nameSplit[0].find('T恤') >= 0 or nameSplit[0].find('衫') >= 0  \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            #外套類
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 \
                or nameSplit[0].find('夾克') >= 0 or nameSplit[0].find('外搭') >= 0  or nameSplit[0].find('大衣') >= 0:
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0 or nameSplit[0].find('罩') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0 or nameSplit[0].find('內褲') >= 0:
                item['category'] = '內褲'
            #褲裙類
            elif nameSplit[0].find('褲') >= 0 or nameSplit[0].find('裙') >= 0:
                item['category'] = '褲裙'
            #鞋類
            elif nameSplit[0].find('鞋') >= 0 :
                item['category'] = '鞋'
                
            elif nameSplit[0].find('T') >= 0 or nameSplit[0].find('衣') >= 0 :
                item['category'] = '衣服'
            #配件
            else :
                item['category'] = '其他'
            
            
            if response.xpath('//*[@id="products_intro_content"]/p[contains(@class, "item_name")]/span[contains(@class, "price")]/span/text()').extract_first():
                #優惠價
                price = response.xpath('///*[@id="products_intro_content"]/p[contains(@class, "item_name")]/span[contains(@class, "price")]/text()').extract_first()
                item['price'] = price.split('.')[1]
                #原價
                price = response.xpath('//*[@id="products_intro_content"]/p[contains(@class, "item_name")]/span[contains(@class, "price")]/span/text()').extract_first()
                item['store_price'] = price.split('.')[1]
            else :  #可能沒有優惠價
                #價格
                price = response.xpath('///*[@id="products_intro_content"]/p[1]/span[contains(@class, "price")]/text()').extract_first()
                item['price'] = price.split('.')[1]

    return item

