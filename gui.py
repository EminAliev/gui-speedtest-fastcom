import threading
import tkinter as tk

import fastcom
import speedtest

d = 0

st = speedtest.SpeedTestObject()
fc = fastcom.FastCom()


def download_gui():
    global d
    x = fc.download(timeout=40)
    d = " Download Speed : " + str(x) + " MBPS "


def ping_gui():
    global p
    x = st.ping()
    p = "Ping: " + str(x) + "ms"



def speed():
    top = tk.Toplevel()
    top.grab_set()
    top.config(bg="#040837")
    top.minsize(400, 200)
    top.resizable(0, 0)
    f = tk.Label(top, bg="#040837")
    f.grid(row=0)

    dl = tk.Label(top, text=" Download Speed : --- MBPS ", width=28)
    dl.grid(row=2, column=0, pady=22)
    dl.config(font=("Courier", 17, "bold"), bg="#124576", fg="white")

    b1.config(text="Calculating...")
    b1.update()
    t1 = threading.Thread(target=download_gui, args=())
    t1.start()
    t1.join()
    if d:
        dl.config(text=d)
    else:
        dl.config(text="Cannot Connect")
    dl.update()
    b1.config(text="Calculate Speed")
    b1.update()


def ping():
    top = tk.Toplevel()
    top.grab_set()
    top.config(bg="#040837")
    top.minsize(400, 200)
    top.resizable(0, 0)
    f = tk.Label(top, bg="#040837")
    f.grid(row=0)

    dl = tk.Label(top, text=" Ping : --- ms ", width=28)
    dl.grid(row=2, column=0, pady=22)
    dl.config(font=("Courier", 17, "bold"), bg="#124576", fg="white")

    b1.config(text="Calculating...")
    b1.update()
    t1 = threading.Thread(target=ping_gui(), args=())
    t1.start()
    t1.join()
    if p:
        dl.config(text=p)
    else:
        dl.config(text="Cannot Connect")
    dl.update()
    b1.config(text="Ping")
    b1.update()


root = tk.Tk()
label = tk.Label(text="Speed")
label.config(font=("Courier", 30, "bold"), width=17, bg="white", fg="#040837")
label.grid(row=1, column=1, pady=50)

b1 = tk.Button(text="Download Speed", command=speed)
b1.config(font=("Courier", 25, "bold"), width=16, bg="#124576", fg="white", relief="raised", bd=10)
b1.grid(row=2, column=1, pady=20)

b3 = tk.Button(text="Ping", command=ping)
b3.config(font=("Courier", 25, "bold"), width=16, bg="#124576", fg="white", relief="raised", bd=10)
b3.grid(row=3, column=1, pady=20)

b2 = tk.Button(text="Exit", command=root.quit)
b2.config(font=("Courier", 25, "bold"), width=16, bg="#124576", fg="white", relief="raised", bd=10)
b2.grid(row=4, column=1, pady=20)

root.config(bg="#040837")
root.minsize(400, 400)
root.resizable(0, 0)
root.mainloop()
