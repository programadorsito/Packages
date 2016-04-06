import utils
import os.path
import sublime, random, re, os
import sublime_plugin

class TiposXml:
	def tipoValido(tipo):
		return tipo in ["zul","xml","jsf","html","php","xaml"]

class CompletacionXml:
	def __init__(self, tipo=None):
		if not tipo:tipo=utils.get_language()
		if not TiposXml.tipoValido(tipo):return
		self.tipo=tipo
		self.rutaArchivo=utils.get_packages_path("SublimeXml", "%s.json"%(self.tipo))
		self.cargar()
	
	def cargar(self):
		if not os.path.exists(self.rutaArchivo):open(self.rutaArchivo, "w").close()
		d=sublime.decode_value(open(self.rutaArchivo).read())
		if not d:d={}
		self.tags=d["tags"] if d.get("tags") else {}
		self.attrs=d["attrs"] if d.get("attrs") else {}

	def agregarActuales(self):
		texto=ArchivoXml.getTextoLimpio()
		[self.agregarTag(tag) for tag in re.findall("(<([\w:-]+)\s+([^>]+)>)", texto, re.DOTALL)]
		self.guardar()

	def agregarTag(self, l):
		tag=l[1] 
		if not self.tags.get(tag):self.tags[tag]={"n":tag, "c":l[0][1:], "s":"n"}
		elif self.tags[tag]["s"]=="n":self.tags[tag]["c"]=l[0][1:]
		[self.agregarAtributo(tag, attr[0], attr[1]) for attr in re.findall('([\w:-]+)\s*=\s*"([^"]*)"', l[2])]

	def agregarAtributo(self, tag, attr, valor):
		coma=""
		if not self.attrs.get(attr):self.attrs[attr]={"n":attr, "e":tag, "v":valor}
		elif valor:
			if not valor in self.attrs[attr]["v"].strip().split(","):
				if self.attrs[attr]["v"].strip():coma=","
				self.attrs[attr]["v"]+=coma+valor
				coma=""
		if not tag in self.attrs[attr]["e"].strip().split(","):
			if self.attrs[attr]["e"].strip():coma=","
			self.attrs[attr]["e"]+=coma+tag

	def guardar(self):
		archivo=open(self.rutaArchivo, "w")
		d={}
		d["tags"]=self.tags
		d["attrs"]=self.attrs
		archivo.write(sublime.encode_value(d))
		archivo.close()

	def valores(self, atributo):
		atributo=atributo.strip()
		lista=[]
		valores=self.attrs[atributo]["v"].split(",")
		for v in valores:lista.append((v+"\t•", v))
		return lista
		
	def atributos(self, etiqueta):
		lista=[]
		for a in self.tags[etiqueta]["attrs"]:lista.append((a["n"]+"\t•", a["n"]+"="+'"${1:}"'))
		return lista


	def etiquetas(self):
		"""Genera todas las etiquetas con sus respectivos cierres"""
		lista=[]
		for e in self.tags:
			tag=self.tags[e]
			
			if tag["c"].count("\n")<=1:
				clean=tag["c"].strip()
				if not clean.endswith("/>") and not clean.startswith("!") and clean.count(">")==1:tag["c"]+="\n\n</"+tag["n"]+">"
			elif tag["c"].count("\n")>1 and tag["c"].strip().endswith("/>"):
				pass
			elif tag["c"].find("</%s>"%tag["n"])==-1:
				tag["c"]=tag["c"]+"\n\n</%s>"%tag["n"]
			lista.append((e+"\t•", ArchivoXml.agregarCursores(tag["c"])))
		return lista

	def limpiarCursores(self, linea):
		coincidencias=self.patron.findall(linea)
		for coincidencia in coincidencias:
			quitar=coincidencia[:coincidencia.find(":")+1]
			linea=linea.replace(coincidencia, coincidencia.replace(quitar, "").replace("}", ""))
		return linea

	def grabar(self, texto):
		lineas=texto.splitlines()
		tag=lineas[0].strip()
		tag=tag[1:tag.find(" ")]
		bloque=""
		for l in lineas:
			clean=l.strip()
			if not clean:bloque+="\n"
			if clean.startswith("<") or clean.startswith("</"):bloque+=l+"\n"
		bloque=bloque.strip()[1:]
		if not self.tags.get(tag):self.tags[tag]={"n":tag, "c":bloque}
		else:self.tags[tag]["c"]=bloque
		self.tags[tag]["s"]="y"
		self.guardar()

	def completar(self):
		view=sublime.active_window().active_view()
		lineSel=sublime.Region(view.line(view.sel()[0]).a, view.sel()[0].a)
		linea=view.substr(lineSel)
		if linea.strip().isalpha():return sorted(self.etiquetas())
		if linea.rfind(">")>linea.rfind("<"):return
		if linea.find("<")==-1:
			lines=view.lines(sublime.Region(0, view.size()))
			i=0
			for line in lines:
				if line==lineSel:
					return
				i+=1
			while i>=0:
				lineSel=lines[i]
				linea=view.substr(lineSel)
				if linea.find("<")==-1:i-=1
			else:return



		etiqueta=linea[linea.rfind("<")+1:linea.find(" ", linea.rfind("<"))]
		etiqueta=etiqueta.strip()
		if not etiqueta:
			return sorted(self.etiquetas())
		elif linea.strip().endswith("=") or linea.strip().endswith('="'):
			return sorted(self.valores(linea[linea.rfind(" "):linea.rfind("=")]))
		else:
			return sorted(self.atributos(etiqueta))

	def getAtributos(self, etiqueta):
		lista=[]
		for atributo in self.attrs:
			if etiqueta in self.attrs[atributo]["e"].split(","):
				lista.append(atributo)
		return lista

