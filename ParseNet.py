
import time
import queue
import datetime

from scrapy.selector import Selector

def ParseNet(cur_url, response):

    
    item = dict({
                "site":"",
                "name":"",
                "gender":"",
                "category":"",
                "url":"",
                "obj_id":"",
                "img_url":"",
                "price":"",
                "store_price":"",
                "color":"",
                "colors":"",
                "sizes":"",
                "last_updated":""
            })
    for obj in response.xpath('//*[@id="main"]'):
            print('get Product')
            name = response.xpath('//*[contains(@class, "product_detail_Right_title")]/text()').extract_first()
            color = response.xpath('//*[contains(@class, "product_color_block color_active")]/div/text()').extract_first()
            if name == [] or name is None:
                continue
            name = name.split('\n')
            name = ''.join(name)
            item['name'] = name
            item['site'] = 'NET'
            
            if item['name'] == [] or item['name'] is None:
                continue
            item['color'] = color[3:]
            print(item['name'])
            print(item['color']) 
            item['url'] = cur_url
            item['obj_id'] = response.xpath('//*[contains(@class, "product_detail_Right_numberL")]/span/text()').extract_first()
            item['img_url'] = response.xpath('//*[@id="PRODUCT_IMAGE_MAIN"]/@src').extract_first() 
            colors = response.xpath('//*[contains(@class, "product_color")]/div/div/text()').extract()
            tmparr = []
            for i in colors:
                tmparr.append(i[3:])
            item['colors'] = tmparr
            item['sizes'] = response.xpath('//*[contains(@class, "product_size")]/div/a/div[contains(@class, "product_size_block")]/text()').extract()
            item['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            gender = response.xpath('//*[@id="silderbar"]/div[last()]/ul/li[last()]/ul/a/b/text()').extract_first()
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
            elif nameSplit[0].find('外套') >= 0 or nameSplit[0].find('羽絨') >= 0 or nameSplit[0].find('夾克') >= 0 or nameSplit[0].find('大衣'):
                item['category'] = '外套'
            #內衣類
            elif nameSplit[0].find('內衣') >= 0 or nameSplit[0].find('bra') >= 0 or nameSplit[0].find('細肩帶') >= 0 or nameSplit[0].find('罩') >= 0:
                item['category'] = '內衣'
            #內褲類
            elif nameSplit[0].find('三角褲') >= 0 or nameSplit[0].find('平口褲') >= 0 or nameSplit[0].find('安全褲') >= 0 \
                    or nameSplit[0].find('生理褲') >= 0 or nameSplit[0].find('四角褲') >= 0:
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
            
            price = response.xpath('//*[contains(@class, "product_priceR_original")]/text()').extract_first()
            if price : #如果有原價的話
                #優惠價
                item['price'] = response.xpath('//*[contains(@class, "product_priceR_real")]/b/text()').extract_first()
                #原價
                price = price.split('\n')
                price = ''.join(price)
                item['store_price'] = price
            else :  #可能沒有優惠價
                #價格
                item['price'] = response.xpath('//*[contains(@class, "product_priceR_real")]/b/text()').extract_first()
           
    return item
