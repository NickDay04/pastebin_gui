from tkinter import filedialog
from tkinter import *
import subprocess as sp
import webbrowser
import os
import requests

# output = sp.getoutput("pastebin get VEA8sQXN") - return "test"

path = r"C:\PastebinGUI"
try:
    os.mkdir(path)
except:
    pass

global pasteContent
global url
pasteContent = ""
url = ""

def registerFun():

    registerWin = Toplevel(root)

    def devKeyHelpFun():

        devKeyHelpWin = Toplevel(registerWin)

        def callback(url):
            webbrowser.open_new(url)

        infoLabel1 = Label(devKeyHelpWin, text="To get your developer key click")
        infoLabel1.pack()

        hyperlink = Label(devKeyHelpWin, text="here", fg="blue", cursor="hand2")
        hyperlink.pack()
        hyperlink.bind("<Button-1>", lambda e: callback("https://pastebin.com/doc_api#1"))

        infoLabel2 = Label(devKeyHelpWin, text="and the key should be near the top (ensuring you are logged in).")
        infoLabel2.pack()

    
    def registerFun():

        # key = PastebinAPI.user_details(devKeyEntry.get(), usernameEntry.get(), passwordEntry.get())
        # \n{key}
        writeString = f"{usernameEntry.get()}\n{passwordEntry.get()}\n{devKeyEntry.get()}"

        with open(r"C:\PastebinGUI\userinfo.txt", "w+") as userInfo:

            userInfo.write(writeString)
        
        registerWin.destroy()

    usernameStringVar = StringVar()
    passwordStringVar = StringVar()
    devKeyStringVar = StringVar()

    try:

        with open(r"C:\PastebinGUI\userinfo.txt", "r") as userInfo:

            userInfoList = userInfo.readlines()

            usernameStringVar.set(userInfoList[0])
            passwordStringVar.set(userInfoList[1])
            devKeyStringVar.set(userInfoList[2])

    except:

        usernameStringVar.set("")
        passwordStringVar.set("")
        devKeyStringVar.set("")

    usernameLabel = Label(registerWin, text="Username: ")
    usernameLabel.grid(row=0, column=0)
    # devKeyEntry["textvariable"] = devKey

    usernameEntry = Entry(registerWin)
    usernameEntry.grid(row=0, column=1)
    usernameEntry["textvariable"] = usernameStringVar

    passwordLabel = Label(registerWin, text="Password: ")
    passwordLabel.grid(row=1, column=0)

    passwordEntry = Entry(registerWin)
    passwordEntry.grid(row=1, column=1)
    passwordEntry["textvariable"] = passwordStringVar

    devKeyLabel = Label(registerWin, text="Developer Key: ")
    devKeyLabel.grid(row=2, column=0)

    devKeyEntry = Entry(registerWin)
    devKeyEntry.grid(row=2, column=1)
    devKeyEntry["textvariable"] = devKeyStringVar

    devKeyHelp = Button(registerWin, text="Need help getting developer key?", command=devKeyHelpFun)
    devKeyHelp.grid(row=2, column=2)

    registerButton = Button(registerWin, text="Register", command=registerFun)
    registerButton.grid(row=3, column=1)

    backButton = Button(registerWin, text="Back", command=registerWin.destroy)
    backButton.grid(row=3, column=2)


