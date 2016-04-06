"""este programa formara un atributo apartir de una propiedad que se le especifica"""
import re
import sublime
import sublime_plugin


class CreateFieldCommand(sublime_plugin.TextCommand):
	palabra=""
	caret=0
	view=None
	regionClase=None
	tipo=""
	edit=None
	def run(self , edit):
		"""tomara la palabra identificara el itpo y luego a lo ultimo de la 
		clase pondra el atributo respectivo"""
		self.view=sublime.active_window().active_view()
		if self.view.scope_name(0).find("source.java ")==-1:return
		self.edit=edit;
		self.caret=self.view.sel()[0].a
		self.palabra=self.view.substr(self.view.word(self.caret))
		self.inicio=self.caret
		print(self.palabra)
		listo=True
		while self.inicio>=0:
			c=self.view.substr(self.inicio)
			if c=="{" and not listo:listo=True
			elif c=="{":break
			elif c=="}":listo=False
			self.inicio-=1

		self.fin=self.caret
		listo=True
		while self.fin<=self.view.size():
			c=self.view.substr(self.fin)
			if c=="}" and not listo:listo=True
			elif c=="}":break
			elif c=="{":listo=False
			self.fin+=1
		self.regionClase=self.view.substr(sublime.Region(self.inicio, self.fin+1))
		self.identificarTipo()
		self.ponerAtributo()

	def identificarTipo(self):
		lineas=self.regionClase.split("\n")
		for l in lineas:
			if re.findall("[A-Za-z][\w<> ]* "+self.palabra+"\s*[;=]", l):
				l=l.strip()
				partes=l.split(" ");
				for p in partes:
					if p.strip() and p.find(self.palabra)==-1:
						self.tipo=p
					if p.find(self.palabra.strip())!=-1:
						break
				print(self.tipo)
				break
		

	def ponerAtributo(self):
		"""buscara el fin de la clase y luego pondra los atributos alli"""
		posicion=self.view.find_all("\}")[-1].a
		insertar="""
	public void set%(nombreC)s(%(tipo)s %(nombre)s){this.%(nombre)s=%(nombre)s;}
	public %(tipo)s get%(nombreC)s(){return this.%(nombre)s;}
"""%{"tipo":self.tipo, "nombre":self.palabra, "nombreC":self.palabra[0].upper()+self.palabra[1:]}
		self.view.insert(self.edit, posicion, insertar)

