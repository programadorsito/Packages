import os
import sublime
import sublime_plugin
from subprocess import PIPE, Popen
import os.path
import re

class RutasPython:
	def python():
		return os.path.join(sublime.packages_path(), "..", "python"+os.sep+"completion"+os.sep)
	def modulos():
		return RutasPython.python()+"modulos.json"
	def funciones():
		return RutasPython.python()+"funciones.json"
	def modulo(name):
		return RutasPython.python()+"librerias"+os.sep+name+".json"
	def clase(name):
		return RutasPython.python()+"clases"+os.sep+name+".json"
	def mapa():
		return RutasPython.python()+"mapa.json"
	def donde(donde, name):
		return RutasPython.python()+donde+os.sep+name+".json"
	def importar():
		return RutasPython.python()+"importar.txt"
	def temporal():
		return RutasPython.python()+"temporal.txt"

class Identificadores:
	"""Toma las variables y trata de identificar sus tipos"""
	def __init__(self):
		self.variables={}
		for variable in re.findall("([\w$]+)\s*=(.+)", ArchivoPython.getTextoLimpio()):
			self.variables[variable[0]]=self.tipo(variable[1])
	
	def tipo(self, tipo):
		tipo=tipo.strip()
		t=self.tipoBasico(tipo)
		if t:return t
		t=self.traducir(tipo)
		if t:return t

	def tipoBasico(self, tipo):
		if tipo.startswith('"'):return "str"
		elif tipo.startswith("0"):return "int"
		elif tipo.startswith("["):return "list"
		elif tipo.startswith("{"):return "dict"
		elif tipo.startswith("set()"):return "set"
		elif tipo.startswith("()"):return "tuple"
		elif tipo.startswith("open()"):return "file"

	def traducir(self, tipo):
		if tipo.find("(")!=-1:
			v=""
			if tipo.find(".")!=-1:
				v=tipo[:tipo.rfind(".")].strip()
				if self.variables.get(v):v=self.variables[v]
				v+="."
			funcion=tipo[tipo.rfind(".")+1:tipo.find("(")] if tipo.find(".")!=-1 else tipo[:tipo.find("(")]
			tipo=v+funcion
		tipos=sublime.decode_value(open(RutasPython.mapa()).read())
		if tipos.get(tipo):		
			return tipos[tipo]
		else:
			return tipo

	def getVariables(self):
		return self.variables

class pythonCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.scope_name(0).find("source.python ")!=-1:
			linea=view.substr(view.line(view.sel()[0].a)).strip()
			if not linea:return self.allFunctions()
			if linea.strip().startswith("import") or (len(linea)==1 and linea.islower()):return self.librerias()
			if not view.substr(sublime.Region(view.sel()[0].a-1, view.sel()[0].a))==".":return self.librerias()
			identificador=view.substr(view.word(view.sel()[0].a-1)).strip()
			variables=Identificadores().getVariables()
			if identificador in variables.keys():
				return self.modulo(variables[identificador].strip(), donde="clases")
			modulo=view.substr(sublime.Region(view.line(view.sel()[0].a).a, view.sel()[0].a)).strip()

			modulo=re.findall("([\w\d$.]+)\.$", modulo)[0]
			#frones=re.findall("from\s+([\w.]+)\s+import\s+(.+)", ArchivoPython.getTexto())
			print(modulo)

			"""for f in frones:
				if f[1].find(" "+modulo)!=-1 or f[1].find(","+modulo)!=-1 or f[1]==modulo:
					modulo=f[0]+"."+modulo
					modulo=modulo.strip()"""

			return self.modulo(modulo)

	def librerias(self):
		return [(m+"\t•", m) for m in ArchivoPython.cargarModulos()]

	def allFunctions(self):
		"""retorna todas las funciones"""
		modulos=sublime.decode_value(open(RutasPython.funciones()).read())
		lista=[]
		for modulo in modulos:
			lista+=[ (funcion+"\t•"+modulo, self.ponerCursor(modulo+"."+funcion)) for funcion in modulos[modulo]]
		return sorted(lista)

	def modulo(self, modulo, donde="librerias"):
		"""retorna la informacion de ese modulo"""
		if donde=="clases":
			clases=ArchivoPython.getClases()
			
			if modulo in clases.keys():
				print("sie sta")
				modulo=clases[modulo]
				print(modulo)
				return [(f+"\t•", self.ponerCursor(f)) for f in modulo]		
		
		pathFile=RutasPython.donde(donde,modulo)
		if not os.path.exists(pathFile):
			return
		modulo=sublime.decode_value(open(pathFile).read())
		return [(f+"\t•", self.ponerCursor(f)) for f in modulo]

	def ponerCursor(self, linea):
		"""pone el cursos para poder insertar el snippet"""
		linea=linea.replace(",", "},${:").replace("(", "(${:").replace(")", "})")
		otra=""
		contador=1
		for c in linea:
			if c==":":
				otra+=str(contador)
				contador+=1
			otra+=c
		return otra

