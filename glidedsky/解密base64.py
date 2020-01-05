# -*- coding: utf-8 -*- 
# @Time : 2019/12/29 3:17 
# @Author : lattesea 
# @File : 解密base64.py
import base64
from fontTools.ttLib import TTFont
import re

font_base64 = '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'
b = base64.b64decode(font_base64)
with open('font_online.ttf', 'wb') as f:
    f.write(b)
online_font = TTFont('font_online.ttf')
online_font.saveXML('online.xml')
true_dict = {}  # 正确的映射字典
index = 0
base_uni_list = online_font.getGlyphOrder()[1:]
for i in base_uni_list:
    true_dict[i] = index
    index += 1
print(true_dict)
# false_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
#               'seven': 7, 'eight': 8, 'nine': 9, 'zero': 0}
false_dict = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
              '9': 'nine', '0': 'zero'}
# html = etree.HTML(response)
# false_number = html.xpath("//div[@class='col-md-1']/text()")
false_number = ['154', '458']
# false_number = list(map(lambda item: re.sub('\s+', '', item), false_number))
# false_number = list(filter(None, false_number))

# result = list(map(lambda item: list(item), false_number))
# print(result)
middle_list1 = []
middle_list2 = []
middle_list3 = []
true_list = []
for i in false_number:
    for j in i:
        middle = j.replace(j, false_dict[j])
        middle_list1.append(middle)
    middle_list2.append(middle_list1.copy())
    middle_list1.clear()
for i in middle_list2:
    for j in i:
        middle = j.replace(j, str(true_dict[j]))
        middle_list1.append(middle)
    middle_list3.append(middle_list1.copy())
    middle_list1.clear()
for i in middle_list3:
    s = "".join(i)
    true_list.append(int(s))

print(middle_list2)
print(middle_list3)
print(true_list)
