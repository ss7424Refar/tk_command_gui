import os

path = os.getcwd()
print(path)
for file in os.listdir(path):
    file_location = os.path.join(path, path + '/' + file)
    print(file_location)