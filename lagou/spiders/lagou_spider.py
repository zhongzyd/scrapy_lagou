# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from lagou.items import LagouItem
import scrapy
import re
import json
import urllib

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')


kd_list = ['数据分析','数据挖掘','机器学习'] 
 
city_list = ['北京','上海','深圳','广州','杭州','成都','南京','武汉','西安','厦门','长沙', \
        '苏州','天津','重庆','郑州','青岛','合肥','福州','济南','大连','珠海','无锡', \
        '佛山','东莞','宁波','常州','沈阳','石家庄','昆明','南昌','南宁','哈尔滨',  \
        '海口','中山','惠州','贵阳','长春','太原','嘉兴','泰安','昆山','烟台','兰州', \
        '泉州']
        
gj_list = ['不限','应届毕业生','1年以下','1-3年','3-5年','5-10年','10年以上']

xl_list = ['不限','大专','本科','硕士','博士']

jd_list = ['初创型','成长型','成熟型','已上市']

hy_list = ['移动互联网','电子商务','金融','企业服务','教育','文化娱乐','游戏','O2O', \
      '硬件','社交网络','旅游','医疗健康','生活服务','信息安全','数据服务','广告营销',  \
      '分类信息','招聘','其他']

base_url = 'http://www.lagou.com/jobs/positionAjax.json?'
urls = []
for kd in kd_list:
    for city in city_list:
        for gj in gj_list:
            for xl in xl_list:
                for jd in jd_list:
                    for hy in hy_list:
                        urls.append(base_url + 
                                    'kd=' + kd + 
                                    '&city=' + city +
                                    '&gj=' + gj +
                                    '&xl=' + xl +
                                    '&jd=' + jd +
                                    '&hy=' + hy +
                                    '&pn=1')

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_urls = urls
    
    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        url_split = re.split('kd=',response.url)
        kd = re.split('&',url_split[1])[0]
        kd = urllib.unquote(kd)
        
        for job in data['content']['result']:
            companyLabelList = '|'
            for label in job['companyLabelList']:
                companyLabelList = companyLabelList + label + '|'
            job['companyLabelList'] = companyLabelList
            job[u'kd'] = kd
            
            item = LagouItem()
            item['job_inf'] = job
            
            yield item
        
        url_split = re.split('pn=',response.url)
        pn = int(url_split[1])
        
        if pn == 1:
            totalPageCount = data['content']['totalPageCount']
            while pn < totalPageCount:
                pn = pn + 1
                next_url = url_split[0] + 'pn=' + str(pn)
                yield scrapy.Request(next_url, callback=self.parse)
                