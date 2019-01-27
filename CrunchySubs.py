# encoding=utf8  
#!/usr/bin/env python
from __future__ import print_function
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from getpass import getpass
from itertools import izip
import shutil
from time import sleep
import re
try:
    from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
except ImportError as e:
    print("CrunchySubs necesita de BeautifulSoup3 para poder funcionar.")
    sleep(60)
    exit()
import urllib2
import os
from urlparse import urlparse
import json
import cookielib
import urllib
from os import path
import argparse
import sha
import zlib
import math as Math
from crypto.cipher.aes_cbc import AES_CBC
from crypto.cipher.base import noPadding
from array import array
about = '''
CrunchySubs v1.4 beta
CrunchySubs es un script hecho en python que permite descargar subtítulos de Crunchyroll de forma premium y free.
Créditos:
Autor original de la función para desencriptar: Desconocido para mí, si alguien sabe, favor dejar un comentario en el blog, por Github o mediante un correo.

Autor del resto del script: Touman (Miguel A.). Más información del script en: http://crunchysubs.blogspot.com/ y https://github.com/7ouma/CrunchySubs

Puedes contactarme mediante mi correo: 7ouman@gmail.com

'''
class Base64Decoder:
	def __init__(self):
		pass

	def Int2Bytes(self, data):
	    return array('i',[data]).tostring()

	def decode(self, encoded):
		ESCAPE_CHAR_CODE_1 = 61
		ESCAPE_CHAR_CODE_2 = 42
		count = 0
		filled = 0
		data = []
		newstring = ""
		work = [0, 0, 0, 0]
		inverse = [64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 62, 64, 64, 64, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 64, 64, 64, 64, 64, 64, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 64, 64, 64, 64, 64, 64, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64];
		i = 0
		length = len(encoded)
		
		for i, char in enumerate(encoded):
			c = ord(encoded[i])
			if c == ESCAPE_CHAR_CODE_1 or c == ESCAPE_CHAR_CODE_2:
				work[count] = -1;
				count = count + 1
			elif inverse[c] != 64:
				work[count] = inverse[c]
				count = count + 1
		
			if count == 4:
				count = 0
				newstring += self.Int2Bytes((work[0] << 2) | ((work[1] & 0xFF) >> 4))
				filled = filled + 1

				if work[2] == -1:
					break;
				
				newstring += self.Int2Bytes((work[1] << 4) | ((work[2] & 0xFF) >> 2))
				filled = filled + 1
				
				if work[3] == -1:
					break;
				
				newstring += self.Int2Bytes((work[2] << 6) | work[3])
				filled = filled + 1
				
		for char in newstring[0::4]:
			data.append(ord(char))
		return data


