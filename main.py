from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import pandas as pd


# general window setup
window = Tk()
window.title("Batch Mailer")

mainframe = Frame(window)
mainframe.grid(column=0, row=0, sticky=(N, E, S, W))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

# --- server settings frame
server_settings_frame = Frame(mainframe)
server_settings_frame.pack(fill=X)

# smtp server
Label(server_settings_frame, text="SMTP Server").pack(side=LEFT)

smtp_server = Entry(server_settings_frame)
smtp_server.pack(side=LEFT)

# username
Label(server_settings_frame, text="Username").pack(side=LEFT)

username = Entry(server_settings_frame)
username.pack(side=LEFT)

# password
Label(server_settings_frame, text="Password").pack(side=LEFT)

password = Entry(server_settings_frame)
password.pack(side=LEFT)

# --- list settings
list_settings_frame = Frame(mainframe)
list_settings_frame.pack(fill=X)

table = None
processed_mails = StringVar()
processed_mails.set("0 / 0")


def load_csv() -> None:
    global table

    filename = askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filename:
        table = pd.read_csv(filename)
        if table is not None:
            processed_mails.set(f"0 / {table.shape[0]}")


load_csv_button = Button(list_settings_frame, text="Load CSV", command=load_csv)
load_csv_button.pack(side=LEFT)

Label(list_settings_frame, text="Mail Address Column").pack(side=LEFT)
address_column = Entry(list_settings_frame)
address_column.pack(side=LEFT)

# bcc
Label(list_settings_frame, text="Send a blind copy to your own mail adress").pack(
    side=LEFT
)

bcc = Checkbutton(list_settings_frame)
bcc.pack(side=LEFT)

# --- mail settings frame
mail_settings_frame = Frame(mainframe)
mail_settings_frame.pack(fill=X)

# mail subject
Label(mail_settings_frame, text="Subject").pack(side=LEFT)

subject = Entry(mail_settings_frame)
subject.pack(side=LEFT)

# mail text
mail_frame = Frame(mainframe)
mail_frame.pack(fill=X)

Label(mail_frame, text="Mail Text").pack(side=LEFT)

mail_text = Text(mail_frame)
mail_text.pack(side=LEFT)

# --- send mails
send_frame = Frame(mainframe)
send_frame.pack(fill=X)


def send_mails() -> None:
    pass


send_buttom = Button(send_frame, text="Send Mails", command=send_mails)
send_buttom.pack(side=LEFT)

progress = Progressbar(send_frame, orient=HORIZONTAL, length=200, mode="determinate")
progress.pack(side=LEFT)

progress_text = Label(send_frame, textvariable=processed_mails)
progress_text.pack(side=LEFT)

window.mainloop()
