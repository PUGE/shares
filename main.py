#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import re
import os
import json
import requests
import time


# 今天日期
date = time.strftime('%Y.%m.%d',time.localtime(time.time()))

# 判断是否已经获取到了当天的数据
if not os.path.exists('./history/' + date + '.csv'):
  # 读取上证指数列表
  szListFile = open('sz.json', 'r', encoding='utf-8').read()
  szList = json.loads(szListFile)
  print("等待获取条数:" + str(len(szList)))
  summary = '股票名字,代码,当前价格,昨日收盘价,今日开盘价,成交的股票数,外盘,内盘,买一报价,买一数量,买二报价,买二数量,买三报价,买三数量,买四报价,买四数量,买五报价,买五数量,卖一报价,卖一数量,卖二报价,卖二数量,卖三报价,卖三数量,卖四报价,卖四数量,卖五报价,卖五数量,最近逐笔成交,时间,涨跌,涨跌%,今日最高价,今日最低价,价格/成交量(手)/成交额,成交量(手),成交金额,换手率(%),市盈率,最高,最低,振幅(%),流通市值(亿),总市值(亿),市净率,涨停价,跌停价,量比,委差,平均成本,PE(动)\n'
  
  # 每50个提交一次
  tempList = []
  def getData ():
    listString = ','.join(tempList)
    data = requests.get(url='http://qt.gtimg.cn/q=' + listString).text
    sharesList = re.findall(r"=\"1\~(.+?)\";", data)

    # 去掉空数据
    for sz in sharesList:
      global summary
      sz = sz.replace("~~", "~")
      summary += sz.replace("~",",") + '\n'

  for sz in szList:
    if len(tempList) >= 50:
      getData()
      tempList = []
    tempList.append(sz['id'])

  getData()

  file_path = './history/' + date + '.csv'
  with open(file_path, mode='w', encoding='utf_8_sig') as file_obj:
    file_obj.write(summary)

# 跌了的列表
lostList = []
# 涨了的列表
winList = []
# 没有涨没有跌的
flatList = []
# 总交易价格
allTraAmount = 0

# 读取上证数据
firstFloor = open('./history/' + date + '.csv', 'r', encoding='utf_8_sig').read().split('\n')
# 清洗数据
secondFloor = []

index = 0
for temp in firstFloor:
  # 过滤掉空数据 并且过滤掉表头
  if (temp != "" and index != 0):
    secondFloor.append(temp.split(','))
  index += 1

print("数据总条数: " + str(len(secondFloor)))

for player in secondFloor:
  win = float(player[30])
  if win > 0:
    winList.append(player)
  elif win == 0:
    flatList.append(player)
  else:
    lostList.append(player)
  # 增加价格
  # allTraAmount += player['traPri']

print('今日: [%s] 只股票赢了 [%s] 只股票输了 [%s] 只股票在观望!' % (str(len(winList)), str(len(lostList)), str(len(flatList))))
# print('成交金额 [%s], 平均成交金额 [%s]' % (str(allTraAmount), str(allTraAmount / len(todayData))))