#######  Made by Nam Nguyen, September 3, 2017  ######

import os
import sys
from tkinter import *
from os import listdir
from os.path import isfile, join
headline = ("Nếu không đọc được Tiếng Việt thì không biết dùng đâu!")

make_folder_head = "Tạo nhiều thư mục cùng lúc trong một đường dẫn"
alter_extension_head = "Thay đổi đuôi của tất cả các file có đuôi chỉ định trong 1 thư mục"
alter_links_head = "Biến đổi link ảnh từ dạng gốc sang HTML, hoặc ngược lại"
make_folder_fields = ["Đường dẫn thư mục", "Số chap khởi điểm", "Số chap kết thúc", "Phần đầu (optional)", "Phần cuối (optional)"]
alter_extension_fields = ["Đường dẫn thư mục", "Đuôi file cần đổi", "Đổi thành đuôi"]
alter_links_fields = ["Đường dẫn file chứa links"]



def add_folders(entries):
    if (entries[0][1].get()=="" or entries[1][1].get()=="" or entries[2][1].get()==""):
        pop_up("Không được bỏ trống 3 mục đầu")
        return
    path=entries[0][1].get()
    start=entries[1][1].get()
    end=entries[2][1].get()
    
    if (entries[3][1].get()==""):
        prefix="Chap "
    else:
        prefix=entries[3][1].get()
        
    if (entries[4][1].get()==""):
        suffix=""
    else:
        suffix=entries[4][1].get()
        
    try:
        dest=r'%s' %(path)
        dir = os.path.dirname(dest)
        if not os.path.exists(dir):
            pop_up("Đường dẫn tạo thư mục không tồn tại… Hãy kiểm tra lại đường dẫn...")
            return
        start=int(start)
        end=int(end)+1
        for i in range(start,end):            
            path_name = dest + '\\' +str(prefix)+str(i)+str(suffix)
            dir = os.path.dirname(path_name)
            if not os.path.exists(path_name):
                os.makedirs(path_name)
        pop_up("Thêm thư mục thành công!")
    except:
        pop_up("Đã xảy ra lỗi... Hãy kiểm tra lại các hạng mục...")
   

    
def change_extension(e):
    try:
        if (e[0][1].get()=="" or e[1][1].get()=="" or e[2][1].get()==""):
            pop_up("Không được để trống 3 mục này")
            return
        path = e[0][1].get()
        old_extension = e[1][1].get()
        new_extension = e[2][1].get()
        files=[]
        for f in listdir(path):
            if (isfile(join(path, f)) and f.endswith('.'+old_extension)):
                files.append(join(path, f))
        for f in files:
            base = os.path.splitext(f)[0]
            os.rename(f,base+'.'+new_extension)
        #files = [f for f in listdir(path) if isfile(join(path, f))]
        pop_up("Thay đổi thành công!")
    except:
        pop_up("Đã xảy ra lỗi...")

def add_prefix(e):
    try:
        if (e[0][1].get()==""):
            pop_up("Cần có file text mới chạy được")
            return
        file= open(e[0][1].get(),"r+")
        links=[]
        for line in file:
            link = "<img src=\"" + line.strip() + "\" />\n"
            links.append(link)
        file.seek(0)
        file.truncate()
        for l in links:
            file.write(l)
        file.close()
        pop_up("Thay đổi thành công!")
    except:
        pop_up("Đã xảy ra lỗi...")

def remove_prefix(e):
    try:
        if (e[0][1].get()==""):
            pop_up("Cần có file text mới chạy được")
            return
        file= open(e[0][1].get(),"r+")
        links=[]
        for line in file:
            link = line.strip()
            for i in range(0,len(link)):
                if (link[i:i+3]=="src"):
                    link = link[i:]
                    
                    first= link.find('\"')+1
                    second= link[first+1:].find('\"') + first+1
                    link = link[first:second]
                    link = link + "\n"
                    break
            links.append(link)
        file.seek(0)
        file.truncate()
        for l in links:
            file.write(l)
        file.close()
        pop_up("Thay đổi thành công!")
    except:
        pop_up("Đã xảy ra lỗi...")
    
def pop_up(text):
    window=Tk()
    window.title("Thông báo")
    window.geometry("250x150")
    row = Frame(window)
    
    lab=Label(row,wraplengt=150,text=text)
    row.pack(side=TOP,fill=X,padx=10,pady=10)
    lab.pack()
    b1 = Button(window, text='Đóng', command=window.destroy)
    b1.pack(padx=30,pady=10)
    root.mainloop()

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

if __name__ == "__main__":    
    root=Tk()
    root.title("Chương trình đa dụng")
    root.geometry("450x520")
##    row = Frame(root)
##    row.pack(side=TOP, fill=X, padx=15, pady=5)

    lab1 = Label(root, width=200, anchor='w', text=headline, wraplengt=400,font=(100) )
    lab1.pack()

    
    ##Make folder##
    make_folder_lab = Label(root, width=200, anchor='w', text=make_folder_head, wraplengt=400,fg='red')
    make_folder_lab.pack()
    make_folder_entries = makeform(root, make_folder_fields)
##    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    make_folder_button = Button(root, text='Tạo thư mục',command=(lambda e=make_folder_entries: add_folders(e)))
    make_folder_button.pack(padx=25, pady=10)
    
    ##Alter extension##
    alter_extension_lab = Label(root, width=200, anchor='w', text=alter_extension_head, wraplengt=400,fg='red')
    alter_extension_lab.pack()
    alter_extension_entries = makeform(root,alter_extension_fields)
    alter_extension_button = Button(root, text='Đổi file extension',command=(lambda e=alter_extension_entries: change_extension(e)))
    alter_extension_button.pack(padx=25, pady=10)

    ##Alter link HTML##
    alter_links_lab = Label(root, width=200, anchor='w', text=alter_links_head, wraplengt=400,fg='red')
    alter_links_lab.pack()
    alter_links_entries = makeform(root,alter_links_fields)
    alter_links_button1 = Button(root, text='Biến links thành HTML',command=(lambda e=alter_links_entries: add_prefix(e)))
    alter_links_button1.pack(padx=25, pady=10,side=LEFT)
    alter_links_button2 = Button(root, text='Biến HTML thành links',command=(lambda e=alter_links_entries: remove_prefix(e)))
    alter_links_button2.pack(padx=25, pady=10,side=LEFT)
    root.mainloop()