def pasteFun():

    pasteWin = Toplevel(root)

    def callback(url):

        webbrowser.open_new(urlLabel["text"])

    def selectFileFun():

        filePath = filedialog.askopenfilename()

        with open(filePath, "r") as pasteFile:

            selectFileFun.pasteContent = pasteFile.read()

    def submitPasteFun():

        with open(r"C:\PastebinGUI\userinfo.txt", "r+") as userInfo:

            userInfoList = userInfo.readlines()

            login_data = {
                'api_dev_key': userInfoList[2].strip(),
                'api_user_name': userInfoList[0].strip(),
                'api_user_password': userInfoList[1].strip()
            }

            data = {
                'api_option': 'paste',
                'api_dev_key': userInfoList[2],
                'api_paste_code': selectFileFun.pasteContent,
                'api_paste_name': pasteNameEntry.get(),
                'api_paste_expire_date': expiryDictBE[expiryVar.get()],
                'api_user_key': None,
                'api_paste_format': None if pasteTypeEntry.get() == "" else pasteTypeEntry.get()
            }

            login = requests.post("https://pastebin.com/api/api_login.php", data=login_data)
            data['api_user_key'] = login.text

            r = requests.post("https://pastebin.com/api/api_post.php", data=data)
            url = r.text

            urlLabel["text"] = url

    def pasteTypeHyperlinkFun(event):

        webbrowser.open_new("https://pastebin.com/doc_api#5")

    devKeyLabel = Label(pasteWin, text="Developer key: ")
    devKeyLabel.grid(row=0, column=0)

    devKey = StringVar()

    try:

        with open(r"C:\PastebinGUI\userinfo.txt", "r") as userInfo:

            userInfoList = userInfo.readlines()
            devKey.set(userInfoList[2])
    
    except:

        devKey.set("")

    devKeyEntry = Entry(pasteWin)
    devKeyEntry.grid(row=0, column=1)
    devKeyEntry["textvariable"] = devKey

    selectFileButton = Button(pasteWin, text="Select file", command=selectFileFun)
    selectFileButton.grid(row=0, column=2, columnspan=2)

    pasteNameLabel = Label(pasteWin, text="Paste name: ")
    pasteNameLabel.grid(row=1, column=0, sticky="W")

    pasteNameEntry = Entry(pasteWin)
    pasteNameEntry.grid(row=1, column=1)

    submitPasteButton = Button(pasteWin, text="Submit paste", command=submitPasteFun)
    submitPasteButton.grid(row=1, column=2, columnspan=2)

    pasteTypeLabel = Label(pasteWin, text="Paste format: ")
    pasteTypeLabel.grid(row=2, column=0, sticky="W")

    pasteTypeEntry = Entry(pasteWin)
    pasteTypeEntry.grid(row=2, column=1)

    pasteTypeHyperlink = Label(pasteWin, text="See more here", fg="blue", cursor="hand2")
    pasteTypeHyperlink.grid(row=2, column=2, columnspan=2)
    pasteTypeHyperlink.bind("<Button-1>", pasteTypeHyperlinkFun)

    pastePrivacyLabel = Label(pasteWin, text="Paste privacy")
    pastePrivacyLabel.grid(row=3, column=0, sticky="W")

    privacyVar = IntVar()
    privacyList = []

    privacyCBDict = {0: "Public", 1: "Unlisted", 2: "Private"}

    for i in range(3):

        privacyList.append(Checkbutton(pasteWin, onvalue=i, variable=privacyVar, text=privacyCBDict[i]))
        privacyList[i].grid(row=i+4, column=0, sticky="W")
    
    expiryDateLabel = Label(pasteWin, text="Expiry date")
    expiryDateLabel.grid(row=3, column=1, sticky="W")

    expiryVar = IntVar()
    expiryList = []

    expiryDictFE = {0: "Never", 1: "10 Minutes", 2: "1 Hour", 3: "1 Day", 4: "1 Month"} # Front end
    expiryDictBE = {0: "N", 1: "10M", 2: "1H", 3: "1D", 4: "1M"} # Back end

    for i in range(5):

        expiryList.append(Checkbutton(pasteWin, onvalue=i, variable= expiryVar, text=expiryDictFE[i]))
        expiryList[i].grid(row=i+4, column=1, sticky="W")
    
    urlLabel = Label(pasteWin, text="", fg="blue", cursor="hand2")
    urlLabel.grid(row=3, column=2, rowspan=6, columnspan=2)
    urlLabel.bind("<Button-1>", callback)


def getFun():

    getWin = Toplevel(root)

    def getDirFun():
        
        global filePath
        filePath = filedialog.askdirectory()
    
    def getPasteFun(filePath):

        pasteContent = sp.getoutput(f"pastebin get {keyEntry.get()}")

        print(filePath)

        with open(os.path.join(filePath, fileNameEntry.get() + ".txt"), "w+") as outputTextFile:

            outputTextFile.write(pasteContent)

    keyLabel = Label(getWin, text="Key:")
    keyLabel.grid(row=0, column=0)

    keyEntry = Entry(getWin)
    keyEntry.grid(row=0, column=1)

    fileNameLabel = Label(getWin, text="File name:")
    fileNameLabel.grid(row=1, column=0)

    fileNameEntry = Entry(getWin)
    fileNameEntry.grid(row=1, column=1)

    fileLocationButton = Button(getWin, text="Select file location", command=getDirFun)
    fileLocationButton.grid(row=2, column=0)

    getPasteButton = Button(getWin, text="Get paste", command=lambda: getPasteFun(filePath))
    getPasteButton.grid(row=2, column=1)

# output = sp.getoutput("pastebin get VEA8sQXN")
root = Tk()

registerButton = Button(root, text="Register", command=registerFun)
registerButton.pack()

pasteButton = Button(root, text="Paste", command=pasteFun)
pasteButton.pack()

getButton = Button(root, text="Get", command=getFun)
getButton.pack()

root.mainloop()

if __name__ == "__main__":

    try:

        with open(r"C:\PastebinGUI\userinfo.txt", "r"):

            pass
    
    except:

        with open(r"C:\PastebinGUI\userinfo.txt", "r+"):

            pass

    
