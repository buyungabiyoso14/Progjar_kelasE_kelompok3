import Tkinter
from Tkinter import *
import tkMessageBox

import socket
import sys
from thread import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('10.151.36.250', 10010)

sock.connect(server_address)
flag = 0

def receive_chatp(text1):
    while True:
        status=sock.recv(1024)
        temp = status.split()
        i = 2
        message = []
        message.append(temp[1] + ":")
        while i != len(temp):
            message.append(temp[i])
            i += 1
        message.append("\n")
        strings = " ".join(message)
        print strings
        text1.insert(END, strings)
		
def receive_chatg(text1):
    while True:
        status = sock.recv(1024)
        print status
        temp = status.split()
        i = 3
        message = []
        message.append(temp[1] + ": " + temp[2] + ": ")
        while i != len(temp):
            message.append(temp[i])
            i += 1
        strings = " ".join(message)
        print strings
        text1.insert(END, strings)

def receive_listg(text1):
    sock.sendall("TGRUP")
    while True:
        status=sock.recv(1024)
        temp = status.split()
        i = 0
        while i != len(temp) - 1:
            text1.insert(END, temp[i] + "\n")
            i += 1
    	
def receive_pesan(text1):
    sock.sendall("apesan")
    while True:
        status=sock.recv(1024)
        temp = status.split()
        i = 0
        while i != len(temp) - 1:
            text1.insert(END, temp[i] + "\r")
            i += 1

def return_server():
    while True:
		status = sock.recv(1024)
		if status == "8:Daftar Berhasil.":
			tkMessageBox.showinfo("Sukses!","Pendaftaran Sukses!")
		elif status == "17:Keluar Grup Gagal.":
			tkMessageBox.showinfo("Gagal!", "Keluar Grup Gagal!")
		elif status == "9:Daftar Gagal.":
			tkMessageBox.showinfo("Gagal!", "Pendaftaran Gagal!")
		elif status == "1:Login Berhasil.":
			response = tkMessageBox.showinfo("Sukses!", "Login Sukses")
			if response == "ok":
				mainWindow()
		elif status == "2:Login Gagal.":
			tkMessageBox.showinfo("Gagal!", "Login Gagal!")
		elif status == "13:Buat Grup Sukses.":
			tkMessageBox.showinfo("Sukses!", "Buat Grup Sukses!")
		elif status == "14:Buat Grup Gagal.":
			tkMessageBox.showinfo("Gagal!", "Buat Grup Gagal!")
		elif status == "12:Gabung Grup Berhasil.":
			tkMessageBox.showinfo("Sukses!", "Gabung Grup Berhasil!")
		elif status == "15:Gabung Grup Gagal.":
			tkMessageBox.showinfo("Gagal!", "Gabung Grup Gagal!")
		elif status == "16:Keluar Grup Berhasil.":
			tkMessageBox.showinfo("Sukses!", "Keluar Grup Berhasil!")
        
			
def terima_list_grup_member(text1):
    while True:
        status = sock.recv(1024)
        temp = status.split()
        i = 0
        while i != len(temp) - 1:
            text1.insert(END, temp[i] + "\n")
            i += 1


def personalWindowHandler(entry1, entry2,text1):
    recipient = entry1.get()
    message = entry2.get()
    text1.insert(END,"You -> "+recipient+" : "+message+"\n")
    sock.sendall("KIRIM_PRIVATE " + recipient + " " + message)

def groupListWindow():
    top = Tkinter.Tk()
    top.title("Group List")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    start_new_thread(receive_pesan, (W1,))
    top.mainloop()
	
def ambilpesan():
    top = Tkinter.Tk()
    top.title("ambil pesan")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    start_new_thread(receive_listg, (W1,))
    top.mainloop()
def groupMessageWindowHandler(entry1,entry2,text1):
    grup = entry1.get()
    message = entry2.get()
    text1.insert(END, "You -> " + grup + " : " + message + "\n")
    sock.sendall("KIRIM_GRUP " + message)
def groupMessageWindow():
    top = Tkinter.Tk()
    top.title("Grup Chat")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    frame3 = Frame(top)
    frame3.pack()
    L1 = Label(frame1, text="Grup")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Pesan")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5)
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Kirim", command=lambda: groupMessageWindowHandler(E1, E2,W1))
    Z.pack()
    start_new_thread(receive_chatg,(W1,))
    top.mainloop()
def personalWindow():
    top = Tkinter.Tk()
    top.title("Private Chat")
    frame0 = Frame(top)
    frame0.pack()
    W1 = Text(frame0)
    W1.pack()
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    frame3 = Frame(top)
    frame3.pack()
    L1 = Label(frame1, text="Penerima")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Pesan")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5)
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Kirim", command=lambda: personalWindowHandler(E1, E2,W1))
    Z.pack()
	w = Button(frame3, text="ambil pesan", command=ambilpesan)
    w.pack()
    start_new_thread(receive_chatp,(W1,))
    top.mainloop()
def createWindowHandler(entry1,entry2):
    groupname = entry1.get()
    password = entry2.get()
    sock.sendall("BGRUP " + groupname + " " + password)

def joinWindowHandler(entry1,entry2):
    groupname = entry1.get()
    password = entry2.get()
    sock.sendall("GGRUP " + groupname + " " + password)
def keluargWindowHandler(entry1):
    groupname = entry1.get()
    sock.sendall("KGRUP " + groupname)