class ArchivoPython:
	def diseccionar(modulosFaltantes=False,modulosTotales=False,modulosPosibles=False, modulosImportados=False, dModulosImportados=False, clases=False, dClases=False, funciones=False, variables=False, texto=None):
		if dModulosImportados:modulosImportados=True
		if dClases:clases=True
		view=sublime.active_window().active_view()
		if modulosFaltantes:modulosTotales=modulosPosibles=modulosImportados=True
		patronVariables="([\w\d$]+) *="
		patronModulosImportados="import\s+([a-z][\w\d.]+)"
		patronmodulosPosibles="[\w\d$]+\.[\w\d$.]+"
		patronClases="class ([\w]+)\(?[\w. ]*\)?:"
		patronMetodos="def ([\w]+\([^)]*\))"
		patronAtributos="self.[\w]+"
		d={}
		if not texto:
			texto=view.substr(sublime.Region(0, view.size()))
		texto=ArchivoPython.limpiarTexto(texto)
		if modulosImportados:
			d["modulosImportados"]=set([m.strip() for m in re.findall(patronModulosImportados, texto)])
		if dModulosImportados:
			d["dModulosImportados"]={}
			for m in d["modulosImportados"]:
				d["dModulosImportados"][m]=re.findall(m+"\.([\w][\w\d]*\([^)]*\))",texto)

		if variables:d["variables"]=set(re.findall(patronVariables, texto))
		if modulosPosibles:d["modulosPosibles"]=set([modulo[:modulo.rfind(".")].strip() for modulo in re.findall(patronmodulosPosibles, texto)])
		if modulosTotales:d["modulosTotales"]=set(ArchivoPython.cargarModulos())
		if modulosFaltantes:d["modulosFaltantes"]=(d["modulosTotales"]&d["modulosPosibles"])-d["modulosImportados"]
		if clases:d["clases"]=set()

		return d

	def getTexto():
		view=sublime.active_window().active_view()
		return view.substr(sublime.Region(0, view.sel()[0].a))

	def getTextoLimpio():
		return ArchivoPython.limpiarTexto(ArchivoPython.getTexto())

	def getTextoCompletoLimpio():
		return ArchivoPython.limpiarTexto(ArchivoPython.getTextoCompleto())

	def getTextoCompleto():
		view=sublime.active_window().active_view()
		return view.substr(sublime.Region(0, view.size()))

	def limpiarTexto(texto):
		texto=re.sub("^#.", "", texto)
		texto=re.sub('"""[^"]+"""', "", texto)
		texto=re.sub('"[^"]*"', "", texto)
		texto=re.sub("\{[^:}]+\}", "set()", texto)
		texto=re.sub("\{[^}]+\}", "{}", texto)
		texto=re.sub("\[[^\]]+\]", "[]", texto)
		texto=re.sub("[\d][\d.]*", "0", texto)
		texto=re.sub("\([^)]+\)", "()", texto)
		text=""
		que={}
		for l in texto.splitlines():
			l=l.strip()
			if re.match("^import\s*[\w.]+\s*,\s*[\w.]+", l):
				imports=re.findall("^import\s*([\w. ,]+)", l)[0].split(",")
				l=""
				for i in imports:l+="import "+i.strip()+"\n"
			elif re.match("^\s*[\w]+\s*,[\w ,]+\s*=.", l):
				variables, valores=re.findall("([\w\d, ]+)\s*=\s*(.+)", l)[0]
				variables=variables.split(",")
				valores=valores.split(",")
				l=""
				for i in range(len(variables)):l+=variables[i]+"="+valores[i]+"\n"
			"""elif re.match("^\s*from\s+[\w.]+\s+import\s+.", l):
				m=l[l.find("from")+4:l.find("import")].strip()
				que[m]=[m.strip() for m in l[l.find("import")+6:].split(",")]
				l="import "+m"""
			text+=l+"\n"

		
		for q in que:
			for p in que[q]:
				text=text.replace(p+".", "%s.%s."%(q,p))
		
		return text
		
	def getClases():
		d={}
		clase=""
		for l in re.sub("\(\s*self\s*,?", "(", ArchivoPython.getTexto()).splitlines():
			if l.strip().startswith("class "):
				clase=re.findall("class ([\w]+)", l)[0]
				d[clase]=""
			elif clase:
				d[clase]+=l+"\n"
		for clase in d:
			texto=d[clase]
			d[clase]=re.findall("def\s+([^:]+):", texto)+re.findall("self\.([\w]+)", texto)
		return d

	def cargarModulo(modulo):
		return sublime.decode_value(open(RutasPython.modulo(modulo)).read())

	def guardarModulo(nombre, miembros):
		fModulo=open(RutasPython.modulo(nombre), "w")
		fModulo.write(sublime.encode_value(miembros, True))
		fModulo.close()
	
	def agregarAModulo(nombre, miembros):
