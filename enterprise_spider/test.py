#
# def isSimilar(a, b):
#     score = 0
#     for char in a:
#         if char in b:
#             score += 1
#     return score >= len(a) * 0.6
#
#
# print(isSimilar('腾讯科技', '腾讯科技(北京)有限公司'))

import re

print(re.search('we', 'w3wewewedfasdfsdf').span()[0])
