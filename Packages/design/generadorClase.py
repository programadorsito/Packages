import os
import sublime
import sublime_plugin


class GeneradorClaseJava:
	def __init__(self, clases):
		self.clases=clases
		self.d={"clases":{}, "paquete":""}
		self.generarClases()

	def generarClases(self):
		for clase in self.clases:
			if clase.startswith("paquete="):self.d["paquete"]=clase[clase.find("=")+1:]
			elif clase.find("{")!=-1:self.generarClase(clase)

	def getClases(self):
		return self.d

	def generarClase(self, linea):
		linea=linea.strip()
		if linea.startswith("//"):linea=linea.replace("//", "")
		lineaOriginal=linea
		nombreClase=nombre=linea[:linea.find("{")].strip()
		self.d["clases"][nombreClase]={"nombre":nombreClase, "filename":nombreClase+".java"}
		linea=linea[linea.find("{")+1:-1]
		partes=linea.split(",")
		atributos=[]
		for parte in partes:
			parte=parte.strip()
			nombreAtributo=parte[:parte.find(" ")]
			parte=parte[parte.find(" "):].strip()
			if parte.find(" ")!=-1:
				tipo=parte[:parte.find(" ")]
				parte=parte[parte.find(" "):].strip()
			else:
				tipo=parte
				parte=""
			atributos.append({"nombre":nombreAtributo, "tipo":tipo, "sql":parte})
		clase="//%s\npublic class %s implements Serializable\n{\n"%(lineaOriginal,nombreClase)
		clase+="\tprivate static final long serialVersionUID = 1L;\n\n"
		for attr in atributos:
			clase+="\tprivate %(tipo)s %(nombre)s;\n"%{"tipo":attr["tipo"], "nombre":attr["nombre"]}
		clase+="""
	public %s (){}
"""%(nombre)

		clase+="\n\tpublic %s ("%(nombre)
		for attr in atributos:
			clase+=attr["tipo"]+" "+attr["nombre"]+","
			break
		clase+=")"
		clase=clase.replace(",)", ")")
		clase+="\n\t{\n"
		for attr in atributos:
			clase+="\t\tthis.%(nombre)s=%(nombre)s;\n"%{"nombre":attr["nombre"]}
			break
		clase+="\t}\n"

		clase+="\n\tpublic %s ("%(nombre)
		for attr in atributos:
			clase+=attr["tipo"]+" "+attr["nombre"]+","
		clase+=")"
		clase=clase.replace(",)", ")")
		clase+="\n\t{\n"
		for attr in atributos:
			clase+="\t\tthis.%(nombre)s=%(nombre)s;\n"%{"nombre":attr["nombre"]}
		clase+="\t}\n"
		for attr in atributos:
			clase+="""
	public void set%(nombreC)s(%(tipo)s %(nombre)s){this.%(nombre)s=%(nombre)s;}
	public %(tipo)s get%(nombreC)s(){return this.%(nombre)s;}
"""%{"nombre":attr["nombre"], "tipo":attr["tipo"], "nombreC":attr["nombre"][0].upper()+attr["nombre"][1:]}
		inicio="package "+self.d["paquete"]+";\n" if self.d["paquete"] else ""
		self.d["clases"][nombreClase]["texto"]=inicio+clase+"\n}\n"

class GeneradorClasePython:
	def __init__(self, clases):
		self.clases=clases
		self.d={"clases":{}}
		self.generarClases()

	def generarClases(self):
		for clase in self.clases:
			if clase.find("{")!=-1:self.generarClase(clase)

	def getClases(self):
		return self.d

	def generarClase(self, linea):
		nombreClase=nombre=linea[:linea.find("{")].strip()
		self.d["clases"][nombreClase]={"nombre":nombreClase, "filename":nombreClase+".py"}
		linea=linea[linea.find("{")+1:-1]
		partes=linea.split(",")
		atributos=[]
		for parte in partes:
			parte=parte.strip()
			nombreAtributo=parte[:parte.find(" ")] if parte.find(" ")!=-1 else parte
			atributos.append({"nombre":nombreAtributo})

		constructorVacio="\tdef __init__(self):\n"
		cabeceraConstructorLleno="\tdef __init__(self"
		cuerpoConstructorLLeno=""
		metodos=[]
		for attr in atributos:
			attr["nombreUpper"]=attr["nombre"][:1].upper()+attr["nombre"][1:]
			constructorVacio+="\t\tself.%(nombre)s=None\n"%attr
			cabeceraConstructorLleno+=","+attr["nombre"]
			cuerpoConstructorLLeno+="\t\tself.%(nombre)s=%(nombre)s\n"%attr
			metodo="""
	def set%(nombreUpper)s(self, %(nombre)s):
		self.%(nombre)s=%(nombre)s
	"""%attr
			metodos.append(metodo)
			metodo="""
	def get%(nombreUpper)s(self):
		return self.%(nombre)s
	"""%attr
			metodos.append(metodo)
		
		cabeceraConstructorLleno+="):\n"
		clase="class %s:\n"%nombreClase
		clase+=constructorVacio+"\n"
		clase+=cabeceraConstructorLleno
		clase+=cuerpoConstructorLLeno
		for metodo in metodos:
			clase+=metodo
		self.d["clases"][nombreClase]["texto"]=clase

class GeneradorClase(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		tipo=view.scope_name(0)
		if tipo.startswith("source.java") or tipo.startswith("source.python"):
			region=view.sel()[0]
			if region.a==region.b:
				region=view.line(region.a)
			punto=region.a
			clases=view.substr(region).splitlines()
			view.replace(edit, region, "")
			if not clases:return
			d={}

			if tipo.startswith("source.java "):
				d=GeneradorClaseJava(clases).getClases()
			elif tipo.startswith("source.python "):
				d=GeneradorClasePython(clases).getClases()

			if not d:return
			
			ruta=""
			if view.file_name():
				ruta=view.file_name()
				sep="/" if ruta.find("/")!=-1 else "\\"
				ruta=ruta[:ruta.rfind(sep)]+os.sep
			elif window.folders():
				if window.folders()[0]:ruta=window.folders()[0]+os.sep

			if len(clases)==1:
				for clase in d["clases"]:
					view.run_command("insertar", {"text":d["clases"][clase]["texto"], "point":punto})
			else:
				if ruta:
					for clase in d["clases"]:
						clase=d["clases"][clase]
						archivo=open(ruta+clase["filename"], "w")
						archivo.write(clase["texto"])
						archivo.close()
						window.open_file(ruta+clase["filename"])
				else:
					for clase in d["clases"]:
						clase=d["clases"][clase]
						v=window.new_file()
						view.run_command("insertar", {"text":[clase]["texto"], "point":punto})
						#v.insert(edit, 0, clase["texto"])
						v.set_syntax_file(view.settings().get("syntax"))