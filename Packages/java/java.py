import utils
import time
import threading
import shutil
import os
import sublime, re
import sublime_plugin
import os.path
from functools import cmp_to_key
from subprocess import PIPE, Popen

"""
reglas
	se tendra un archivo por clase, al lado de la misma clase
Conjunto de comandos que permiten lo siguiente:
	importar librerias (ctrl+shift+o)
	Completar funciones en java (ultimo nivel, funciones estaticas y funcioes de objetos)
	agregar una librerias que no existia en los paquetes
	limpiar (eliminar los archivos .class si ya no sirven)
Estructura:
	clases de java:
		directorio donde van a estar todas las clases de java
	archivos centrales:
		indice de clases
		indice de paquetes
	librerias
		paquetes con informacion de sus clases
Clases:
	la que extrae todos los json
	la que hace los indices de clases y de paquetes
	la que permite la importacion (depende de la que hace los indices de las clases y paquetes)
	la que permite la completacion (depende de las cadenas de importancion que tenga, toma el tipo mira si es la clase o el objeto y listo con eso tiene para entregarlo todo)
"""

ROOT="D:/sublime3/Data/librerias/java"
PATH_CLASSES=ROOT+"/clases"
PATH_JSON=ROOT+"/json"
PATH_LIBRERIAS=ROOT
PATH_INDEX_PACKAGES=os.path.join(ROOT, "packages.json")
PATH_INDEX_CLASSES=os.path.join(ROOT, "classes.json")

class JavaProcessClassesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ClassToJson().start()

class ClassToJson(threading.Thread):
	def run(self):
		self.i=0
		self.processFolder(PATH_CLASSES)

	def processFolder(self, ruta):
		for subruta in os.listdir(ruta):
			newruta=ruta+"/"+subruta
			if os.path.isdir(newruta):
				self.processFolder(newruta)
			elif subruta.strip().endswith(".class") and subruta.find("$")==-1:
				self.processClass(newruta)

	def processClass(self, ruta):
