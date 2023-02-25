import json
import os
import re
import socket
import struct
import sys
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

MAGIC = 0x0000EA6E
PORT = 9045


def getCurrentDirectory():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)


def choosefile():
    file = fd.askopenfilename()
    choose_file_box.delete(0, tk.END)
    choose_file_box.insert(0, file)


def sendfile():
    sendfile_button.config(state="disabled")

    # Validate IP address
    ip = enter_ip.get()
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        mb.showerror("Error", "Invalid IP address!")
        sendfile_button.config(state="normal")
        return

    # Validate filepath
    filepath = choose_file_box.get()
    if not os.path.exists(filepath):
        mb.showerror("Error", "File does not exist!")
        sendfile_button.config(state="normal")
        return

    try:
        # Get filesize
        stats = os.stat(filepath)

        # # Update progress bar
        # progress = wx.ProgressDialog('Uploading', 'Sending file to console...', stats.st_size, self.panel)

        with open(filepath, 'rb') as f:
            # Connect to console
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, PORT))

            # Send magic
            sock.sendall(struct.pack('<I', MAGIC))

            # Send filesize
            sock.sendall(struct.pack('<Q', stats.st_size))

            # Loop in chunks of 4096
            sent = 0
            while True:
                data = f.read(4096)
                if data == b'':
                    break
                sock.sendall(data)
                sent += len(data)
                # progress.Update(sent)
                # wx.Yield()

            # Close connection
            sock.close()

            mb.showinfo("Success", "Successfully sent file to PS4/PS5!")

            # Save values to config
            with open(os.path.join(getCurrentDirectory(), 'mast1c0re-file-loader.json'), 'w') as f:
                f.write(json.dumps({
                    'ip': ip,
                    'file': filepath,
                }, indent=4))

            sendfile_button.config(state="normal")

    except socket.error:
        mb.showerror("Error", "Failed to connect!")
        sendfile_button.config(state="normal")


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("500x140")
    window.resizable(False, False)

    window.title("Mast1c0re File Loader")

    choose_file_box = tk.Entry(window, width=40)
    choose_file = tk.Button(window, text="Select File", command=choosefile)

    enter_ip_label = tk.Label(window, text="Enter IP-Address of your PS4/PS5:")
    enter_ip = tk.Entry(window, width=27)

    sendfile_button = tk.Button(window, text="Send File to PS4/PS5", width=49, command=sendfile)

    # Load config
    try:
        with open(os.path.join(getCurrentDirectory(), 'mast1c0re-file-loader.json')) as f:
            config = json.load(f)
            if 'ip' in config:
                enter_ip.insert(0, config['ip'])
            if 'file' in config:
                choose_file_box.insert(0, config['file'])
    except:
        config = {}

    choose_file_box.place(x=10, y=10)
    choose_file.place(x=390, y=8)

    enter_ip_label.place(x=10, y=50)
    enter_ip.place(x=230, y=48)

    sendfile_button.place(x=10, y=90)

    window.mainloop()
