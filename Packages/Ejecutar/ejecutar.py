#si no hay archivo que lo guarde en un temporal que tome todos los datos de la vista y que tome todos los datos del archivo
import sublime, os, platform
import sublime_plugin
import subprocess
import webbrowser
import utils
from subprocess import PIPE, Popen

class RunFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		esLinux=False
		esMac=False
		view=sublime.active_window().active_view()
		tipo=utils.get_language()
		comando=""
		archivo=self.extraerArchivo(view.file_name(), tipo)
		print("el archivo es :"+archivo["ruta"])
		print("la ruta es : "+archivo["ruta"])
		os.chdir(archivo["ruta"])
		pausa=" & pause>nul"
		plataforma=platform.system().lower().strip()

		if plataforma == "linux":
			esLinux=True
			pausa=' && read - p ""'
		elif plataforma == "darwin":
			esMac=True

		print(archivo)
		commands={
		"java":"java %(nombre)s"%archivo,
		"c":"%(nombre)s"%archivo,
		"batch file":"%(nombre)s"%archivo,
		"ruby":'ruby %(path)s'%archivo,
		"r":'rscript %(path)s'%archivo,
		"python":'python %(path)s'%archivo,
		"python3":'python3 %(path)s'%archivo,
		"dart":'dart %(nombreCompleto)s'%archivo,
		"plsql":'sqlplus %(username)s/%(password)s~%(host)s:%(port)s/%(service)s @ %(path)s'%archivo,
		"sqlite":'sqlite -cmd ".read %(nombreCompleto)s"'%archivo,
		"mysql":'mysql --bind-address=%(host)s --port=%(port)s --user=%(username)s --password=%(password)s --database=%(db)s -e "source %(path)s"'%archivo,
		"nodejs":'node %(path)s'%archivo,
		"perl":'perl %(nombreCompleto)s'%archivo,
		"mongodb":"mongo %(nombreCompleto)s"%archivo,
		"source.postgre ":"psql -f %(nombreCompleto)s"%archivo,
		"sqlserver":'sqlcmd -S "ANTIN\SQLEXPRESS" -i "%(nombreCompleto)s"'%archivo,
		"scala":"scala %(nombreCompleto)s"%archivo,
		"groovy":"groovy %(path)s"%archivo,
		"go":"go run %(path)s"%archivo
		}

		print("el tipo es : "+tipo)
		if commands.get(tipo):
			print("el tipo es: "+commands.get(tipo))
			comando=commands.get(tipo)
		elif tipo.startswith("source.js ") or tipo.startswith("source.basic.html"):
			webbrowser.open_new_tab(archivo["path"])
			return
		else:
			print("no es ninguno")

		if comando.strip():
			print("el comando es : "+comando)
			if esMac:
				print("es mac")
				rutaArchivo = os.path.join(sublime.packages_path(), "run.command")
				utils.file_write(rutaArchivo, comando)
				comando='open "'+rutaArchivo+'"'
				print("el comando final es : "+comando)
				os.system(comando)
			else:
				view.run_command("ejecutar_comando", {"comando":comando})			

	def extraerArchivo(self, path, tipo):
		if tipo=="js":path=None
		archivo={}
		view=sublime.active_window().active_view()
		seleccion=view.sel()[0].a!=view.sel()[0].b
		if seleccion:path=None
		if not path:
			prefacio=""
			anexo=""
			exts={
			"java":"java",
			"batch file":"bat",
			"c":"c",
			"r":"r",
			"mysql":"sql",
			"sqlserver":"sqlserver",
			"cpp":"cpp",
			"python":"py",
			"python3":"py",
			"ruby":"rb",
			"dart":"dart",
			"perl":"pl",
			"nodejs":"js",
			"mongodb":"js",
			"scala":"scala",
			"groovy":"groovy",
			"go":"go"
			}

			if exts.get(tipo):
				path=utils.get_temp(name="app", ext=exts.get(tipo))
				print("el archivo retornado es : "+path)
			elif tipo=="js":
				prefacio="<html><head><script>"
				anexo="</script></head><body></body></html>"
				path=utils.get_temp(name="app", ext="html")
			elif tipo=="plsql":
				prefacio="set wrap off\nset pagesize 30\nset serveroutput on"
				path=utils.get_temp(name="app", ext="sql")
			elif tipo=="sqllite":
				path=utils.get_temp(name="app", ext="sql")
				prefacio=(".restore "+sublime.packages_path()+os.sep+"bd.sqlite").replace("\\", "/")
				anexo=(".backup "+sublime.packages_path()+os.sep+"bd.sqlite").replace("\\", "/")
			
			fil=open(path, "w")
			if prefacio:fil.write(prefacio+"\n")
			if seleccion:
				fil.write(view.substr(view.sel()[0]))
			else:
				fil.write(self.view.substr(sublime.Region(0, self.view.size())))
			if anexo:fil.write("\n"+anexo)
			fil.close()
		else:self.view.run_command("save")

		archivo["db"]=""
		archivo["username"]=""
		archivo["password"]=""
		archivo["host"]=""
		archivo["port"]=""
		archivo["service"]=""
		archivo["db"]=""

		if tipo=="plsql":
			archivo["username"]=utils.get_preference("oracle.user")
			archivo["password"]=utils.get_preference("oracle.pass")
			
			archivo["host"]=utils.get_preference("oracle.host")
			if not archivo["host"]:archivo["host"]="localhost"
			
			archivo["port"]=utils.get_preference("oracle.port")
			if not archivo["port"]:archivo["port"]="1521"
			
			archivo["service"]=utils.get_preference("oracle.service")
			if not archivo["service"]:archivo["service"]="xe"
		elif tipo=="mysql":
			archivo["username"]=utils.get_preference("mysql.user")
			archivo["password"]=utils.get_preference("mysql.pass")
			archivo["host"]=utils.get_preference("mysql.host")
			archivo["port"]=utils.get_preference("mysql.port")
			archivo["db"]=utils.get_preference("mysql.db")

		path=path.strip()
		sep="\\"
		if path.find("/")!=-1:sep="/"
		archivo["path"]=path
		archivo["nombreCompleto"]=path[path.rfind(sep)+1:]
		archivo["ruta"]=path[:path.rfind(sep)]

		if(archivo["nombreCompleto"].find(".")!=-1):
			archivo["nombre"]=archivo["nombreCompleto"][:archivo["nombreCompleto"].find(".")]
			archivo["extension"]=archivo["nombreCompleto"][archivo["nombreCompleto"].find(".")+1:]
		else:
			archivo["nombre"]=archivo["nombreCompleto"]
		return archivo