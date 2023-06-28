from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import ttk
import pymysql
import pickle
import shutil
import os

main = tkinter.Tk()
main.title("Tool for Easy Management of Files and Directories") 
main.maxsize(width=500 ,  height=300)
main.minsize(width=500 ,  height=300)

global login_user, login_pass, sign_user, sign_pass, contact, username, count, winsignup, winlogin, text, dirname, filecombo, accessList
count = 0
global available_files
access_count = {}

def createDirectory():
    global username, text
    global dirname
    dirname = simpledialog.askstring(title="Please enter directory name", prompt="Please enter directory name")
    if os.path.exists('files/'+username) == False:
        os.mkdir('files/'+username)
    if os.path.exists('files/'+username+"/"+dirname) == False:
        os.mkdir('files/'+username+"/"+dirname)
    text.insert(END,"Directory Created\n")

def createFile():
    global username, text
    global dirname
    dirname = simpledialog.askstring(title="Please enter directory name", prompt="Please enter directory name")
    filename = simpledialog.askstring(title="Please enter file name", prompt="Please enter file name")
    if os.path.exists('files/'+username+"/"+dirname):
        open('files/'+username+"/"+dirname+"/"+filename, 'w').close()
        text.insert(END,"File Created: "+filename)
        available_files.append('files/'+username+"/"+dirname+"/"+filename)
        filecombo['values'] = available_files
    else:
        text.insert(END,"Given path does not exists\n")
    
def deleteFile():
    global username, text
    global dirname
    dirname = filecombo.get()
    dirname = dirname.replace("\\","/")
    arr = dirname.split("/")
    usernames = arr[1]
    dirname = arr[2]+"/"+arr[3]
    if os.path.exists('files/'+username+"/"+dirname):
        if os.path.isdir('files/'+username+"/"+dirname):
            shutil.rmtree('files/'+username+"/"+dirname)
        if os.path.isfile('files/'+username+"/"+dirname):
            os.remove('files/'+username+"/"+dirname)
        text.insert(END,"Given file deleted\n")
        available_files.remove(filecombo.get())
        filecombo['values'] = available_files
    else:
        text.insert(END,"file does not exists\n")
       
def writeFile():
    global username, text
    global dirname
    dirname = filecombo.get()
    dirname = dirname.replace("\\","/")
    arr = dirname.split("/")
    current_name = arr[1]
    dirname = arr[2]
    filename = arr[3]
    filetext = simpledialog.askstring(title="Please enter file content", prompt="Please enter file content")
    if os.path.exists('files/'+username+"/"+dirname+"/"+filename):
        f = open('files/'+username+"/"+dirname+"/"+filename, "a")
        f.write(filetext+"\n")
        f.close()
        text.insert(END,"file data saved at server\n")
    else:
        text.insert(END,"file does not exists\n")                
   
def readFile():
    global username, text
    global dirname
    text.delete('1.0', END)
    dirname = filecombo.get()
    dirname = dirname.replace("\\","/")
    arr = dirname.split("/")
    usernames = arr[1]
    dirname = arr[2]
    filename = arr[3]
    if os.path.exists('files/'+username+"/"+dirname+"/"+filename):
        with open('files/'+username+"/"+dirname+"/"+filename) as f:
            data = f.read()
        f.close()
        text.insert(END,"File Content Showing in Below lines\n\n")
        text.insert(END,data)
        if filename in access_count.keys():
            access_count[filename] = access_count.get(filename) + 1
        else:
            access_count[filename] = 1
    else:
        text.insert(END,"files does not exists\n")        
    

def renameFile():
    global username, text
    global dirname
    dirname = filecombo.get()
    dirname = dirname.replace("\\","/")
    arr = dirname.split("/")
    usernames = arr[1]
    dirname = arr[2]
    oldname = arr[3]    
    newname = simpledialog.askstring(title="Please enter new file name", prompt="Please enter new file name")
    if os.path.exists('files/'+username+"/"+dirname+"/"+oldname):
        os.rename('files/'+username+"/"+dirname+"/"+oldname,'files/'+username+"/"+dirname+"/"+newname)
        text.insert(END,"file rename successfully\n")
    else:
        text.insert(END,"file does not exists\n")
    available_files.append('files/'+username+"/"+dirname+"/"+newname)
    for i in range(len(available_files)):
        ff = available_files[i]
        if os.path.basename(ff) == oldname:
            available_files.remove(ff)
            break
    filecombo['values'] = available_files
    text.insert(END,"File renamed successfully\n")

def accessCount():
    text.delete('1.0', END)
    for name,count in access_count.items():
        text.insert(END,"File Name = "+name+" Access Count = "+str(count)+"\n")
        

