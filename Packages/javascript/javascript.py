import os
import sublime
import sublime_plugin
import os.path
import re

class ArchivoJavascript:
	def diseccionar(variables=False, librerias=False, texto=None):
		d={}
		if texto==None:texto=ArchivoJavascript.getTextoLimpio()
		patronVariables="\s*([\w$][\w$\d]*)\s*=\s*.+"
		
		if librerias:variables=True

		if variables:
			d["variables"]=re.findall(patronVariables,texto)
			if d["variables"]:d["variables"]=set(d["variables"])
			else:d["variables"]=set()
		if librerias:
			d["librerias"]=re.findall(patronLibreria, texto)
			if d["librerias"]:d["librerias"]=set(d["librerias"])-d["variables"]
			else:d["librerias"]=set()

		return d
		
	def getTipo(variable, texto=None):
		if texto==None:texto=ArchivoJavascript.getTextoLimpio()
		tipo=re.findall("%s\s*=\s*(.+)"%variable, texto)
		if not tipo:return
		tipo=tipo[0].strip()
		if tipo.isalnum():
			return ArchivoJavascript.getTipo(tipo)

	def getMiembros(tipo, texto=None):
		if texto==None:texto=ArchivoJavascript.getTextoLimpio()
		miembros=re.findall("\b%s\.([\w]+\([^)]*\))"%tipo, texto)
		if miembros:return set(miembros)
		else: return set()

	def getTextoLimpio(todo=True):
		return ArchivoJavascript.limpiarTexto(ArchivoJavascript.getTexto(todo))

	def limpiarTexto(texto):
		texto="\n"+texto
		texto=re.sub("'[^']*'", '""', texto, flags=re.DOTALL)
		texto=re.sub('"[^"]*"', '""', texto, flags=re.DOTALL)
		texto=re.sub("/**[^*]**/", repl, texto, flags=re.DOTALL)
		texto=re.sub("\n\s*//[^\n]+\n", "\n", texto)
		texto=re.sub("=\s*new\s+", "=", texto)
		texto=re.sub('=\s*""', '=String()', texto)
		texto=re.sub("=\s*/[^/]*/", "=RegExp()", texto, flags=re.DOTALL)
		texto=re.sub("=\s*\[[^\]]*\]", "=Array()", texto, flags=re.DOTALL)
		texto=re.sub("=\s*[\d.]", '=Number()', texto)
		texto=re.sub("=\s*\{[^}]*\}", "=Object()", texto, flags=re.DOTALL)
		texto=re.sub("}\s*\n", "\n{", texto)
		return texto

	def getTexto(todo=True):
		view=sublime.active_window().active_view()
		if todo:
			return view.substr(sublime.Region(0, view.size()))
		else:
			return view.substr(sublime.Region(0, view.sel()[0].a))

	def getLinea(toda=True):
		view=sublime.active_window().active_view()
		punto=view.sel()[0].a
		if toda:
			return view.substr(sublime.Region(view.line(punto), punto))
		else:
			return view.substr(view.line(punto))

	def getPalabra():
		palabra=re.findall("([\w]+)\.?$", ArchivoJavascript.getLinea(toda=False))
		if palabra:palabra=palabra[0]
		return palabra
			
	def cargarArchivo():
		d=sublime.decode_value(open(sublime.packages_path()+os.sep+"javascript"+os.sep+"javascript.json").read())
		pass
	
	def guardarFunciones():
		texto=ArchivoJavascript.getTextoLimpio()
		js=ArchivoJavascript.cargarArchivo()
		d=ArchivoJavascript.diseccionar(librerias=True, variables=True, texto=texto)
		for libreria in d["librerias"]:
			if js["librerias"].get("libreria"):
				js[librerias][libreria]=list(set(js["librerias"][libreria])|ArchivoJavascript.getMiembros(libreria))
			else:
				js["librerias"][libreria]=ArchivoJavascript.getMiembros(libreria, texto=texto)
		for variable in d["variables"]:
			tipo=ArchivoJavascript.getTipo(variable, texto=texto)
			if js["clases"].get(tipo)==None:js["clases"][tipo]=[]
			js["clases"][clase]=list(set(js["clases"][clase]+ArchivoJavascript.getMiembros(variable)))
		
		archivo=open(sublime.packages_path()+os.sep+"javascript"+os.sep+"javascript.json","w")
		archivo.write(sublime.encode_value(js, True))
		archivo.close()

