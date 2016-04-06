"""este programa formara un atributo apartir de una propiedad que se le especifica"""

import sublime
import sublime_plugin


class CrearClase(sublime_plugin.TextCommand):
	def run(self, edit):
		view=sublime.active_window().active_view()
		region=view.line(view.sel()[0])
		self.linea=view.substr(region)
		view.erase(edit, region)
		scope=view.scope_name(region.a)
		if scope.find("source.java ")!=-1:
			view.insert(edit, region.a, self.java())
	def java(self):
		linea=self.linea
		nombre=linea[:linea.find("{")].strip()
		print(nombre)
		linea=linea[linea.find("{")+1:-1]
		partes=linea.split(",")
		atributos=[]
		for parte in partes:
			parte=parte.strip()
			atributos.append({"tipo":parte[:parte.rfind(" ")], "nombre":parte[parte.rfind(" ")+1:]})
		print(atributos)
		clase="public class %s\n{\n"%nombre
		for attr in atributos:
			clase+="\tprivate %(tipo)s %(nombre)s;\n"%{"tipo":attr["tipo"], "nombre":attr["nombre"]}
		clase+="""
	public %s ()
	{

	}
"""%(nombre)
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
	public void set%(nombreC)s(%(tipo)s %(nombre)s)
	{
		this.%(nombre)s=%(nombre)s;
	}

	public %(tipo)s get%(nombreC)s()
	{
		return this.%(nombre)s;
	}
"""%{"nombre":attr["nombre"], "tipo":attr["tipo"], "nombreC":attr["nombre"][0].upper()+attr["nombre"][1:]}
		return clase+"\n}"