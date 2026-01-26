# открыть файл для чтения
file = open(file = 'My_file.txt',mode = 'r',encoding='utf-8')
text = file.read()
text_str = file.read()
print(text)
print(text_str)


output_file = open(file = 'My_file_2.txt',mode = 'w',encoding='utf-8')
text_to_write = "hello world"
output_file.write(text_to_write)
file.close()