from tkinter import filedialog
from tkinter import *
import webbrowser
import os
import requests

# Make the folder where the user info is stored
path = os.getenv("APPDATA")
path = os.path.join(path, "PastebinGUI")
try:
    os.mkdir(path)
except:
    pass

# Update path to involve the file
path = os.path.join(path, "userInfo.txt")

global pasteContent
global url
pasteContent = ""
url = ""

# Function holding the register window
def registerFun():

    registerWin = Toplevel(root)

    # Function holding the help window
    def devKeyHelpFun():

        devKeyHelpWin = Toplevel(registerWin)

        # This function opens a url in the webbrowser (used for hyperlinks)
        def callback(url):
            webbrowser.open_new(url)

        infoLabel1 = Label(devKeyHelpWin, text="To get your developer key click")
        infoLabel1.pack()

        hyperlink = Label(devKeyHelpWin, text="here", fg="blue", cursor="hand2")
        hyperlink.pack()
        hyperlink.bind("<Button-1>", lambda e: callback("https://pastebin.com/doc_api#1")) # This functions as a hyperlink

        infoLabel2 = Label(devKeyHelpWin, text="and the key should be near the top (ensuring you are logged in).")
        infoLabel2.pack()

    
    def registerFun():

        writeString = f"{usernameEntry.get()}\n{passwordEntry.get()}\n{devKeyEntry.get()}"

        with open(path, "w+") as userInfo:

            userInfo.write(writeString)
        
        registerWin.destroy()

    usernameStringVar = StringVar()
    passwordStringVar = StringVar()
    devKeyStringVar = StringVar()

    # I used a try/except statement in case the user hadn't registered yet so it wouldn't throw an error
    try:

        with open(path, "r") as userInfo:

            userInfoList = userInfo.readlines()

            usernameStringVar.set(userInfoList[0])
            passwordStringVar.set(userInfoList[1])
            devKeyStringVar.set(userInfoList[2])

    # Sets the values of the variables if the user hasn't registered
    except:

        usernameStringVar.set("")
        passwordStringVar.set("")
        devKeyStringVar.set("")

    usernameLabel = Label(registerWin, text="Username: ")
    usernameLabel.grid(row=0, column=0)

    usernameEntry = Entry(registerWin)
    usernameEntry.grid(row=0, column=1)
    usernameEntry["textvariable"] = usernameStringVar # Autofills the username box

    passwordLabel = Label(registerWin, text="Password: ")
    passwordLabel.grid(row=1, column=0)

    passwordEntry = Entry(registerWin)
    passwordEntry.grid(row=1, column=1)
    passwordEntry["textvariable"] = passwordStringVar # Autofills the password box

    devKeyLabel = Label(registerWin, text="Developer Key: ")
    devKeyLabel.grid(row=2, column=0)

    devKeyEntry = Entry(registerWin)
    devKeyEntry.grid(row=2, column=1)
    devKeyEntry["textvariable"] = devKeyStringVar # Autofills the developer key box

    devKeyHelp = Button(registerWin, text="Need help getting developer key?", command=devKeyHelpFun)
    devKeyHelp.grid(row=2, column=2)

    registerButton = Button(registerWin, text="Register", command=registerFun)
    registerButton.grid(row=3, column=1)

    backButton = Button(registerWin, text="Back", command=registerWin.destroy)
    backButton.grid(row=3, column=2)

