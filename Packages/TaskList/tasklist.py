import os
import sublime
import sublime_plugin

class TaskListCommand(sublime_plugin.TextCommand):
	def run(self, edit, **args):
		window=sublime.active_window()
		view=window.active_view()
		self.cargarTareas()
		if not args.get("path"):
			if args.get("project"):args["path"]=window.folders()[0]
			else :
				args["path"]=view.file_name()
				if not args["path"]:args["path"]="general"
		if not args.get("path"):return
		if not self.tareas:self.tareas={}
		self.path=args["path"]
		self.archivo=self.tareas.get(args["path"])
		if not self.archivo:self.tareas[args["path"]]=self.archivo={}
		if args.get("agregar"):window.show_input_panel("Ingrese tarea", "", self.registrarTarea, None, None)
		elif args.get("mostrar"):
			if self.archivo and self.archivo["tareas"]:
				window.show_quick_panel(self.archivo["tareas"], self.seleccionarTarea)

	def registrarTarea(self, tarea):
		if not self.archivo.get("tareas"):self.archivo["tareas"]=[]
		self.archivo["tareas"].append(tarea)
		self.guardarTareas()

	def seleccionarTarea(self, indice):
		if indice==-1:return
		tareaHecha=""
		tareaSeleccionada=self.archivo["tareas"][indice]
		if tareaSeleccionada.endswith("•"):
			self.archivo["tareas"].remove(tareaSeleccionada)
			if len(self.archivo["tareas"])==0:
				del self.tareas[self.path]
				self.guardarTareas()
			return
		for tarea in self.archivo["tareas"]:
			if tarea.endswith("•"):
				tareaHecha=tarea
				break
		if tareaHecha:self.archivo["tareas"].remove(tareaHecha)
		if tareaSeleccionada in self.archivo["tareas"]:
			self.archivo["tareas"].remove(tareaSeleccionada)
		self.archivo["tareas"].append(tareaSeleccionada+"      •")
		print("asi es que es")
		self.guardarTareas()

	def cargarTareas(self):
		self.tareas=sublime.decode_value(open(sublime.packages_path()+os.sep+"tasklist"+os.sep+"tasklist.json").read())

	def guardarTareas(self):
		archivo=open(sublime.packages_path()+os.sep+"tasklist"+os.sep+"tasklist.json", "w")
		archivo.write(sublime.encode_value(self.tareas))
		archivo.close()