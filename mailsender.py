# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:02:15 2021

@author: Rochy
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 16:47:36 2021

@author: Rochy
"""

from tkinter import *
from tkinter import messagebox 
from tkinter.filedialog import askopenfilename
import smtplib
import time
import csv
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from tkinter import ttk
from ttkthemes import themed_tk as tk
#from ttkthemes import ThemedTk
from tkinter import filedialog


root=tk.ThemedTk()
root.get_themes()
root.set_theme('breeze')
root_width=450
root_height=400
root.geometry(f"{root_width}x{root_height}")
root.title('Mail Sender')
root.iconbitmap('GMail_icon.ico')
root.resizable(0,0)
root.config(bg="#EFF0F1")
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
x=(screen_width/2)-(root_width/2)
y=(screen_height/2)-(root_height/2)
root.geometry(f'{root_width}x{root_height}+{int(x)}+{int(y)}')
def close():
    root.destroy()
def select():
    global select_file
    global clicked
    new_list=[]
    try:
        select_file=filedialog.askopenfilename(initialdir="C:/",filetypes=(("csv files","*.csv"),("all files","*.*")))
        filename_label1.configure(text=select_file)
        if len(select_file)>60:
            filename_label1.configure(text=f"{select_file[0:59]}\n{select_file[60:]}")
    
        with open(select_file, 'r') as file_object:
            csv_reader=csv.reader(file_object)
            csv_headings=next(csv_reader)
            for row in csv_headings:
                new_list.append(row)
            new_list=list(filter(None, new_list))
            clicked=StringVar()
            clicked.set(new_list[0])
            drop_down_button=ttk.OptionMenu(root, clicked, *new_list)
            drop_down_button.config(width=8)
            drop_down_button.place(x=340,y=280)
    except FileNotFoundError:
        pass
    except UnboundLocalError:
        pass
    
def email():
    process=ttk.Label(root,text="",font="calibri 10")
    process.place(x=250,y=90)
    
    get=clicked.get()
    receiver_email=[]
    with open(select_file, 'r') as file_object:
        csv_dict_reader=csv.DictReader(file_object)
        next(csv_dict_reader)
        for line in csv_dict_reader:
            receiver_email.append(line[get])
    receiver_email=list(filter(None, receiver_email))
    try:
        sender_email = email_entry.get()
        sender_password= email_password_entry.get()
#        receiver_email = ''
        '''instance of MIMEMultipart'''
        message = MIMEMultipart() 
        '''string to store the body of the mail'''
        body = textbox1.get(1.0, END)
        '''attach the body with the msg instance'''
        message.attach(MIMEText(body, 'plain')) 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        s.starttls() 
        s.login(sender_email, sender_password) 
        '''Converts the Multipart msg into a string'''
        send_message = message.as_string() 
        '''sending the mail'''
        count=0
        sent=0
        for mail in receiver_email:
            if mail.endswith("@gmail.com"):
                sent=sent+1
                s.sendmail(sender_email, mail, send_message)
                process.config(text=f"Successfully sent {sent} of {len(receiver_email)}")
            else:
                count=count+1
                if count==1:
                    messagebox.showerror(f"Address Error",f"{count} Email address is incorrect")
                elif count>1:
                    messagebox.showerror(f"Address Error",f"{count} Email addresses are incorrect")
        '''terminating the session'''
        s.quit()
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Authentication Error","Logged In Failed!")
    

filename_label1=ttk.Label(root, text="")
filename_label1.place(x=20,y=50)

close_button=ttk.Button(root,text="Close",command=close)
close_button.place(x=340,y=355)

select_file_button=ttk.Button(root,text="Select A File",command=select)
select_file_button.place(x=20,y=15)

email_button=ttk.Button(root,text="Send",command=email)
email_button.place(x=20,y=355)

message_label=ttk.Label(root,text="Text Field",font="calibri 15")
message_label.place(x=20,y=80)

email_label=ttk.Label(root,text="Sender",font="calibri 13")
email_label.place(x=200,y=290)

email_password_label=ttk.Label(root,text="Password",font="calibri 13")
email_password_label.place(x=200,y=320)

email_entry=ttk.Entry(root,font="calibri 12")
email_entry.place(x=20,y=285)

email_password_entry=ttk.Entry(root,font="calibri 12",show="•")
email_password_entry.place(x=20,y=315)

textframe1=ttk.Frame(root)
scrollbar1=ttk.Scrollbar(textframe1, orient=VERTICAL)
textbox1=Text(textframe1, width=50,height=8, bg="#FAFBFC", fg="#464646", font="calibri 12", yscrollcommand=scrollbar1.set)
scrollbar1.config(command=textbox1.yview)
scrollbar1.pack(side=RIGHT, fill=Y)
textframe1.place(x=20,y=115)
textbox1.pack()

root.mainloop()
