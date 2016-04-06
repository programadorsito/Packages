import http
import datetime
import re
import subprocess
import os
import sublime
import sublime_plugin
import shutil
import utils
import time
import threading


class ChangeMavenContextCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.folderConf=os.environ["M2_HOME"]+os.sep+"conf"
		self.archivos=utils.get_files({"folder":self.folderConf, "ext":"xml"})
		window=sublime.active_window()
		window.show_quick_panel(self.archivos, self.seleccionar)

	def seleccionar(self, index):
		if index==-1:return
		archivo=self.archivos[index]
		utils.file_write(self.folderConf+os.sep+"settings.xml", utils.file_read(archivo))
		

class MavenExec(sublime_plugin.TextCommand):
	def run(self, edit):
		window=sublime.active_window()
		view=window.active_view()
		filename=os.path.basename(view.file_name())
		clase=filename[:filename.find(".")]
		texto=view.substr(sublime.Region(0, view.size()))
		paquete=re.findall("package ([\w.]+);", texto)[0]
		ProyectoMaven().ejecutarComando('mvn exec:java -Dexec.mainClass="%(paquete)s.%(clase)s"'%{"paquete":paquete, "clase":clase})

class MavenHelpEffectivePom(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoMaven().ejecutarComando("mvn help:effective-pom")


class ProyectoMaven:
	"""Administrate a Maven"""

	def crear(self):
		"""Prepara la lista de artefactos, extrae el nombre del proyecto, y muestra los artefactos"""
		self.window=sublime.active_window()
		folders=self.window.folders()
		if not folders:
			sublime.status_message("No se ha abierto ningun subdirectorio")
			return
		folder=folders[0]
		parentFolder=os.path.dirname(folder)
		self.projectName=os.path.basename(folder)
		self.path=parentFolder
		os.chdir(self.path)
		print("el directorio padre es  : "+self.path)
		print("el nombre del proyecto es : "+self.projectName)
		self.archetypes={}
		self.archetypes["desktop"]="mvn archetype:create "
		self.keys=list(self.archetypes.keys())
		self.window.show_quick_panel(self.keys, self.seleccionar)
		
	def seleccionar(self, index):
		"""Selecciona el artefacto y pide el groupId"""
		if index==-1:return
		self.archetype=self.archetypes[self.keys[index]]
		self.window.show_input_panel("groupId", "com.", self.crearProyecto, None, None)

	def crearProyecto(self, DgroupId):
		"""Crea el proyecto"""
		comando=self.archetype+"-DgroupId=%s -DartifactId=%s"%(DgroupId, self.projectName)
		try:os.removedirs(self.projectName)
		except:pass
		self.ejecutarComando(comando)

	def __init__(self, config=True):
		"""Set the working folder has folder opened"""
		if not config:return
		self.window=sublime.active_window()
		folders=self.window.folders()
		if len(folders)==0:
			sublime.status_message("Error : no se ha abierto ninguna carpeta")
			self.path=None
			return

		self.path=folders[0]
		os.chdir(self.path)

	def ejecutar(self):
		"""Execute the GIT command"""
		time.sleep(1)
		if self.path==None:return
		proceso=subprocess.Popen(self.comando(self.strComando), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		if proceso.communicate()[1]:
			error=proceso.communicate()[1].decode("utf-8")
			sublime.status_message("MAL "+error)
			print(error)
		else:
			salida=proceso.communicate()[0].decode("utf-8")
			print(salida)
			self.window.run_command("refresh_folder_list")
			sublime.status_message("-----OK-----")
			return salida

	def comando(self, comando):
		"""Open the terminal according to the system"""
		return comando if sublime.platform()=="windows" else "gnome-terminal -x bash -c '%s'"%(comando)

	def getPath(self):
		"""Get path from the actual view"""
		return sublime.active_window().active_view().file_name()

	def ejecutarComando(self, comando):
		self.strComando=comando
		print(comando)
		threading.Thread(target=self.ejecutar).start()
		self.window.run_command("refresh_folder_list")
		sublime.status_message("Success : "+comando)