#		print("procesando : "+ruta)
#		time.sleep(0.1)
		self.i+=1
		sublime.status_message(str(self.i)+" clases procesadas")
		proceso=Popen("javap "+ruta, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
		salida=proceso.communicate()[0].decode("utf-8")
		superClases=re.findall("class\s+[\w.]+\s+extends\s+([\w.]+)", re.sub("\<[^>]+\>", "", salida), flags=re.IGNORECASE)
		if superClases:
#			print("tiene superclase y es : "+superClases[0])
			self.processClass(PATH_CLASSES+"/"+superClases[0].replace(".", "/"))
#		os.remove(ruta)
		json=self.getJson(salida)
		ruta=ruta.replace(PATH_CLASSES, PATH_JSON).strip()[:-5]+"json"
		if superClases:
			pathJsonSuperClass=PATH_JSON+"/"+superClases[0].replace(".", "/")+".json"
#			print("el path json es : "+pathJsonSuperClass)
			if os.path.exists(pathJsonSuperClass):
#				print("se van a mezclar")
				jsonSuperClass=utils.load_json(pathJsonSuperClass)
				json["clase"]=list(set(json["clase"]+jsonSuperClass["clase"]))
				json["object"]=list(set(json["object"]+jsonSuperClass["object"]))
		utils.save_json(ruta, json)

	def getJson(self, clase):
		"""
		toma el formato que emite javap y lo convierte en un objeto json
		diferencia entre atributos y metodos, y los metodos los divide en metodos de clase y metodo de objeto
		o={}
		o["clase"]=[]
		o["object"]=[]
		"""
		json={"clase":[], "object":[]}
		clase=clase.replace("interface ", "class ").replace("abstract ", " ").replace("final ", " ").replace(";", "").replace("public ", "").replace("private ", "").replace("protected ", "").replace("synchronized ", "").replace("volatile ", "")
		
		for linea in clase.splitlines():
			linea=linea.strip()
			static=linea.find("static ")!=-1
			linea=linea.replace("static ", "")
			linea=self.cleanLine(linea)

			if linea=="{" or linea=="}":continue

			regclass=re.findall(utils.REG_JAVA_CLASS, linea)
			regmethod=re.findall(utils.REG_JAVA_METHOD_SIGNATURE, linea)
			regattrib=re.findall(utils.REG_JAVA_ATTR_NAME, linea)
			
			if regclass:continue
			elif regmethod:
				if static:json["clase"].append(regmethod[0])
				else:json["object"].append(regmethod[0])
			elif regattrib:
				if static:json["clase"].append(regattrib[0])
				else:json["object"].append(regattrib[0])
		return json

	def cleanLine(self, linea):
#		return linea
		if linea.find("<")!=-1:
			newline=""
			i=0
			tomar=True
			for c in linea:
				if c=="<":
					i+=1
					tomar=False
				elif c==">":
					i-=1
					if i==0:tomar=True
				if tomar:
					newline+=c
			return newline
		else:return linea

class Java:
	def __init__(self):
		text=utils.get_text()
		declaraciones=re.findall("\<([A-Z][a-z]*)\>", text)
		text=re.sub("\<([A-Z][a-z]*)\>", "", text)
		text=text.replace("< ", "").replace(" >", "").replace("<=", "").replace(">=", "")
		#text=self.clean(text)
		text=text.replace("abstract ", " ").replace("final ", " ").replace("public ", "").replace("private ", "").replace("protected ", "").replace("synchronized ", "").replace("volatile ", "").replace("class ", "public class").replace("static ", "").replace("< ", "").replace("> ", "").replace("<=", "").replace(">=", "")
		tipos=[]
		variables={}
		#print("jojo")
		#print("el texto es : "+text)
		#print(re.findall("\n[\t ]*([A-Z][\w]*[ ]+[\w_]+)", text))
		declaraciones+=re.findall("\n[\t ]*([A-Z][\w]*[ ]+[\w_]+)", text) + re.findall("[^\w]([A-Z][\w]*)\.", text) + re.findall("\(\s*([A-Z][\w]*[ ]+[\w_]+)", text) + re.findall(",\s*([A-Z][\w]*[ ]+[\w_]+)", text) + re.findall("\n[ \t]*@([A-Z][\w]*)", text) + re.findall("new ([A-Z][\w]*)", text) + re.findall("implements ([A-Z][\w]*)", text) + re.findall("extends ([A-Z][\w]*)", text) + re.findall("throws ([A-Z][\w]*)", text) +re.findall("\<([A-Z][\w]*)\>", text)
		#print(declaraciones)
		#text=self.clean(text)

		this=re.findall("extends ([A-Z][\w]*)", text)
		if this:declaraciones+=[this[0]+" this"]
		#print(declaraciones)
		for declaracion in declaraciones:
			declaracion=declaracion.strip()
			pos=declaracion.find(" ")
			if pos!=-1:
				tipo=declaracion[:pos]
				variable=declaracion[pos+1:]
				variables[variable]=tipo
				tipos.append(tipo)
			else:tipos.append(declaracion)
		newtipos=[]
		tipos=list(set(tipos))
		for tipo in tipos:
			if re.findall("import [\w.]+\.%s;"%(tipo), text):
				#print("ya esta exportado******"+tipo)
				continue
			newtipos.append(tipo)
		tipos=newtipos
		self.tipos=tipos
		self.variables=variables
		#print(self.variables)
	
	def clean(self, text):
		newtext=""
		i=0
		while i<len(text):
			if text[i]=='"':
				i+=1
				while text[i]!='"':i+=1
				i+=1

			"""if text[i]=='<':
				i+=1
				while text[i]!='>':i+=1
				i+=1"""

			newtext+=text[i]
			i+=1
		return newtext

	def get_tipos(self):
		return self.tipos

	def get_variables(self):
		return self.variables

class ImportJavaCommand(sublime_plugin.TextCommand):
	"""
		obtiene todo 
		Class some
		Class.
		(Class metodo)
	"""
	def run(self, edit):
		print("va a importar")
		window=sublime.active_window()
		view=window.active_view()
		self.window=sublime.active_window()
		self.view=self.window.active_view()
		java=Java()
		tipos=java.get_tipos()
		self.packages=utils.load_json(PATH_INDEX_PACKAGES)
		projectFiles=utils.get_files({"ext":"java"})
		projectFiles=[x.replace("/", ".").replace("\\", ".") for x in projectFiles]
		projectFiles=[x[x.rfind(".java.")+6:x.rfind(".")] for x in projectFiles]
		
		##print(projectFiles)
		viewPackage=view.substr(view.find(utils.REG_JAVA_PACKAGE, 0))
		viewPackage=viewPackage.replace("package ", "").replace(";", "")

		for projectFile in projectFiles:
			className=projectFile[projectFile.rfind(".")+1:]
			packageClass=projectFile[:projectFile.rfind(".")]
			if packageClass==viewPackage:continue
			if self.packages.get(className)==None:
				self.packages[className]=[]
			self.packages[className].append(packageClass)
		
		self.clases=list(set(tipos))
		##print(self.clases)
		self.i=0
		self.importar(None)

	def importar(self, paquete):
		self.z=0
		if paquete!=None:self.importarPaquete(paquete)
		if self.i>=len(self.clases):return
		self.clase=self.clases[self.i]
		##print("la nueva clase seleccionada es : "+self.clase)
		##print(self.packages.get(self.clase))

		self.i+=1
		if not self.packages.get(self.clase):
			##print("no se encontroo nada para : "+self.clase)
			self.importar(None)
		else:
			##print(self.packages[self.clase])
			self.selList=self.packages[self.clase]
			if "java.lang" in self.selList:
				self.importar(None)
				return
			self.window.show_input_panel("select import",self.selList[self.z]+"."+self.clase, self.importar, None, self.cancelar)

	def cancelar(self):
		self.z+=1
		if(self.z<len(self.selList)):
			self.window.show_input_panel("select import",self.selList[self.z]+"."+self.clase, self.importar, None, self.cancelar)
		else:
			self.importar(None)

	def importarPaquete(self, paquete):
#		view.find(, unicodearg2, longarg3 [, intarg4])
		punto=self.view.find("\n?[ \t]*package[ ]+[\w.]+;", 0).b
		inicio="\n"
		fin=""
		if punto==-1:
			punto=0
			inicio=fin
			fin="\n"
		paquete=inicio+"import "+paquete+";"+fin
		self.view.run_command("insertar", {"text":paquete, "point":punto})

class BuildJavaIndexPackageCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		BuildIndex().start()

class BuildIndex(threading.Thread):
	def run(self):
		self.packages={}
		self.explore(PATH_JSON)
		utils.save_json(PATH_INDEX_PACKAGES, self.packages)
		utils.save_json(PATH_INDEX_CLASSES, list(self.packages.keys()))

	def explore(self, path):
		package=path.replace(PATH_JSON, "").replace("/", ".").replace("\\", ".")[1:]
		for subpath in os.listdir(path):
			newpath=os.path.join(path, subpath)
			if os.path.isdir(newpath):self.explore(newpath)
			else: 
				clase=subpath[:subpath.rfind(".")]
				if self.packages.get(clase)!=None:self.packages[clase].append(package)
				else:self.packages[clase]=[package]

class JavaCompletionListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if utils.get_language() != "java":return
		ultimo=utils.get_last_character()
		if ultimo=="." and utils.get_language()=="java":
			window=sublime.active_window()
			view=window.active_view()
			word=utils.get_word(-1)
			variables=Java().get_variables()
			tipo=word
			static=True
			if variables.get(word):
				tipo=variables[word]
				static=False

			package=re.findall("import ([\w.]+\.%s);"%tipo, utils.get_text())
			
			if not package:
				posibleRuta=os.path.join(PATH_JSON, "java", "lang", tipo+".json")
				if os.path.exists(posibleRuta):
					package=["java.lang."+tipo]

			if package:
				package=package[0]
				clase=self.get_project_class(package)
				if clase:
					return utils.get_completion_list(clase["members"])
				ruta=package.replace(".", os.sep)+".json"
				ruta=os.path.join(PATH_JSON, ruta)
				print("ya se determino")
				objeto=utils.load_json(ruta)
				miembros="clase" if static else "object"
				return utils.get_completion_list(objeto[miembros])

	def get_project_class(self, package):
		clases=utils.get_files_java()
		for clase in clases:
			clase=self.get_java_members(clase)
			if clase==None:continue
			if clase["package"]==package:
				return clase

	def get_java_members(self, ruta):
	    strClass=open(ruta).read()
	    strClass=re.sub("\<[^>]*\>", "", strClass)
	    strClass=strClass.replace(" interface ", " class ").replace(" enum ", " class ")
	    #limpiar la clase aqui
	    package=re.findall(utils.REG_JAVA_PACKAGE,strClass)
	    members=re.findall(utils.REG_JAVA_METHOD_COMPLETION,strClass)
	    className=re.findall(utils.REG_JAVA_CLASS, strClass)
	    if package:package=package[0]+"."
	    else:package=""
	    try:
	        clase={}
	        clase["package"]=package+className[0]
	        methods=[]
	        for member in members:
	            methods.append(member[1])
	        clase["members"]=methods
	        return clase
	    except:return None

class JavaCleanClassesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.cleanFolder(PATH_CLASSES)
	def cleanFolder(self, ruta):
		for subruta in os.listdir(ruta):
			newruta=os.path.join(ruta, subruta)
			if os.path.isdir(newruta):self.cleanFolder(newruta)
			elif subruta.endswith(".class") and subruta.find("$")!=-1 or not subruta.endswith(".class"):os.remove(newruta)

class JavaCompletionClassListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if utils.get_language()!="java":return
		line=utils.get_line()
		line=line.lstrip()
		if line.startswith("@"):line=line[1:]
		if len(line)==1 and line.isupper() or line.endswith("new "):return utils.get_completion_list(utils.load_json(PATH_INDEX_CLASSES), "(Class)")


class JavaComentarClaseCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=sublime.active_window().active_view()
		if not view.scope_name(0).startswith("source.java "):return
		lineas=view.lines(sublime.Region(0, view.size()))
		contador=0
		vieneComentado=False
		listDoc=[]
		for regionLinea in lineas:
			linea=self.limpiar(view.substr(regionLinea))
			if not vieneComentado:
				metodo=re.findall("\s*([\w.<>]+)\s+([\w$]+\([^)]*\))", linea)				
				if metodo!=None and len(metodo)==1:
					documentacion="\n\t/**\n\t* TODO\n\t*\n\t"
					metodo=metodo[0]
					retorno=metodo[0]
					if retorno=="new" or retorno=="else" or retorno=="return":continue
					metodo=metodo[1]
					parametros=self.quitarSimbolosDiamantes(metodo[metodo.find("(")+1:-1])
					tipo=""
					nombre=""
					for parametro in parametros.split(","):
						parametro=parametro.strip().split(" ")
						tipo=parametro[0]
						if tipo.strip() and len(parametro)>1:
							nombre=parametro[1]
							documentacion+="* @param %s TODO\n\t"%(nombre)
					if retorno!="void" and retorno!="private" and retorno!="public" and retorno!="protected":
						documentacion+="* @return %s TODO\n\t"%(retorno)

					contador+=1
					documentacion+="**/\n"
					listDoc.append((regionLinea.a, documentacion))					

			if linea.strip() and not linea.strip().startswith("@"):
				vieneComentado=linea.endswith("*/")
		
		if listDoc!=None and len(listDoc)>0:
			for doc in reversed(listDoc):
				view.run_command("insertar", {"text":doc[1], "point":doc[0]})
		##print("Tiene un total de "+str(contador)+"metodos")
		if contador>0:
			sublime.status_message("se insertaron "+str(contador)+" comentarios")

	def quitarSimbolosDiamantes(self, parametros):
		lenParametros=len(parametros)
		params=""
		contadorLess=0
		i=0
		while i<lenParametros:
			contadorLess=0
			if parametros[i]=='<':
				contadorLess+=1
				i+=1
				while contadorLess>0 and i<lenParametros:
					if parametros[i]=='>':
						contadorLess-=1
					elif parametros[i]=='<':
						contadorLess+=1
					i+=1
			params+=parametros[i]
			i+=1
		return params

	def limpiar(self, linea):
		return re.sub('"[^"]*"', "", linea)

class JavaCheckDocCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.contador=0
		window=sublime.active_window()
		if window.folders()!=None and len(window.folders())>0:
			folder=window.folders()[0]
			self.javaFiles(folder)
			#print("El total de metodos por documentar es : "+str(self.contador))
				
	def javaFiles(self, path):
		if os.path.isdir(path):
			for subpath in os.listdir(path):
				self.javaFiles(os.path.join(path, subpath))
		else:
			if path.endswith(".java"):
				self.checkDoc(path)

	def checkDoc(self, path):
		javaClass=os.path.basename(path)
		lines=open(path).readlines()
		vieneComentado=False

		for linea in lines:
			linea=self.limpiar(linea)
			if not vieneComentado:
				metodo=re.findall("\s*([\w.<>]+)\s+([\w$]+\([^)]*\))", linea)				
				if metodo!=None and len(metodo)==1:
					metodo=metodo[0]
					retorno=metodo[0]
					if retorno=="new" or retorno=="else" or retorno=="return":continue
					metodo=metodo[1].strip()
					if metodo.startswith("onEvent("):continue
					self.contador+=1
					#print(javaClass+":"+metodo)
		
			if linea.strip() and not linea.strip().startswith("@"):
				vieneComentado=linea.strip().endswith("*/")
	
	def limpiar(self, linea):
		return re.sub('"[^"]*"', "", linea)

server_folder_deploy={
	"jboss": os.path.join(os.environ["JBOSS_AS_HOME"], "standalone", "tmp", "vfs"),
	"weblogic":"D:/weblogic12/user_projects/domains/mydomain/servers/myserver/tmp"
}

class XhtmlListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if utils.get_language()!="jsf":return
		window=sublime.active_window()
		folders=window.folders()
		if not folders:return

		folderProyecto=folders[0]
		if not os.path.exists(os.path.join(folderProyecto, "pom.xml")):return
		server=utils.get_preference("server")
		
		folderDeploy=server_folder_deploy[server]
		self.folderDeploy=folderDeploy

		filepath=utils.get_filepath()
		self.filepath=filepath
		
		if server=="weblogic":
			threading.Thread(target=self.reemplazarTodos).start()
			return

		if server!="jboss":
			folderDeploy=folderDeploy+os.sep+os.listdir(folderDeploy)[0]
			self.folderDeploy=folderDeploy

			folderDeploy=os.path.normpath(folderDeploy)
			print("the folder deploy is : "+folderDeploy)
		nombreProyecto=filepath.replace(folderProyecto+os.sep, "")
		#print("el nombre del proyceto es : "+nombreProyecto)
		nombreProyecto=nombreProyecto[:nombreProyecto.find(os.sep)]
		#print("el nuevo nombre del proyecto es: "+nombreProyecto)
		#print("el filepath es : "+filepath)
		#print("el folderDeploy es : "+folderDeploy)
		fileLocation=filepath[filepath.find("webapp"+os.sep)+7:]
		#print("el fileLocation is: "+fileLocation)
		print(server)
		

		print("el nombre del proyecto es : "+nombreProyecto)
		folders=os.listdir(folderDeploy)

		folders=[os.path.join(folderDeploy, x) for x in folders]
		
		def comparador(x):return os.path.getmtime(x)

		folders=sorted(folders, key=comparador, reverse=True)
		print(folders)
		for folderS in folders:
			for folder in os.listdir(folderS):
				print(folder)
				if folder.find(nombreProyecto)!=-1:
					fileLocation=folderS+os.sep+folder+os.sep+fileLocation
					print("la nueva localizacion del archivo es : "+fileLocation)
					utils.file_write(fileLocation, utils.file_read(filepath))
					#print("escrito con exito")
					return
				else:print("no")

	def reemplazarTodos(self):
		print(self.folderDeploy)
		self.nombreArchivo=os.path.basename(self.filepath)
		self.nombreCarpeta=os.path.basename(os.path.dirname(self.filepath))
#		self.lista=[]
		self.recorrerCarpeta(self.folderDeploy)
#		print(self.lista)
	
	def recorrerCarpeta(self, archivo):
#		print(archivo)
		if os.path.isdir(archivo):
			for ruta in os.listdir(archivo):
				self.recorrerCarpeta(archivo+"/"+ruta)
		elif os.path.basename(archivo)==self.nombreArchivo and os.path.basename(os.path.dirname(archivo))==self.nombreCarpeta:
			utils.file_write(archivo, utils.file_read(self.filepath))