# Function opens the window to submit a paste
def pasteFun():

    pasteWin = Toplevel(root)

    # Opens a url in the webbrowser for hyperlinks
    def callback(url):

        webbrowser.open_new(urlLabel["text"])

    def selectFileFun():

        # Opens a dialogue box and returns the file path and file name selected by the user
        filePath = filedialog.askopenfilename()

        with open(filePath, "r") as pasteFile:

            # Reads the contents of the file and stores it to be submitted in a paste
            selectFileFun.pasteContent = pasteFile.read()

    def submitPasteFun():

        with open(path, "r+") as userInfo:

            userInfoList = userInfo.readlines()

            # Assembles all the data used to log the user in
            login_data = {
                'api_dev_key': userInfoList[2].strip(),
                'api_user_name': userInfoList[0].strip(),
                'api_user_password': userInfoList[1].strip()
            }

            # Assembles all the data to submit a new paste
            data = {
                'api_option': 'paste',
                'api_dev_key': userInfoList[2],
                'api_paste_code': selectFileFun.pasteContent,
                'api_paste_name': pasteNameEntry.get(),
                'api_paste_expire_date': expiryDictBE[expiryVar.get()],
                'api_user_key': None,
                'api_paste_format': None if pasteTypeEntry.get() == "" else pasteTypeEntry.get()
            }

            login = requests.post("https://pastebin.com/api/api_login.php", data=login_data) # Logs the user in to get the user key
            data['api_user_key'] = login.text # Sets the user key in the data dictionary

            r = requests.post("https://pastebin.com/api/api_post.php", data=data) # Submits the post
            url = r.text # Stores the response

            # Handles non-url responses from the server         
            if url == "Bad API request, invalid api_dev_key":

                urlLabel["text"] = "Invalid developer key"

            elif url == "Bad API request, maximum number of 25 unlisted pastes for your free account":

                urlLabel["text"] = "You have reached the maximum number of unlisted pastes"
            
            elif url == "Bad API request, maximum number of 10 private pastes for your free account":

                urlLabel["text"] = "You have reaced the maximum number of private pastes"
            
            elif url == "Bad API request, api_paste_code was empty":

                urlLabel["text"] = "Your paste is empty"
            
            elif url == "Bad API request, maximum paste file size exceeded":

                urlLabel["text"] = "Your file size exceeds the maximum file size"

            elif url == "Bad API request, invalid api_paste_format":

                urlLabel["text"] = "Invalid paste format"

            else:

                urlLabel["text"] = url

    # Lambda wasn't working so I made another function to handle one specific hyperlink
    def pasteTypeHyperlinkFun(event):

        webbrowser.open_new("https://pastebin.com/doc_api#5")

    devKeyLabel = Label(pasteWin, text="Developer key: ")
    devKeyLabel.grid(row=0, column=0)

    devKey = StringVar()

    # Try/except statement used in case user hasn't registered
    try:

        with open(path, "r") as userInfo:

            userInfoList = userInfo.readlines()
            devKey.set(userInfoList[2])
    
    except:

        devKey.set("")

    devKeyEntry = Entry(pasteWin)
    devKeyEntry.grid(row=0, column=1)
    devKeyEntry["textvariable"] = devKey # Auto fills developer key box

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
    pasteTypeHyperlink.bind("<Button-1>", pasteTypeHyperlinkFun) # Hyperlink to open different paste formats

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
    urlLabel.bind("<Button-1>", callback) # Hyperlink to open the url if the paste was sucessful


# Opens window to get a paste
def getFun():

    getWin = Toplevel(root)

    # Gets the directory for the text file paste to be stored in
    def getDirFun():
        
        global filePath
        filePath = filedialog.askdirectory()
    
    def getPasteFun(filePath):

        response = requests.get(f"https://pastebin.com/raw/{keyEntry.get()}")
        pasteContent = response.text

        with open(os.path.join(filePath, fileNameEntry.get() + ".txt"), "w+") as outputTextFile:

            outputTextFile.write(pasteContent) # Writes the paste to a text file


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

root = Tk()

registerButton = Button(root, text="Register", command=registerFun)
registerButton.pack()

pasteButton = Button(root, text="Paste", command=pasteFun)
pasteButton.pack()

getButton = Button(root, text="Get", command=getFun)
getButton.pack()

root.mainloop()

if __name__ == "__main__":

    # Tries to open the file holding the user data
    try:

        with open(path, "r"):

            pass
    
    # If that fails (userInfo.txt doesn't exist) it creates userInfo
    except:

        with open(path, "r+"):

            pass