def fileSystem():
    global username, text, available_files, filecombo, accessList
    fs = tkinter.Tk()
    fs.title("Tool for Easy Management of Files and Directories")
    fs.maxsize(width=1300 ,  height=900)
    fs.minsize(width=1300 ,  height=900)
    font1 = ('times', 13, 'bold')

    cdButton = Button(fs, text="Create Directory", command=createDirectory)
    cdButton.place(x=50,y=100)
    cdButton.config(font=font1)

    cfButton = Button(fs, text="Create File", command=createFile)
    cfButton.place(x=300,y=100)
    cfButton.config(font=font1)

    filecombo = ttk.Combobox(fs,values=available_files,postcommand=lambda: filecombo.configure(values=available_files))
    filecombo.place(x=50,y=150)
    if len(available_files) > 0:
        filecombo.current(0)
    filecombo.config(font=font1)

    dfButton = Button(fs, text="Delete File", command=deleteFile)
    dfButton.place(x=300,y=150)
    dfButton.config(font=font1)

    rfButton = Button(fs, text="Read File", command=readFile)
    rfButton.place(x=50,y=200)
    rfButton.config(font=font1)

    wfButton = Button(fs, text="Write File", command=writeFile)
    wfButton.place(x=300,y=200)
    wfButton.config(font=font1)

    renButton = Button(fs, text="Rename File", command=renameFile)
    renButton.place(x=50,y=250)
    renButton.config(font=font1)

    renButton = Button(fs, text="Get File Access Count", command=accessCount)
    renButton.place(x=300,y=250)
    renButton.config(font=font1) 

    text=Text(fs,height=15,width=120)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=10,y=300)
    text.config(font=font1)

    fs.config(bg='chocolate1')
    fs.mainloop()

def readFiles():
    global username, available_files
    if len(available_files) > 0:
        available_files.clear()
    available_files.append("Available Files")
    for root, dirs, directory in os.walk('files/'+username):
        for j in range(len(directory)):
            available_files.append(root+"/"+directory[j])


def validateLogin():
    global login_user, login_pass, username, available_files
    available_files = []
    usr = login_user.get()
    password = login_pass.get()

    output = "none"
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'distributed',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select username, password FROM register")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == usr and row[1] == password:
                output = "success"
                username = usr
                readFiles()
                break
    if output == "success":
        winlogin.destroy()
        fileSystem()
    else:
        messagebox.showinfo("Login Failed. Please Retry")
                

def signupAction():
    global sign_user, sign_pass, contact, username, count, winsignup
    usr = sign_user.get()
    password = sign_pass.get()
    contactno = contact.get()

    output = "none"
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'distributed',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select username FROM register")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == usr:
                output = username+" Username already exists"
                break                
        if output == "none":
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'distributed',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact) VALUES('"+usr+"','"+password+"','"+contactno+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. You can login now"
                count = 2
                messagebox.showinfo(output,output)
                winsignup.destroy()
                loginFunction()
        else:
            messagebox.showinfo(output,output)

    
def loginFunction():
    global login_user, login_pass, count, winlogin
    if count == 0:
        main.destroy()
        count = 1
    winlogin = tkinter.Tk()
    winlogin.title("User Login Screen")
    winlogin.maxsize(width=500 ,  height=300)
    winlogin.minsize(width=500 ,  height=300)
	
    l1 = Label(winlogin, text='Login Screen')
    l1.config(font=font1)
    l1.place(x=140,y=30)

    l2 = Label(winlogin, text='Username')
    l2.config(font=font1)
    l2.place(x=50,y=80)

    login_user = Entry(winlogin,width=35)
    login_user.config(font=font1)
    login_user.place(x=150,y=80)

    l3 = Label(winlogin, text='Password')
    l3.config(font=font1)
    l3.place(x=50,y=130)

    login_pass = Entry(winlogin,width=35, show="*")
    login_pass.config(font=font1)
    login_pass.place(x=150,y=130)

    login1Button = Button(winlogin, text="Submit", command=validateLogin)
    login1Button.place(x=100,y=180)
    login1Button.config(font=font1)

    winlogin.mainloop()

def signupFunction():
    main.destroy()
    global sign_user, sign_pass, contact, winsignup
    winsignup = tkinter.Tk()
    winsignup.title("New User Signup Screen")
    winsignup.maxsize(width=500 ,  height=400)
    winsignup.minsize(width=500 ,  height=400)
	
    l1 = Label(winsignup, text='New User Signup Screen')
    l1.config(font=font1)
    l1.place(x=140,y=30)

    l2 = Label(winsignup, text='Username')
    l2.config(font=font1)
    l2.place(x=50,y=80)

    sign_user = Entry(winsignup,width=35)
    sign_user.config(font=font1)
    sign_user.place(x=150,y=80)

    l3 = Label(winsignup, text='Password')
    l3.config(font=font1)
    l3.place(x=50,y=130)

    sign_pass = Entry(winsignup,width=35, show="*")
    sign_pass.config(font=font1)
    sign_pass.place(x=150,y=130)

    l4 = Label(winsignup, text='Contact No')
    l4.config(font=font1)
    l4.place(x=50,y=180)

    contact = Entry(winsignup,width=25)
    contact.config(font=font1)
    contact.place(x=150,y=180)

    sign1Button = Button(winsignup, text="Submit", command=signupAction)
    sign1Button.place(x=100,y=230)
    sign1Button.config(font=font1)

    winsignup.mainloop()

def closeFunction():
    main.destroy()


font = ('times', 16, 'bold')
title = Label(main, text='',anchor='w')
title.config(bg='darkviolet', fg='gold')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')

loginButton = Button(main, text="Login Here", command=loginFunction)
loginButton.place(x=100,y=100)
loginButton.config(font=font1)

loginButton = Button(main, text="New User Signup Here", command=signupFunction)
loginButton.place(x=100,y=150)
loginButton.config(font=font1)

exitButton = Button(main, text="Exit", command=closeFunction)
exitButton.place(x=100,y=200)
exitButton.config(font=font1)

main.config(bg='turquoise')
main.mainloop()


