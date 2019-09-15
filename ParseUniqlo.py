
import time
import queue
import datetime

from scrapy.selector import Selector

def ParseUniqlo(cur_url, response):

    
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
    for obj in response.xpath('//*[@id="secondary"]'):
            print('get Product')
            name = response.xpath('//*[@id="goodsNmArea"]/text()').extract_first()
            color = response.xpath('//*[@id="listChipColor"]/li[contains(@class, "selected")]/a/@title').extract_first()
            if name == [] or name is None:
                continue
            item['name'] = name[2:]
            item['site'] = 'Uniqlo'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            item['objID'] = response.xpath('//*[@id="basic"]/li[4]/text()').extract_first()
            item['image_urls'] = response.xpath('//*[@id="prodImgDefault"]/img/@src').extract_first() 
            colors = response.xpath('//*[@id="listChipColor"]/li/a/@title').extract()
            item['colors'] = colors
            item['sizes'] = response.xpath('//*[@id="listChipSize"]/li/a/em/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            gender = name[:3]
            print(gender)
            if gender.find('女') != -1:
                item['gender'] = '女'
            elif gender.find('男') != -1:
                item['gender'] = '男'
            else :
                item['gender'] = '童'
            print(item['gender'])

            nameSplit = [item['name']]
            #衣服類
            if  nameSplit[0].find('衫') >= 0 \
                or nameSplit[0].find('背心') >= 0 or nameSplit[0].find('洋裝') >= 0:
                item['category'] = '衣服'
            #外套類
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0 or nameSplit[0].find('大衣') >= 0:
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0 or nameSplit[0].find('罩') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0  or nameSplit[0].find('內褲') >= 0:
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
                item['category'] = '配件'
            
            price = response.xpath('//*[@id="price"]/text()').extract_first()
            item['price'] = price[3:]
            item['store_price'] = price[3:]
           
    return item
