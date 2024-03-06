# https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_quick_guide.htm

import base64

class Cipher():
    
    def __init__(self):
        self.toMapStr  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.@#$%*!-_+:='
        self.mappedStr = 'TUVW@#$XYZA6789.BCwxyzabcNOP%*!-QRSdef345ghijkl_+:mDEFGH012IJK=LMnopqrstuv'
        self.defaultPassKey = "passkey@2021#Jun"
        self.trans = self.makeMapping(self.toMapStr, self.mappedStr)
        #print (self.trans)
        self.reverseTrans = self.makeMapping(self.mappedStr, self.toMapStr)
        #print (self.reverseTrans)
        self.encryptText = ""
        self.plainText = ""

        return
    
    def makeMapping(self, str1, str2):
        if len(str1) != len(str2):
            return {}
        mapDict = {}
        for i in range(len(str1)):
            mapDict[str1[i]] = str2[i]   
            
        if " " in mapDict:
            return mapDict
        
        mapDict[" "] = " "
        return mapDict
        
    def translationEncrypt(self, text):
        transText = ""
        for i in range(len(text)):
            transText = transText + self.trans[text[i]]       
        return transText
    
    def translationDecrypt(self, text):
        rtransText = ""
        for i in range(len(text)):
            rtransText = rtransText + self.reverseTrans[text[i]]       
        return rtransText
    
    def base64Encode(self, text):
        textByte = text.encode("utf-8")
        return base64.urlsafe_b64encode(textByte).decode("utf-8") 
    
    def base64Decode(self, text):
        return base64.urlsafe_b64decode(text).decode('utf-8')

    def encrypt(self, text, passkey = None):
        if passkey == None:
            text = text + self.defaultPassKey
        else:
            text = text + passkey
            
        encText = self.translationEncrypt(text)
        self.encryptText = self.base64Encode(encText)
        return self.encryptText
    
    def decrypt(self, encryptText, passkey = None):
        encTextWithKey = self.base64Decode(encryptText)
        plainTextWithPasskey = self.translationDecrypt(encTextWithKey)
        
        if passkey == "":
            return plainTextWithPasskey
        
        if passkey == None:
            text = plainTextWithPasskey.replace(self.defaultPassKey, "")
        else:
            text = plainTextWithPasskey.replace(passkey, "")
        return text     
        
#
# #check the above function
# text = "CEASER CIPHER DEMO"
#
# cipher = Cipher()
#
# print ("Plain Text : " + text)
# print ("Cipher: " + cipher.translationEncrypt(text))
# print ("Base64: " + cipher.base64Encode(cipher.translationEncrypt(text)))
# print ("DeCipher: " + cipher.translationDecrypt(cipher.translationEncrypt(text)))
#
# encText = cipher.encrypt(text)
# print ("Cipher Text: " + encText)
# print ("Decrypt Text: " + cipher.decrypt(encText))
#


