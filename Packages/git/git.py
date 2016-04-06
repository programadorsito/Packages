import http
import datetime
import re
import subprocess
import os
import sublime
import sublime_plugin
"""
class GitInitCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().init()

class GitResetCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().reset()

class GitPullCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().pull()

class GitPushBranchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().pushBranch()

class GitPushDeleteBranchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().pushDeleteBranch()

class GitCommitCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().commit()

class GitDeleteBranch(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().deleteBranch()

class GitCloneCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().clone()

class GitConfigCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().config()

class GitCheckoutCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().checkout()

class GitBranchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().branch()

class GitMergeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().merge()

class GitPushCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().push()

class GitConfigProxy(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().configProxy()

class GitAddCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().add()

class GitRemoveCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().remove()

class GitRenameCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().rename()

class GitDiffCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().diff()

class GitAddAllCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		ProyectoGit().addAll()


class ProyectoGit:
	def __init__(self):
		self.window=sublime.active_window()
		folders=self.window.folders()
		if len(folders)==0:
			sublime.status_message("Error : no se ha abierto ninguna carpeta")
			self.path=None
			return

		self.path=folders[0]
		os.chdir(self.path)
		

	def diff(self):
		path=self.getPath()
		window=sublime.active_window()
		view=window.active_view()
		salida=self.ejecutar("git diff --unified=0 "+path)
		puntos=[]
		numeroLinea=""
		for linea in salida.splitlines():
			if linea.startswith("@@"):
				numeroLinea=linea
			elif numeroLinea:
				if linea.startswith("+"):
					puntos.append(int(re.findall("\+([\d]+)", numeroLinea)[0]))
		i=0
		regiones=[]
		for line in view.lines(sublime.Region(0, view.size())):
			i+=1
			if i in puntos:
				regiones.append(line)
		view.erase_regions("diferentes")
		view.add_regions("diferentes", regiones, "comment", "bookmark", sublime.DRAW_OUTLINED)

	def getLine(self, lines, i):
		if i>=0 and i<len(lines):
			return lines[i]
		return None

	def rename(self):
		path=self.getPath()
		self.path=path
		sublime.active_window().show_input_panel("new name", os.path.basename(self.path), self.renameFile, None, None)

	def renameFile(self, newName):
		self.ejecutar("git mv "+self.path+" "+os.path.join(os.path.dirname(self.path), newName))

	def checkout(self, branch=None):
		if not branch:
			self.window.show_input_panel("branch", "", self.checkout, None, None)
		else:
			self.ejecutar("git checkout "+branch)

	def branch(self, branch=None):
		if not branch:
			self.window.show_input_panel("branch name", "", self.branch, None, None)
		else:
			self.ejecutar("git checkout -b "+branch)

	def merge(self, branch=None):
		if not branch:
			self.window.show_input_panel("branch name", "", self.merge, None, None)
		else:
			self.ejecutar("git merge "+branch)

	def deleteBranch(self, branch=None):
		if not branch:
			self.window.show_input_panel("branch name", "", self.deleteBranch, None, None)
		else:
			self.ejecutar("git branch -D "+branch)

	

	def reset(self, eleccion=None):
		if self.path==None:return
		if not eleccion:
			self.versiones=re.findall("\{([^:]+):([^:]+):([^:]+)\}",self.ejecutar("git log --pretty=format:{%H:%ct:%s}"))
			lista=[]
			for v in self.versiones:
				version=[]
				version.append(v[2])
				date=datetime.datetime(1,1,1,0,0).fromtimestamp(int(v[1])).strftime('%Y-%m-%d %H:%M:%S')
				version.append(date)
				lista.append(version)
			self.window.show_quick_panel(lista, self.reset)
		elif eleccion==-1:return
		else:self.ejecutar("git reset --hard "+self.versiones[eleccion][0])

	
	def config(self):
		self.ejecutar('')
		self.ejecutar('git config --global user.name "programadorsito"')
	
	def configProxy(self):
		self.ejecutar('')

	def push(self):
		self.getRuta()
		self.ejecutar("git push "+self.ruta+" master")

	def getRuta(self, ruta=None):
		if not ruta:
			salida=self.ejecutar("git remote -v")
			rutas=re.findall("https?://[^ ]+",salida)
			if rutas:ruta=rutas[0]
			else:
				self.window.show_input_panel("url", "", self.getRuta, None, None)
				return
		self.ruta=ruta.replace("://", "://programadorsito:alejandromagno1@")

	def pushBranch(self, rama=None):
		if not rama:
			self.window.show_input_panel("rama", "", self.pushBranch, None, None)
			return
		self.getRuta()
		self.ejecutar("git push "+self.ruta+" "+rama)

	def pushDeleteBranch(self, rama=None):
		if not rama:
			self.window.show_input_panel("rama", "", self.pushDeleteBranch, None, None)
			return
		self.getRuta()
		self.ejecutar("git push "+self.ruta+" :"+rama)

	def pull(self):
		self.getRuta()
		self.ejecutar("git pull "+self.ruta)

	def getPath(self):
		return sublime.active_window().active_view().file_name()
"""