def hapusgWindowHandler(entry1,entry2):
    groupname = entry1.get()
    password = entry2.get()
    sock.sendall("HGRUP " + groupname + " " + password)
	
def createWindow():
    top1 = Tkinter.Tk()
    top1.title("Buat Grup")
    L0 = Label(top1, text="Buat Grup\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Nama Grup (alphanumeric)")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password (alphanumeric)")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5, show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Create Group!", command=lambda: createWindowHandler(E1, E2))
    Z.pack()
    top1.mainloop()
	
def keluargWindow():
    top1 = Tkinter.Tk()
    top1.title("keluar grup")
    L0 = Label(top1, text="keluar dari grup\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Nama Grup")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    Z = Button(frame3, text="keluar grup!", command=lambda: keluargWindowHandler(E1))
    Z.pack()
    top1.mainloop()

def hapusgWindow():
    top1 = Tkinter.Tk()
    top1.title("hapus grup")
    L0 = Label(top1, text="hapus grup\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Nama Grup (alphanumeric)")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password (alphanumeric)")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5, show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="hapus grup!", command=lambda: hapusgWindowHandler(E1, E2))
    Z.pack()
    top1.mainloop()
	
def joinWindow():
    top1 = Tkinter.Tk()
    top1.title("Join Group")
    L0 = Label(top1, text="Join A Group\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="Group Name")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password")
    L2.pack(side=LEFT)
    E2 = Entry(frame2, bd=5, show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Join Group!", command=lambda: joinWindowHandler(E1, E2))
    Z.pack()
    top1.mainloop()

    

def logoutHandler(top):
    sock.sendall("LOGOUT")
    response = tkMessageBox.showinfo("Success!", "Logout success")
    if response == "ok":
        global flag
        flag.destroy()

def groupWindow():
	top = Tkinter.Tk()
	top.title("Grup Chat")
	frame1 = Frame(top)
	frame1.pack()
	frame2 = Frame(top)
	frame2.pack()
	A = Button(frame1,text="buat grup", command=createWindow)
    	A.pack()
	B = Button(frame1,text="gabung grup", command=joinWindow)
    	B.pack()
	C = Button(frame1,text="daftar grup", command=groupListWindow)
    	C.pack()
	D = Button(frame1,text="keluar grup", command=keluargWindow)
    	D.pack()
	E = Button(frame1,text="kirim pesan ke grup", command=groupMessageWindow)
    	E.pack()
	F = Button(frame1,text="hapus grup", command=hapusgWindow)
    	F.pack()
	start_new_thread(return_server, ())
	top.mainloop()

def mainWindow():
    top = Tkinter.Tk()
    top.title("Home")
    A = Button(top,text="Private Chat", command=personalWindow)
    A.pack()
    B = Button(top, text="Grup Chat", command=groupWindow)
    B.pack()
    C = Button(top, text="Logout", command=lambda: logoutHandler(top))
    C.pack()
    top.mainloop()

def signupWindowHandler(entry1,entry2):
    username =  entry1.get()
    password = entry2.get()
    sock.sendall("DAFTAR " + username + " " + password)

def firstWindowHandler(entry1,entry2):
    username = entry1.get()
    password = entry2.get()
    sock.sendall("LOGIN " + username + " " + password)
def signupWindow():
    top1 = Tkinter.Tk()
    top1.title("Sign Up")
    L0 = Label(top1, text="Sign Up\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="User Name (alphanumeric)")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password (alphanumeric)")
    L2.pack(side=LEFT)
    E2 = Entry(frame2,  bd=5,show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Sign Up!", command= lambda: signupWindowHandler(E1,E2))
    Z.pack()
    top1.mainloop()
def loginWindow():
    top1 = Tkinter.Tk()
    top1.title("Login")
    L0 = Label(top1, text="Login\n")
    L0.pack()
    frame1 = Frame(top1)
    frame1.pack()
    frame2 = Frame(top1)
    frame2.pack()
    frame3 = Frame(top1)
    frame3.pack()
    L1 = Label(frame1, text="User Name (alphanumeric)")
    L1.pack(side=LEFT)
    E1 = Entry(frame1, bd=5)
    E1.pack(side=RIGHT)
    L2 = Label(frame2, text="Password (alphanumeric)")
    L2.pack(side=LEFT)
    E2 = Entry(frame2,  bd=5,show="*")
    E2.pack(side=RIGHT)
    Z = Button(frame3, text="Login!", command= lambda: firstWindowHandler(E1,E2))
    Z.pack()
    top1.mainloop()

def firstWindow():
    top = Tkinter.Tk()
    global flag
    flag = top
    top.title("selamat datang!")
    L0 = Label(top, text="Selamat datang di chat kelompok 3!\n")
    L0.pack()
    frame1 = Frame(top)
    frame1.pack()
    frame2 = Frame(top)
    frame2.pack()
    frame3 = Frame(top)
    frame3.pack()
    A = Button(frame3, text ="Log In!", command = loginWindow )
    A.pack()
    L3 = Label(frame3, text="\nAnda Belum Punya Akun?\nMau Daftar?\n")
    L3.pack()
    B = Button(frame3, text ="Sign Up", command = signupWindow)
    B.pack()
    top.mainloop()


start_new_thread(return_server,())

#nama=raw_input("Masukan nama: ");
try:
	firstWindow()
	return_server()
finally:
    sock.close()



		
		