class xmlCompletions(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		tipo=utils.get_language()
		if not TiposXml.tipoValido(tipo):return
		punto=view.sel()[0].a
		completacion=CompletacionXml(tipo)
		if view.substr(sublime.Region(punto-1, punto))=="<":
			return completacion.completar()
		else:
			linea=view.substr(sublime.Region(view.line(punto).a, punto))
			if not linea.strip() or linea.strip().isalpha():
				return [(tag[0], "<"+tag[1]) for tag in completacion.completar()]
			if linea.find("<")==-1:return
			if linea.find(">")!=-1:return
			linea=linea[linea.rfind("<"):]
			if linea.endswith(" "):
				etiqueta=linea[1:linea.find(" ")]
				return [(atributo+"\t•", atributo+'="${1:}"')for atributo in completacion.getAtributos(etiqueta)]
			elif linea.endswith('="'):
				atributo=linea[linea.rfind(" ")+1:linea.rfind("=")].strip()
				return completacion.valores(atributo)

				
class Expresion:
	def __init__(self, exp, etiquetas):
		self.etiquetas=etiquetas
		self.generarDiccionario(exp)
		self.keys=self.etiquetas.keys()
		
	def generarDiccionario(self, exp):
		exp=exp.strip()+"^"
		self.diccionario={}
		self.nivel=1
		self.diccionario[self.nivel]=[]
		tag=""
		texto=""
		atributos=[]
		atributo=""
		bloqueo=0
		colectandoId=colectandoClase=colectandoNumero=colectandoTexto=colectandoAtributo=False
		numero=""
		comprimido=""
		for c in exp:
			if c==".":
				colectandoClase=True
				continue
			elif colectandoClase and not c.isalpha():
				if atributo:
					atributos.append('class="%s"'%atributo)
					atributo=""
				colectandoClase=False
			elif colectandoClase:
				atributo+=c
				continue
			elif c=="#":
				colectandoId=True
				continue
			elif colectandoId and not c.isalpha():
				if atributo:
					atributos.append('id="%s"'%atributo)
					atributo=""
				colectandoId=False
			elif colectandoId:
				atributo+=c
				continue
			elif c=="[":
				colectandoAtributo=True
				continue
			elif colectandoAtributo and c=="]":
				if atributo:
					atributos.append(atributo)
					atributo=""
				colectandoAtributo=False
				continue
			elif colectandoAtributo:
				atributo+=c
				continue
			elif c=="{":
				colectandoTexto=True
				continue
			elif colectandoTexto and c=="}":
				colectandoTexto=False
				continue
			elif colectandoTexto:
				texto+=c
				continue
			elif c=="(":
				bloqueo+=1
				continue
			elif c==")":
				bloqueo-=1
				if bloqueo==0:
					self.diccionario[self.nivel].append(Expresion(comprimido, self.etiquetas))
			if bloqueo==0:
				if colectandoNumero and c.isdigit():
					numero+=c
				elif colectandoNumero:
					for i in range(int(numero)):
						atributosTemp=[]
						if atributos:
							for a in atributos:atributosTemp.append(a.replace("$i", str(i+1)))
						self.diccionario[self.nivel].append(self.newTag(tag, texto.replace("$i", str(i+1)), atributosTemp))
					numero=""
					tag=""
					texto=""
					atributos=[]
					colectandoNumero=False
				if c==">":
					if tag:self.diccionario[self.nivel].append(self.newTag(tag, texto, atributos))
					tag=""
					texto=""
					atributos=[]
					self.nivel+=1
					self.diccionario[self.nivel]=[]
				elif c=="+" and tag:
					self.diccionario[self.nivel].append(self.newTag(tag, texto, atributos))
					tag=""
					texto=""
					atributos=[]
				elif c=="*":colectandoNumero=True
				elif c=="^":
					if tag:self.diccionario[self.nivel].append(self.newTag(tag, texto, atributos))
					elif atributos:
						for a in atributos:
							a=a.strip()
							if a.startswith("class=") or a.startswith("id="):
								self.diccionario[self.nivel].append(self.newTag("div", texto, atributos))
								break
					break
				elif c.isalpha() or c==":" or (c.isalnum() and tag.strip() and not colectandoNumero):tag+=c
			else:
				comprimido+=c
		return self.diccionario

	def newTag(self, tag, texto, atributos):
		return {"nombre":tag, "texto":texto, "atributos":atributos}

	def generarCompletacion(self, deltaTab=0):
		i=self.nivel
		completacionUltimoNivel=""
		completacionNivelActual=""
		while i>=1:
			for t in self.diccionario[i]:
				if type(t)==type({}):
					completacionNivelActual+=self.obtenerCompletacion(t, completacionUltimoNivel, i-1+deltaTab)
				else:completacionNivelActual+=t.generarCompletacion(i-1)
			completacionUltimoNivel=completacionNivelActual
			completacionNivelActual=""
			i-=1
		return completacionUltimoNivel
	


	#toma el inici y el final de la etiqueta y la inserta en el medio
	def obtenerCompletacion(self, tag, medio, tab):
		tab="\t"*tab
		atributos=""
		if tag["texto"]:
			if tag["texto"].find("lorem")!=-1:tag["texto"]=self.lorem(int(tag["texto"].replace("lorem", "").strip()))
			tag["texto"]="\n\t"+tab+tag["texto"]
		if tag["atributos"]:
			for a in tag["atributos"]:atributos+=a+" "
		return self.generarEtiqueta(tag["nombre"])%{"tag":tag["nombre"], "texto":tag["texto"], "medio":medio, "tab":tab, "atributos":atributos}
	
	def generarEtiqueta(self, etiqueta):
		return """%(tab)s<%(tag)s %(atributos)s>%(texto)s
%(medio)s
%(tab)s</%(tag)s>
"""

	def lorem(self, n):
		texto=""
		for i in range(n):texto+=chr(random.randint(97,122))
		return texto.replace(chr(random.randint(97,122)), " ").replace(chr(random.randint(97,122)), " ")
	
class emmetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=sublime.active_window().active_view()
		completacion=CompletacionXml()
		if view.sel()[0].a!=view.sel()[0].b:
			completacion.grabar(view.substr(view.sel()[0]))
			return
		self.etiquetas=completacion.tags
		linea=utils.get_line()
		lineaOriginal=linea
		contadorTabs=linea.count("\t")
		linea=linea.strip()
		punto=view.line(view.sel()[0].a).a
		texto=""
		if linea.startswith("lorem"):texto=self.lorem(int(linea.replace("lorem", "")))
		elif linea.isalpha():texto=self.bloqueUnico(linea, contadorTabs)
		else:
			exp=Expresion(linea, self.etiquetas)
			texto=exp.generarCompletacion()
		view.erase(edit, view.line(punto))
		print("la linea es : "+lineaOriginal)
		espacio=lineaOriginal.replace(lineaOriginal.lstrip(), "")
		print("el espacio es : "+espacio)
		view.run_command('insert_snippet', {"contents":espacio+ArchivoXml.formatear(texto, contadorTabs).replace("\n", "\n"+espacio)})
#		view.run_command("format")

	def lorem(self, n):
		texto=""
		for i in range(n):texto+=chr(random.randint(97,122))
		return texto.replace(chr(random.randint(97,122)), " ").replace(chr(random.randint(97,122)), " ")

	def bloqueUnico(self, tag, contadorTabs):
		tab="\t"*contadorTabs
		return """%(tab)s<%(tag)s>
%(tab)s
%(tab)s</%(tag)s>"""%{"tag":tag, "tab":tab}

class CargadorInteligente(sublime_plugin.EventListener):
	def on_post_save(self, view):
		tipo=utils.get_language()
		if TiposXml.tipoValido(tipo):
			CompletacionXml().agregarActuales()

class FormatoXmlCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view=sublime.active_window().active_view()
		region=sublime.Region(0, view.size())
		self.texto=ArchivoXml.formatear(view.substr(region))
		view.replace(edit, region, sef.texto)

class ArchivoXml:
	def formatear(texto, t=0):
		inicial=t
		texto=re.sub("\s+>", ">", texto)
		texto=re.sub("\s+/>", "/>", texto)
		text=""
		for l in texto.splitlines():
			l=l.strip()
			if re.match("^\</[^>]+\>$", l):
				t-=1
				l="\t"*t+l+"\n"
				if t==0:l+="\n"
			elif re.match("^\<[^>/]+\>$", l):
				tag=re.findall("^\<([\w-]+)", l)
				l="\t"*t+l+"\n"
				if tag:
					tag=tag[0]
					if texto.find("</"+tag)!=-1:
						t+=1
			else:
				l=""*t+l+""
				if re.match("[\w ]+",l.strip()):
					l="\t\t"+l+"\n"
			text+=l
		return text

	def agregarCursores(texto):
		textico=""
		for linea in texto.splitlines():
			if not linea.strip():
				linea+="\t~"
			textico+=linea+"\n"
		texto=textico
		texto=re.sub('=\s*"', '="~', texto)
		texto=re.sub('><', ">~<", texto)
		text=""
		i=1
		activo=False
		for c in texto:
			if activo and (c=='"' or c=='>' or c=="<" or c==" " or c=="\n" or c=="\t"):
				activo=False
				text+="}"
			elif c=="~":
				text+="${%i:"%i
				i+=1
				activo=True
				continue
			text+=c
		return text

	def getTexto(todo=True):
		view=sublime.active_window().active_view()
		if todo:return view.substr(sublime.Region(0, view.size()))
		else:return view.substr(sublime.Region(0, view.sel()[0].a))

	def getLineas(todo=True):
		return ArchivoXml.getTexto(todo).splitlines()

	def limpiarTexto(texto):
		texto=re.sub("<!--[^-]*-->", '', texto, flags=re.DOTALL)
		texto=re.sub("=\s*'", '="', texto)
		texto=re.sub(">[^<]*<", ">\n<", texto, flags=re.DOTALL)
		texto=re.sub("</[^>]+>", "", texto)
		texto=re.sub("\n+", "\n", texto)
		return texto

	def getTextoLimpio(todo=True):
		return ArchivoXml.limpiarTexto(ArchivoXml.getTexto(todo))