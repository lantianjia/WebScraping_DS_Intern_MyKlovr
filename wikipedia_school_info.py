# coding:utf-8
from bs4 import BeautifulSoup
import requests
import xlwt
import pandas as pd


workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('data')

worksheet.write(0, 0, 'arcoName')
worksheet.write(0, 1, 'url')
worksheet.write(0, 2, 'scid')
worksheet.write(0, 3, 'Summary')
worksheet.write(0, 4, 'infobox_start_position')

csv_data = pd.read_csv('url.csv')
length = len(csv_data)


def parse0(url):
    r = requests.get(url)
    # 请求首页后获取整个html界面
    blog = r.content
    # 用html.parser解析html
    soup = BeautifulSoup(blog, "html.parser")
    # find方法查找页面上第一个属性匹配的tag对象
    tag_soup = soup.find(class_="infobox vcard")

    if tag_soup == None:
        return
    elif len(tag_soup.contents) > 0:
        if tag_soup.contents[0] == None:
            return
        else:
            tag_soup2 = len(tag_soup.contents[0].contents)
    else:
        pass

    a = []
    b = []
    content = []

    for j in range(tag_soup2):
        if tag_soup.contents[0].contents[j].contents == None:
            pass
        elif len(tag_soup.contents[0].contents[j].contents)>0:
            a.append(tag_soup.contents[0].contents[j].contents[0].text)

        if tag_soup.contents[0].contents[j].contents == None:
            pass
        elif len(tag_soup.contents[0].contents[j].contents) >1:
            b.append(tag_soup.contents[0].contents[j].contents[1].text)

    for i in a:
        if i == '':
            a.remove(i)

    k = len(a) - len(b)
    m = len(b)
    if len(a) == len(b):
        for i in range(len(a)):
            content.append(a[i])
            content.append(b[i])
    else:
        for i in range(k):
            content.append(a[i])
        for i in range(len(a) - k):
            content.append(a[i+k])
            content.append(b[i])
    return content,k,m



def parse1(url):
    r = requests.get(url)
    # 请求首页后获取整个html界面
    blog = r.content
    # 用html.parser解析html
    soup = BeautifulSoup(blog, "html.parser")
    # find方法查找页面上第一个属性匹配的tag对象
    tag_soup = soup.find(class_="infobox vcard")

    if tag_soup == None:
        return
    else:
        tag_soup1 = len(tag_soup.contents)
    if len(tag_soup.contents) > 1:
        if tag_soup.contents[1] == None:
            return
        else:
            tag_soup2 = len(tag_soup.contents[1].contents)
    else:
        pass

    a = []
    b = []
    content = []

    for i in range(1,tag_soup1):
        for j in range(tag_soup2):
            if tag_soup.contents[1].contents[j].contents == None:
                pass
            elif len(tag_soup.contents[1].contents[j].contents)>0:
                a.append(tag_soup.contents[1].contents[j].contents[0].text)

            if tag_soup.contents[1].contents[j].contents == None:
                pass
            elif len(tag_soup.contents[1].contents[j].contents) >1:
                b.append(tag_soup.contents[1].contents[j].contents[1].text)

    for i in a:
        if i == '':
            a.remove(i)
    k = len(a) - len(b)
    m = len(b)

    if len(a) == len(b):
        for i in range(len(a)):
            content.append(a[i])
            content.append(b[i])
    else:
        for i in range(k):
            content.append(a[i])
        for i in range(len(a) - k):
            content.append(a[i+k])
            content.append(b[i])

    return content,k,m

#test
# url = 'https://en.wikipedia.org//wiki/Cazenovia_College'
# if parse1(url) == None:
#     pass
# else:
#     content,k,m= parse1(url)
#     if len(content) == 0:
#         content, k, m = parse0(url)
# print(content)


for i in range(length):
    url = csv_data.loc[i, 'href']
    arcoName = csv_data.loc[i, 'arcoName']
    scid = csv_data.loc[i,'scid']
    Summary = csv_data.loc[i,'Summary']
    print(i)
    print(url)

    worksheet.write(i+1, 0, arcoName)
    worksheet.write(i+1, 1, url)
    worksheet.write(i+1, 2, scid)
    worksheet.write(i+1, 3, Summary)

    if parse1(url) == None:
        pass
    else:
        content, k, m = parse1(url)
        if len(content) == 0:
            content, k, m = parse0(url)

        for t in range(m):
            worksheet.write(i+1,4+2*t,content[k+2*t])
            worksheet.write(i+1,4+2*t+1,content[k+2*t+1])
        for s in range(k):
            worksheet.write(i+1, 2*m + s + 4,content[s])
    workbook.save('resultss.xls')