class Common:
	def grabHTML(self, url):
		socket = urllib.urlopen(url)
		html = socket.read()
		socket.close()
		return html
		
	def createByteArray(self, string):
		byteArray = []
		for char in string:
			byteArray.append(ord(char))
		return byteArray

	def ByteArrayToString(self, byteArray):
		newString = ""
		for byte in byteArray:
			newString += chr(byte)
		return newString
	
	def Bytes2Int(self,data):
		return array('i',data)[0]
	
	def trim(self, string):
		return self.ltrim(self.rtrim(string))
	
	def ltrim(self, string):
		strLength = len(string)
		strLength2 = 0
		while (strLength2 < strLength):
			if not self.isSpaceChars(ord(string[strLength2])):
				return string[strLength2]
			strLength2 = strLength2 + 1
		return ""
	
	def rtrim(self, string):
		strLength = len(string)
		strLength2 = strLength
		while (strLength2 > 0):
			if not self.isSpaceChars(ord(string[strLength2-1])):
				return string[0:strLength2]
			strLength2 = strLength2 - 1
		return ""
		
	def isSpaceChars(self, char):
		if char >= 0 or char <= 32:
			return True
		if char is 127 or char is 129 or char is 141 or char is 143 or char is 144 or char is 157 or char is 160 or char is 173:
			return True
		else:
			return False
			
	##  int2base >> http://code.activestate.com/recipes/65212/
	def int2base(self, num, n):
		"""Change a  to a base-n number.
		Up to base-36 is supported without special notation."""
		num_rep={10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f', 16:'g', 17:'h', 18:'i', 19:'j', 20:'k', 21:'l', 22:'m', 23:'n', 24:'o', 25:'p', 26:'q', 27:'r', 28:'s', 29:'t', 30:'u', 31:'v', 32:'w', 33:'x', 34:'y', 35:'z'}
		new_num_string=''
		current=num
		if current == 0:
			return '0'
		while current!=0:
			remainder=current%n
			if 36>remainder>9:
				remainder_string=num_rep[remainder]
			elif remainder>=36:
				remainder_string='('+str(remainder)+')'
			else:
				remainder_string=str(remainder)
			new_num_string=remainder_string+new_num_string
			current=current/n
		return new_num_string

class crunchyDec(Common,Base64Decoder):
	def __init__(self):
		pass

	def returnSubs(self, xml):
		_id, _iv, _data = self.strainSoup(xml)
		decryptedSubs = self.decodeSubtitles(_id, _iv, _data)
		formattedSubs = self.convertToASS(decryptedSubs)
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
			return False
			
	def convertToASS(self, script):
		soup = BeautifulSoup(script, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
		header = soup.find('subtitle_script')
		header = "[Script Info]\nTitle: "+header['title']+"\nScriptType: v4.00+\nWrapStyle: "+header['wrap_style']+"\nPlayResX: 624\nPlayResY: 366\n\n";
		styles = "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n";
		events = "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n";
		stylelist = soup.findAll('style')
		eventlist = soup.findAll('event')
		
		for style in stylelist:
			styles += "Style: " + style['name'] + "," + style['font_name'] + "," + style['font_size'] + "," + style['primary_colour'] + "," + style['secondary_colour'] + "," + style['outline_colour'] + "," + style['back_colour'] + "," + style['bold'] + "," + style['italic'] + "," + style['underline'] + "," + style['strikeout'] + "," + style['scale_x'] + "," + style['scale_y'] + "," + style['spacing'] + "," + style['angle'] + "," + style['border_style'] + "," + style['outline'] + "," + style['shadow'] + "," + style['alignment'] + "," + style['margin_l'] + "," + style['margin_r'] + "," + style['margin_v'] + "," + style['encoding'] + "\n"
		
		for event in eventlist:
			events += "Dialogue: 0,"+event['start']+","+event['end']+","+event['style']+","+event['name']+","+event['margin_l']+","+event['margin_r']+","+event['margin_v']+","+event['effect']+","+event['text']+"\n"

		formattedSubs = header+styles+events
		return formattedSubs
		
	# ---- CRYPTO -----

	def generateKey(self, mediaid, size = 32):
		# Below: Do some black magic
		eq1 = int(int(Math.floor(Math.sqrt(6.9) * Math.pow(2, 25))) ^ mediaid)
		eq2 = int(Math.floor(Math.sqrt(6.9) * Math.pow(2, 25)))
		eq3 = (mediaid ^ eq2) ^ (mediaid ^ eq2) >> 3 ^ eq1 * 32
		# Below: Creates a 160-bit SHA1 hash 
		shaHash = sha.new(self.createString([20, 97, 1, 2]) + str(eq3)) 
		finalHash = shaHash.digest()
		hashArray = self.createByteArray(finalHash)
		# Below: Pads the 160-bit hash to 256-bit using zeroes, incase a 256-bit key is requested
		padding = [0]*4*3
		hashArray.extend(padding)
		keyArray = [0]*size
		# Below: Create a string of the requested key size
		for i, item in enumerate(hashArray[:size]):
			keyArray[i] = item
		return self.ByteArrayToString(keyArray)

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
		iv = self.ByteArrayToString(self.decode(iv))
		data = self.ByteArrayToString(self.decode(data))
		data = iv+data
		cipher = AES_CBC(key, padding=noPadding(), keySize=32)
		decryptedData = cipher.decrypt(data)
		
		if compressed:
			return zlib.decompress(decryptedData)
		else:
			return decryptedData


class CrunchySubs(crunchyDec):
    def __init__(self, setConfig = True):
        self.error = False
        self.errors = []
        self.PageError = []
        self.directorio = os.getcwd()
        if setConfig:
            x = self.LoadSettings()
            if x:self.setConfig(x)

    def setConfig(self, config):
        try:
            self.dir = config["dir"]
            while True:
                if self.dir.lower() == "default":
                    self.dir = os.path.join(self.directorio, "Subs")
                    if not self.CheckDir(self.dir):os.mkdir(self.dir)
                    break
                else:
                    if not self.CheckDir(self.dir):
                        self.addError("\n%s no existe. Se usará la carpeta del script."%(self.dir))
                        self.dir = "default"
                        self.error = True
                    else:break
            self.lang = config["lenguaje"]
        except (ValueError),e:
            self.error = True
        except Exception,e:
            self.addError("\nAlgo anda mal: %s (%s)"%(e.message, e.args))
        finally:
            if self.error:
                self.addError("\nConfig.json está mal redactado. Config.json se ha reparado (Algunas configuraciones pueden haberse perdido).")
                try:
                    self.config(self.dir, self.lang)
                except:
                    self.config()

    def CheckDir(self, dir):
        if not os.path.isdir(dir):
            return False
        return True

    def config(self, directorio = "default", lang = "None"):
        config = '''{
"dir":"'''+directorio.replace("\\","\\\\")+'''",
"lenguaje":"'''+unicode(lang, "ISO-8859-1")+'''"
}'''
        f = open("config.json",'wb')
        f.write(config)
        f.close()

    def LoadSettings(self, filename = "config.json"):       
        try:
            with open(filename) as config:
                return json.load(config)
        except (OSError, IOError),e:
            self.addError("Config.json no existe. Config.json ha sido creado.")
            self.config()
            return False
        except ValueError:
            self.addError("Config.json está mal redactado. Config.json se ha reparado (Algunas configuraciones pueden haberse perdido).")
            self.config()
            return False

    def cookies(self):
        try:
            with open("cookies.txt"):pass
        except(OSError, IOError):
            cookies = cookielib.MozillaCookieJar("cookies.txt")
            cookies.save()
            return False
        return True
    def checkFile(self, name):
    	name = os.path.join(self.dir,name)
    	if os.path.isfile(name) and os.stat(name).st_size > 0:
    		return True
    	return False



    def returnTitle(self,lang):
    	titulo = self.titulo[0:39] if len(self.titulo) > 40 else self.titulo
    	i = 1
    	assfilename = self.checkStr(titulo + " - " + self.episodio + " ["+lang+"].ass")
    	while True:
    		if self.checkFile(assfilename):
    			assfilename = self.checkStr(titulo + " - " + self.episodio + " ["+lang+"]("+str(i)+").ass")
    		else:
    			break
    		i += 1
    	return assfilename

    def saveSubs(self, subs, title):	
    	f = open(os.path.join(self.dir,title), 'w')
    	f.write(subs.encode('utf-8-sig'))
    	f.close()
    def checkStr(self, string):
        nopermitido = ["\\","/","?",":","*","\"","<",">","|"]
        return "".join(i for i in string if not i in nopermitido)
    def downloadSubs(self, url):
    	xmlSubs = self.downloadHtml(url)
    	formattedSubs = self.returnSubs(xmlSubs)
    	return formattedSubs
    def addError(self, error):
        self.errors.append(error)
        '''
        This method will create a logfile "Errorlog.txt".
        '''
    def getUrl(self, url):
    	self.errors = []
    	xml = self.downloadHtml(url)
    	subtitulos = BeautifulSoup(xml)
    	subtitulos = subtitulos.findAll(u"subtitle")
    	if not subtitulos:
    		self.addError("Error: Debes ser usuario premium para poder descargar este subtítulo.")
    		return False
    	subs_lang = []
    	subs_url = []
    	for i in subtitulos:
    		lang = re.match(r"\[(.*)\]", i.get(u"title"))
    		lang = lang.groups()
    		subs_lang.append(lang[0])
    		subs_url.append(i.get(u"link"))
    	return subs_lang,subs_url

    def downloadHtml(self, url, login = [False,None,None]):
        self.code = ""
        self.cookies()
        try:
            cookies = cookielib.MozillaCookieJar('cookies.txt')
            cookies.load() 
            opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(cookies))
            opener.addheaders =[('Referer', 'http://www.crunchyroll.com'),('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]
            if login[0]:
                data = {'formname' : 'RpcApiUser_Login', 'fail_url' : 'http://www.crunchyroll.com/login', 'name' : login[1], 'password' : login[2]}
                response = opener.open(url, urllib.urlencode(data))
                html = opener.open("http://www.crunchyroll.com")
                if re.search(login[1]+'(?i)',html.read()):
                    cookies.save()
                    return True
                else:
                    return False
            else:
                response = opener.open(url)
            html = response.read()
            cookies.save()
            return html
        except urllib2.HTTPError, e:
            self.addError("Crunchyroll: Error - %s."%e.code)
            self.code = e.code
        except urllib2.URLError, e:
            self.addError("Error: Comprueba tu conexión a internet.")
        except Exception,e:
            self.addError("Error: %s."%e.message)
    def login(self, user, password):
        self.errors = []
        login = self.downloadHtml("https://www.crunchyroll.com/?a=formhandler",[True, user, password])
        if login:
            return True
        return False
    def UrlCheck(self,url):
    	'''
    	Comprobamos que el enlace ingresado sea correcto. De serlo retornamos el enlace del xml de subtítulos del video.

    	'''
        self.errors = []
        if not url.replace(" ","") == "":
            if re.search(r"^(https://)",url):
                url = url.replace("https://","http://")
            elif re.search(r"^(http://)",url):pass
            else:
                url = "http://"+url
            url = url.replace(" ","")
        if re.match(r"^((?:http|https):\/\/)(w{3}\.)?(crunchyroll.com(?:\/[a-zA-Z\-]+){0,1}\/[a-zA-Z0-9\-\_]+\/)((?:[a-zA-Z0-9\-\_]+)\-[0-9]+)",url):
            url = re.match(r"^((?:http|https):\/\/)(w{3}\.)?(crunchyroll.com(?:\/[a-zA-Z\-]+){0,1}\/[a-zA-Z0-9\-\_]+\/)(?:(episode\-[0-9]+\-))?([a-zA-Z0-9\-\_]+\-)?([0-9]+)",url)
            url = url.groups()
            media_id = url[5]
            xml = "http://www.crunchyroll.com/xml/?req=RpcApiVideoPlayer_GetMediaMetadata&media_id="+media_id
            xml = self.downloadHtml(xml)
            soup = BeautifulSoup(xml)
            self.titulo = soup.find(u"series_title").text
            self.episodio = soup.find(u"episode_number").text
            media_id = soup.find(u"media_id").text
            if not media_id:
            	self.addError("Error: El enlace ciertamente es de Crunchyroll/Videos, pero parece no ser correcto o el episodio no está disponible.")
            	return False
            xml = 'http://www.crunchyroll.com/xml/?req=RpcApiSubtitle_GetListing&media_id=' + media_id
            return xml
        else:
            self.addError("Error: El enlace ingresado no es de Crunchyroll/Videos.")
            return False
if __name__ == '__main__':
    def PrintErrors(x):
        for i in x:
            print (i)

    def cls():
        os.system('cls' if os.name=='nt' else 'clear')
    def print2(string):
        if sys.version_info >= (3,):
            return string.encode('utf8').decode(sys.stdout.encoding)
        else:
            return string.encode('utf8')


    MenuTxt = '''Opciones:
1.- Descargar.
2.- Descargar paquete de enlaces.
3.- Login.
4.- Configuración.
5.- Acerca de..
0.- Salir.
>'''

    SettingsTxt = '''Editar configuración:
1.- Directorio de descargas.
2.- Lenguaje de preferencia.
0.- Cancelar.
>'''
#http://www.crunchyroll.com/naruto-shippuden/episode-425-the-infinite-dream-677385
    while True:
        Menu = True
        subs = CrunchySubs()
        while Menu:
            if subs.errors:
                PrintErrors(subs.errors)
                break
            option = str(raw_input(MenuTxt))
            if option =="1":
                url = subs.UrlCheck(str(raw_input("Introduce el enlace: ")))
                if not url:
                    PrintErrors(subs.errors)
                else:
                    sublist = subs.getUrl(url)
                    if not sublist:
                        PrintErrors(subs.errors)
                        break
                    else:
                    	while True:
                            listo = True
                            if subs.lang.lower() == "none":
                                while True:
                                    esta = False
                                    print("Lenguajes disponibles:")
                                    c = 1
                                    for i in sublist[0]:
                                        string = "%d) %s."%(c,i)
                                        try:
                                            print(string)
                                        except UnicodeEncodeError:
                                            print(print2(string))
                                        c += 1
                                    print (("%d) Todos los lenguajes.\n0) Cancelar"%(c)) if (len(sublist[0]) > 1) else "0) Cancelar.")
                                    seleccion = str(raw_input("> "))
                                    if seleccion == "0":
                                        cls()
                                        break
                                    else:
                                        for i in range(1,c+1):
                                            if str(i) == seleccion:
                                                esta = True
                                                break
                                        if not esta: 
                                            print (u"Opción invalida.") 
                                        else: 
                                            break
                            else:
                                esta = True
                                seleccion = -1
                            if esta:
                                if int(seleccion)-1 == len(sublist[0]) or subs.lang == "*":
                                    print("Descargando todos los idiomas disponibles.\n")
                                    for (lang,url) in izip(sublist[0],sublist[1]):
                                        titulo = subs.returnTitle(lang)
                                        string = "Descargando: %s"%(titulo)
                                        try:
                                            print (string)
                                        except UnicodeEncodeError:
                                            print(print2(string))
                                        subs.saveSubs(subs.downloadSubs(url), titulo)
                                else:
                                    if subs.lang in sublist[0]:
                                        titulo = subs.returnTitle(sublist[0][sublist[0].index(subs.lang)])
                                    elif subs.lang not in sublist[0] and not subs.lang.lower() == "none":
                                        string = "%s no se encuenta en la lista de subtítulos disponibles."%(subs.lang)
                                        try:
                                            print (string)
                                        except UnicodeEncodeError:
                                        	print(print2(string))
                                        listo = False
                                        subs.lang = "none"
                                    else:
                                        titulo = subs.returnTitle(sublist[0][int(seleccion)-1])
                                    if listo:
                                        string = "Descargando: %s"%(titulo)
                                        try:
                                            print (string)
                                        except UnicodeEncodeError:
                                            print(print2(string))
                                        if subs.lang in sublist[0]:
                                            subs.saveSubs(subs.downloadSubs(sublist[1][sublist[0].index(subs.lang)]), titulo)
                                        else:
                                            subs.saveSubs(subs.downloadSubs(sublist[1][int(seleccion)-1]), titulo)
                            if listo:break
	                        	


            elif option == "2":
                pass
            elif option == "3":
                cls()
                print("////////Login//////////")
                user = str(raw_input("Usuario: "))
                password = str(raw_input("Contraseña: "))
                if subs.login(user,password):
                    print("Te has logeado satisfactoriamente.\n\n") 
                else:
                    print("Usuario o contraseña incorrecta. Por favor verifica e intenta nuevamente.\n\n")
                sleep(3)
                cls()

            elif option == "4":
                cls()
                sett = True
                while True:
                    while sett:
                        cls()
                        option = str(raw_input(SettingsTxt))
                        if option == "1":
                            while True:
                                edit = False
                                settings = subs.LoadSettings()
                                string = "Directorio actual: %s"%(settings["dir"])
                                try:
                                	print (string)
                                except UnicodeEncodeError:
                                	print(print2(string))
                                option = str(raw_input("\n1.- Editar directorio. \n0.- Cancelar.\n>"))
                                if option == "1":
                                    dir = str(raw_input("Nuevo directorio: "))
                                    if dir.lower() == "default":
                                        edit = True
                                    elif subs.CheckDir(dir):
                                        edit = True
                                    else:
                                        print ("Directorio invalido. \"%s\" no existe."%dir)

                                    if edit:
                                        subs.config(
                                            directorio = dir, 
                                            lang = settings["lenguaje"]) 
                                        break

                                elif option == "0":
                                    break
                                else:
                                    print ("Opción invalida.")
                        elif option == "2":
                            while True:
                                settings = subs.LoadSettings()
                                ayuda = ''' 
None = Mostrará una lista de subtitulos disponibles de la cual podrás escoger.
* = Descargará todos los lenguajes disponibles.

Puedes ingresar un lenguaje por defecto, por ejemplo "Español". Este deberá coincidir con el lenguaje mostrado en la página de crunchyroll.
Algunos lenguajes de los que tengo conocimiento son:
-) English (US)
-) Español
-) Español (España)
-) Italiano
-) Português (Brasil)
-) Deutsch

                                '''
                                string = "Lenguaje: %s"%(settings["lenguaje"])
                                try:
                                    print(string)
                                except UnicodeEncodeError:
                                    print(print2(string))
                                option = str(raw_input("\n1.- Editar \n2.- Ayuda\n0.- Atras. \n> "))
                                if option == "1":
                                    lenguaje = str(raw_input("Ingresa el lenguaje: "))
                                    print (lenguaje.encode('string_escape'))
                                    subs.config(
                                        directorio = settings["dir"], 
                                        lang = lenguaje)
                                elif option == "2":
                                    print (ayuda)
                                elif option == "0":
                                    break
                                else:
                                    print ("Opción invalida.")
                        elif option == "0":
                            sett = False
                            break
                        else:
                            print ("Opción invalida.")
                    if not sett:
                        break
                cls()
            elif option == "5":
                print(about)
            elif option == "0":
                print("Gracias por usar CrunchySubs (:...")
                Menu = False
                sleep(3)
                break
            else:
                print ("Opción invalida.")
        if not Menu:
            break
