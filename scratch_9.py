
file_obj = open('new.txt', mode='w')
file_obj.write('Rebecca')
file_obj.close()

with open("new_1.txt", mode='w') as file_obj:
    file_obj.write('Rebecca')