#		print("agregando a "+nombre)
#		print(miembros)
		modulo=ArchivoPython.cargarModulo(nombre)
		lista=[f[:f.find("(")] if f.find("(")!=-1 else f for f in modulo]
		for miembro in miembros:
			nombreMiembro=miembro[:miembro.find("(")] if miembro.find("(")!=-1 else miembro
			if not nombreMiembro in lista:
				lista.append(nombreMiembro)
				modulo.append(miembro[:miembro.find("(")+1]+" ,"*miembro.count(",")+" )")
#		print("agregando a "+nombre)
#		print(modulo)
		ArchivoPython.guardarModulo(nombre, modulo)

	def cargarModulos():
		return sublime.decode_value(open(RutasPython.modulos()).read())
	
	def agregarModulo(modulo):
		conjunto=set(ArchivoPython.cargarModulos())
		conjunto.add(modulo)
		ArchivoPython.guardarModulos(list(conjunto))

	def guardarModulos(modulos):
		fileModules=open(RutasPython.modulos(), "w")
		fileModules.write(sublime.encode_value(modulos, True))
		fileModules.close()

	def cargarFunciones():
		return sublime.decode_value(open(RutasPython.funciones()).read())
	
	def guardarFunciones(funciones):
		fileModules=open(RutasPython.funciones(), "w")
		fileModules.write(sublime.encode_value(funciones, True))
		fileModules.close()
		
	def cargarClase(clase):
		pass

	def guardarClase(nombre, miembros):
		fModulo=open(RutasPython.clase(nombre), "w")
		fModulo.write(sublime.encode_value(miembros, True))
		fModulo.close()

class ImportarLibreriasPythonCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=sublime.active_window().active_view()
		for modulo in ArchivoPython.diseccionar(modulosFaltantes=True)["modulosFaltantes"]:view.insert(edit, 0, "import "+modulo+"\n")
		
class AgregarLibreriaPythonCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		sublime.active_window().show_input_panel("nombre del modulo", "", self.agregar, None, None)
		
	def limpiarParentesis(self, ayuda):
		ayudita=""
		contador=0
		for l in ayuda.splitlines():
			for c in l:
				if c=="(":
					contador+=1
					if contador==1:
						ayudita+=c
					continue
				elif c==")":
					contador-=1
					if contador==0:
						ayudita+=c
					continue
				ayudita+=c
			ayudita+="\n"
		return ayudita
	
	def prepararTemporal(self, modulo):
		fImportar=open(RutasPython.importar())
		texto=fImportar.read()
		fImportar.close()

		texto=re.sub("^import [\w.]+", "import %s"%modulo, texto)
		texto=re.sub("help\([\w.]+\)", "help(%s)"%modulo, texto)
		
		fImportar=open(RutasPython.importar(), "w")
		fImportar.write(texto)
		fImportar.close()
		os.chdir(RutasPython.python())
		os.system('importar.bat')

	def agregar(self, modulo):
		ArchivoPython.agregarModulo(modulo)
		self.prepararTemporal(modulo)
		#ayuda=self.limpiarParentesis(open(RutasPython.temporal()).read())
		ayuda=open(RutasPython.temporal()).read()

		modulo={"name":modulo, "FUNCTIONS":"", "DATA":"", "CLASSES":"", "PACKAGE CONTENTS":""}
		nombre=""
		for l in ayuda.splitlines():
			l=l.strip()
			if l.isupper() and modulo.get(l)!=None:
				nombre=l
				modulo[nombre]=""
			elif nombre:
				modulo[nombre]+=l+"\n"

		funciones=modulo["FUNCTIONS"]
		modulo["FUNCTIONS"]=re.findall("\n\s*([\w]+\([^)]*\))", funciones)
		modulo["FUNCTIONS"]+=re.findall("^\s*([\w]+\([^)]*\))", funciones)
		modulo["FUNCTIONS"]+=re.findall("\n\s*[\w]+\.([\w]+\([^)]*\))", funciones)
		modulo["FUNCTIONS"]+=re.findall("\n\s*%s\.([\w]+\([^)]*\))"%modulo["name"], funciones)
		mapa={}
		for f in modulo["FUNCTIONS"]:mapa[f[:f.find("(")]]=f
		modulo["FUNCTIONS"]=list(mapa.values())
		modulo["DATA"]=re.findall("\n\s*([a-z][\w]*)\s*=", modulo["DATA"], re.I)
		
		clases=modulo["CLASSES"]
		nombre=""
		modulo["CLASSES"]={}
		
		for l in clases.splitlines():
			clase=re.findall("^\s*class ([\w]+)", l)
			if clase:
				nombre=clase[0]
				modulo["CLASSES"][nombre]=""
			elif nombre:
				modulo["CLASSES"][nombre]+=l+"\n"
		
		
		modulo["PACKAGE CONTENTS"]=re.findall("\n\s*([a-z.]+)\s*",modulo["PACKAGE CONTENTS"])
		miembrosModulo=modulo["FUNCTIONS"]+modulo["DATA"]+list(modulo["CLASSES"].keys())+modulo["PACKAGE CONTENTS"]
		
		ArchivoPython.guardarModulo(modulo["name"], miembrosModulo)
		funciones=ArchivoPython.cargarFunciones()
		funciones[modulo["name"]]=miembrosModulo
		ArchivoPython.guardarFunciones(funciones)
		
		for clase in modulo["CLASSES"]:
			funciones=modulo["CLASSES"][clase]
			modulo["CLASSES"][clase]=re.findall("\n\s*\|?\s*([\w]+\([^)]*\))", funciones)
			modulo["CLASSES"][clase]+=re.findall("\n\s*\|?\s*[a-z]+\.([\w]+\([^)]*\))", funciones)
			mapa={}
			for f in modulo["CLASSES"][clase]:mapa[f[:f.find("(")]]=f
			modulo["CLASSES"][clase]=list(mapa.values())
			ArchivoPython.guardarClase(modulo["name"]+"."+clase, modulo["CLASSES"][clase])
		
class CompletadoInteligentePythonCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		d=ArchivoPython.diseccionar(dModulosImportados=True)		
		for modulo in d["dModulosImportados"]:
			if not modulo in ArchivoPython.cargarModulos():
				ArchivoPython.agregarModulo(modulo)
				open(RutasPython.modulo(modulo), "w").write("[]")
			listaFunciones=d["dModulosImportados"][modulo]
			ArchivoPython.agregarAModulo(modulo, listaFunciones)

class PythonListener(sublime_plugin.EventListener):
	def on_pre_save(self, view):
		if view.scope_name(0).startswith("source.python "):
#			view.run_command("importar_librerias_python")
			view.run_command("completado_inteligente_python")