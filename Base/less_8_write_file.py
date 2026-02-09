import json


# with open('new_file', 'w',encoding='utf-8') as f:
#     for i in range(3):
#         line = input('Введите текст:\n')
#         f.write(line+ '\n')
# print('файл закрыт')
# with open('new_file', 'a',encoding='utf-8') as f:
#     print('файл открыт')
#     for i in range(3):
#         line = input('Введите текст:\n')
#         f.write(line+ '\n')
#
# with open('new_file', 'r',encoding='utf-8') as f:
#     text = f.read()
#     text_lines = text.split('\n')
#     for :
#         if i % 2 == 0:
#             text_lines.remove(text_lines[i])
#
# with open('new_file', 'w',encoding='utf-8') as f:
#    for line in text_lines:
#        f.write(line+ '\n')

person = {
    'name': 'саша',
    'age': 22,
    'phone': '14353637383',
    'email':['admin.com',
             'alex@mail.'],
    'address':{
        'city':'Новгород'
    }
}

# json_str  = json.dumps(person,ensure_ascii=False,indent=4)
with open('person.json', 'w', encoding='utf-8') as f:
    json.dump(person,f,ensure_ascii=False,indent=4)

with open('person.json', 'r', encoding='utf-8') as f:
    person = json.load(f)
    print(person)