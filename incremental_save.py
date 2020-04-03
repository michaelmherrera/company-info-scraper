import os, json

def setup(directory_path):
    '''
    Create specified directory and initialize create json. 
    If directory already exists, attempt to recover session.

    '''
    if os.path.exists(directory_path):
        print("The path already exists. The program will start where it left off.")
        check_json(directory_path)
    else:
        os.mkdir(directory_path)
        create_json(directory_path)

def create_json(directory_path):
    info = {
        'index-last-written': -1,
        'cause-of-failue': 'unknown',
    }
    info_path = os.path.join(directory_path, "info.json")
    with open(info_path, "w+") as info_file:
        json.dump(info, info_file)

def check_json(directory_path):
    info_path = os.path.join(directory_path, "info.json")
    with open(info_path, "r") as info_file:
        info = json.load(info_file)
        print(info)
        
paths = os.listdir("incremental-saves")
for file in paths:
    os.remove(file)
os.rmdir("incremental-saves")
# setup("incremental-saves")



