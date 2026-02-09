import json
# user = {
#     "id": 0,
#     "name": "Анна",
#     "age": 28,
#     "city": "Москва",
#     "is_active": True
# }

# with open('json.txt','w',encoding='utf-8') as f:
#     json.dump(user,f,ensure_ascii=False,indent=4)

# try:
#     with open ('unknown.json','r',encoding='utf-8') as f:
#         data = json.load(f)
# except:
#     print('Файл не найден')

# print('hello world')
import requests
response = requests.get('https://www.geeksforgeeks.org/git/github-rest-api/')

print(response.status_code)
print(response.ok)
print(response.reason)






    