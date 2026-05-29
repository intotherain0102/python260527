# 정규표현식.py

import re

result = re.search("[0-9]*th", "  35th")
print(result)
print(result.group())

# result = re.match("[0-9]*th", "  35th")
# print(result)
# print(result.group())

result = re.search("\d{4}", "올해는 2026년 입니다.")
print(result.group())

result = re.search("\d{5}", "우리 동네는 52100 입니다.")
print(result.group())

result = re.search("apple", "this is an apple")
print(result.group())

result = re.search("apple", "this is an Apple".lower())
print(result.group())
