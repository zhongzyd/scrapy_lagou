# -*- coding: utf-8 -*-
import json
import pandas

data_file = open('lagou_products.txt', 'r')

data = []

line = data_file.readline().strip()
while line:
    data.append(json.loads(line))
    line = data_file.readline().strip()
    
data = pandas.DataFrame(data)

data_file.close()