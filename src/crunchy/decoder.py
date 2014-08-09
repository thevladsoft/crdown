import gzip
import math
import zlib
import base64
import hashlib
import array
from binascii import hexlify, unhexlify

import lxml
from bs4 import BeautifulSoup
from Crypto.Cipher import AES


class crunchyDec:
    def __init__(self):
        pass

    def returnSubs(self, xml):
        _id, _iv, _data = self.strainSoup(xml)
        print "Attempting to decrypt subtitles..."
        decryptedSubs = self.decodeSubtitles(_id, _iv, _data)

        formattedSubs = self.convertToASS(decryptedSubs)
        print "Success! Subtitles decrypted."
        return formattedSubs

    def strainSoup(self, xml):
        soup = BeautifulSoup(xml)
        subtitle = soup.find('subtitle', attrs={'link': None})
        if subtitle:
            _id = int(subtitle['id'])
            _iv = subtitle.find('iv').contents[0]
            _data = subtitle.data.string
            return _id, _iv, _data
        else:
            print "Couldn't parse XML file."

    def convertToASS(self, script):
        soup = BeautifulSoup(script, 'xml')
        header = soup.find('subtitle_script')
        header = ("[Script Info]\nTitle: "+header['title']+"\nScriptType: v4.00+\nWrapStyle: "+header['wrap_style'] +
                  "\nPlayResX: 656\nPlayResY: 368\n\n")
        styles = ("[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour," +
                  "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle," +
                  "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
        events = "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        stylelist = soup.findAll('style')
        eventlist = soup.findAll('event')

        for style in stylelist:
            styles += ("Style: " + style['name'] + "," + style['font_name'] + "," + style['font_size'] + "," +
                       style['primary_colour'] + "," + style['secondary_colour'] + "," + style['outline_colour'] +
                       "," + style['back_colour'] + "," + style['bold'] + "," + style['italic'] + "," +
                       style['underline'] + "," + style['strikeout'] + "," + style['scale_x'] + "," + style['scale_y'] +
                       "," + style['spacing'] + "," + style['angle'] + "," + style['border_style'] + "," +
                       style['outline'] + "," + style['shadow'] + "," + style['alignment'] + "," + style['margin_l'] +
                       "," + style['margin_r'] + "," + style['margin_v'] + "," + style['encoding'] + "\n")

        for event in eventlist:
            events += ("Dialogue: 0,"+event['start']+","+event['end']+","+event['style']+","+event['name'] +
                       ","+event['margin_l']+","+event['margin_r']+","+event['margin_v']+","+event['effect']+"," +
                       event['text']+"\n")

        formattedSubs = header+styles+events
        return formattedSubs

    # ---- CRYPTO -----
    def generateKey(self, mediaid, size=32):
        # Below: Do some black magic
        eq1 = int(int(math.floor(math.sqrt(6.9) * math.pow(2, 25))) ^ mediaid)
        eq2 = int(math.floor(math.sqrt(6.9) * math.pow(2, 25)))
        eq3 = (mediaid ^ eq2) ^ (mediaid ^ eq2) >> 3 ^ eq1 * 32
        # Below: Creates a 160-bit SHA1 hash
        shaHash = hashlib.sha1()
        shaHash.update(self.createString([20, 97, 1, 2]) + str(eq3))
        finalHash = shaHash.digest()
        hashArray = array.array('B', finalHash)
        #hashArray = Common().createByteArray(finalHash)
        # Below: Pads the 160-bit hash to 256-bit using zeroes, incase a 256-bit key is requested
        padding = [0]*4*3
        hashArray.extend(padding)
        keyArray = [0]*size
        # Below: Create a string of the requested key size
        for i, item in enumerate(hashArray[:size]):
            keyArray[i] = item
        return hashArray.tostring()

    def createString(self, args):
        i = 0
        argArray = [args[2], args[3]]
        while(i < args[0]):
            argArray.append(argArray[-1] + argArray[-2])
            i = i + 1
        finalString = ""
        for arg in argArray[2:]:
            finalString += chr(arg % args[1] + 33)
        return finalString

    def decodeSubtitles(self, id, iv, data):
        compressed = True
        key = self.generateKey(id)
        iv = base64.b64decode(iv)
        data = base64.b64decode(data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decryptedData = cipher.decrypt(data)

        if compressed:
            return zlib.decompress(decryptedData)
        else:
            return decryptedData
