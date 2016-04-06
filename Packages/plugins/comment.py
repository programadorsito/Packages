import sublime, os
import sublime_plugin
import re
import utils
class ComentarCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		tipo=view.scope_name(0)
		region=view.sel()[0]
		lang=utils.get_language()
		for region in reversed(view.sel()):
			for line in reversed(view.lines(region)):
				if line.a==line.b:line=view.line(line)
				texto=view.substr(line)
				
				if lang in ["python", "python3"]:
					if texto.strip().startswith("#"):texto=texto[:texto.find("#")]+texto[texto.find("#")+1:]
					else: texto="#"+texto
				if lang=="ruby":
					if texto.strip().startswith("#"):texto=texto[:texto.find("#")]+texto[texto.find("#")+1:]
					else:texto="#"+texto
				if lang=="batch file":
					if texto.strip().startswith("rem "):texto=texto[:texto.find("rem ")]+texto[texto.find("rem ")+4:]
					else: texto="rem "+texto
				elif lang in ["java", "c", "c++", "c#", "php", "javascript", "go", "nodejs"]:
					if texto.strip().startswith("//"):texto=texto[:texto.find("//")]+texto[texto.find("//")+2:]
					else: texto="//"+texto
				elif lang=="css":
					if texto.strip().startswith("/*"):texto=texto.replace("/*", "").replace("*/", "");
					else: texto="/*"+texto+"*/"
				elif lang in ["html", "android", "zul", "jsf", "xml"]:
					if texto.strip().startswith('<!--'):texto=texto.replace('<!--', '').replace('-->', '')
					else:texto="<!--"+texto+"-->"
				elif lang =="plsql":
					if texto.strip().startswith("--"):texto=texto[:texto.find("--")]+texto[texto.find("--")+2:]
					else: texto="--"+texto
				elif view.file_name() != None:
					filename=os.path.basename(view.file_name())
					if filename.endswith(".properties"):
						if texto.strip().startswith("#"):texto=texto[:texto.find("#")]+texto[texto.find("#")+1:]
						else: texto="#"+texto
				else:return
				view.replace(edit, line, texto)

class CleanCommentsCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		tipo=view.scope_name(0)
		region=sublime.Region(0, view.size())
		texto=view.substr(region)
		text=""
		if tipo.startswith("source.java"):
			if texto.find("~")!=-1:return
			texto=texto.replace("/**", "~").replace("/*", "~").replace("*/", "~")
			noMas=False
			for c in texto:
				if c=="~":
					noMas=not noMas
					continue
				if noMas:continue
				text+=c
			view.replace(edit, region, text)


class CommentMethodCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		punto=view.sel()[0].a+2
		linea=view.substr(view.line(sublime.Region(punto, punto)))
		linea=re.sub("\<[^>]*\>", "", linea)
		parts=re.findall("([\w]+)\s+([\w]+)\(([^)]*)\)", linea)
		if not parts:return
		retorno=parts[0][0]
		nombre=parts[0][1]
		parametros=parts[0][2]
		texto="/**\n"
		texto+="\t*\n"
		if retorno!="void":
			texto+="\t* @return "+retorno+"\n"
	
		if parametros:
			for param in parametros.split(","):
				texto+="\t* @param "+param+"\n"
		texto+="\t*/"
		print("asi quedo el comentario")
		print(texto)
		punto=view.sel()[0].a
		view.replace(edit, sublime.Region(punto, punto), texto)