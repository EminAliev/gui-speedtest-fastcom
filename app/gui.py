import threading
import tkinter as tk

from gui_speedtest_fastcom import speedtest, fast

download = 0
upload = 0
ping = 0
st = speedtest.SpeedTest()
fc = fast.Fast()


def download_fast():
    global download
    x = fc.download()
    download = " Download Speed : " + str(x) + " MBPS "


def download_speedtest():
    global download
    x = st.download()
    download = " Download Speed : " + str(x)


def upload_speedtest():
    global upload
    x = st.upload()
    upload = " Upload Speed: " + str(x)


def ping_text():
    global ping
    x = st.ping()
    ping = "Ping: " + str(x) + "ms"


def threading_function(func):
    t1 = threading.Thread(target=func, args=())
    t1.start()
    t1.join()


def speed_test():
    top = tk.Toplevel()
    top.grab_set()
    top.config(bg="#000080")
    top.minsize(400, 200)
    top.resizable(0, 0)
    top.title('GUI')
    f = tk.Label(top, bg="#000080")
    f.grid(row=0)
    dl = tk.Label(top, text=" Download Speed : --- MBPS ", width=28)
    dl.grid(row=1, column=0, pady=22)
    dl.config(font=("Ubuntu", 20, "bold"), bg="#00BFFF", fg="white")

    dl_2 = tk.Label(top, text=" Upload Speed : --- MBPS ", width=28)
    dl_2.grid(row=2, column=0, pady=22)
    dl_2.config(font=("Ubuntu", 20, "bold"), bg="#00BFFF", fg="white")

    dl_3 = tk.Label(top, text=" Ping : --- ms ", width=28)
    dl_3.grid(row=3, column=0, pady=22)
    dl_3.config(font=("Ubuntu", 20, "bold"), bg="#00BFFF", fg="white")

    b1.config(text="Calculating...")
    b1.update()

    threading_function(download_speedtest)
    threading_function(upload_speedtest)
    threading_function(ping_text)
    if download and upload and ping:
        dl.config(text=download)
        dl_2.config(text=upload)
        dl_3.config(text=ping)
    else:
        dl.config(text="Cannot Connect")
    dl.update()
    b1.config(text="Calculate Speed")
    b1.update()


def fast_test():
    top = tk.Toplevel()
    top.grab_set()
    top.config(bg="#000080")
    top.minsize(400, 200)
    top.resizable(0, 0)
    top.title('GUI')
    f = tk.Label(top, bg="#000080")
    f.grid(row=0)
    dl = tk.Label(top, text=" Download Speed : --- MBPS ", width=28)
    dl.grid(row=1, column=0, pady=22)
    dl.config(font=("Ubuntu", 20, "bold"), bg="#00BFFF", fg="white")

    b1.config(text="Calculating...")
    b1.update()
    threading_function(download_fast)
    if download:
        dl.config(text=download)
    else:
        dl.config(text="Cannot Connect")
    dl.update()
    b1.config(text="Calculate Speed")
    b1.update()


root = tk.Tk()
label = tk.Label(text="GUI")
label.config(font=("Ubuntu", 30, "bold"), width=17, bg="white", fg="#040837")
label.grid(row=1, column=1, pady=50)

b1 = tk.Button(text="SpeedTest", command=speed_test)
b1.config(font=("Ubuntu", 25, "bold"), width=16, bg="#00BFFF", fg="white", relief="raised", bd=10)
b1.grid(row=2, column=1, pady=20)

b3 = tk.Button(text="Fast.com", command=fast_test)
b3.config(font=("Ubuntu", 25, "bold"), width=16, bg="#00BFFF", fg="white", relief="raised", bd=10)
b3.grid(row=3, column=1, pady=20)

b2 = tk.Button(text="Exit", command=root.quit)
b2.config(font=("Ubuntu", 25, "bold"), width=16, bg="#00BFFF", fg="white", relief="raised", bd=10)
b2.grid(row=4, column=1, pady=20)

root.config(bg="#000080")
root.minsize(400, 400)
root.resizable(0, 0)
root.title('GUI')
root.mainloop()
