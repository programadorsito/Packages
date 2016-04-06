import os
import re
import sublime_plugin
import sublime
import threading
import utils
import time


ORDEN=1
CARPETA_COMANDOS="D:/sublime3/Data/comandos/"
ARCHIVO_COMANDO="D:/sublime3/comando.txt"
ARCHIVO_BLOQUEO_UNO="D:/sublime3/flujo_uno.txt"
ARCHIVO_BLOQUEO_DOS="D:/sublime3/flujo_dos.txt"
ARCHIVO_BLOQUEO_TRES="D:/sublime3/flujo_tres.txt"
ARCHIVO_BLOQUEO_CUATRO="D:/sublime3/flujo_cuatro.txt"
loop=None


def eliminar_archivos():
    for ruta in [ARCHIVO_BLOQUEO_UNO, ARCHIVO_BLOQUEO_DOS, ARCHIVO_BLOQUEO_TRES, ARCHIVO_BLOQUEO_CUATRO]:
        if os.path.exists(ruta):os.remove(ruta)

def crear_archivo_bloqueo(orden):
    eliminar_archivos()
    ruta=None
    if orden==1:ruta=ARCHIVO_BLOQUEO_UNO
    elif orden==2:ruta=ARCHIVO_BLOQUEO_DOS
    elif orden==3:ruta=ARCHIVO_BLOQUEO_TRES
    elif orden==4:ruta=ARCHIVO_BLOQUEO_CUATRO

    if ruta:utils.file_write(ruta, "dani")

def existe_archivo_bloqueo(orden):
    print("verificando si existe el flujo : "+str(orden))
    ruta=None
    if orden==1:ruta=ARCHIVO_BLOQUEO_UNO
    elif orden==2:ruta=ARCHIVO_BLOQUEO_DOS
    elif orden==3:ruta=ARCHIVO_BLOQUEO_TRES
    elif orden==4:ruta=ARCHIVO_BLOQUEO_CUATRO
    if ruta:return os.path.exists(ruta)

class LoopComandoCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        global ORDEN
        global loop
        ORDEN=1
        if args.get("orden"):ORDEN=int(args.get("orden"))
        crear_archivo_bloqueo(ORDEN)
        if loop:
            print("Hilo "+str(ORDEN)+" ya iniciado")
            return
        print("iniciando loop de comando "+str(ORDEN))
        loop=LoopComando()
        loop.start()
#        threading.Thread(target=self.loop_comando).start()
 
class LoopComando(threading.Thread):
    def run(self):
        while True:
            comando=None
            if os.path.exists(ARCHIVO_COMANDO) and existe_archivo_bloqueo(ORDEN):
                archivito=open(ARCHIVO_COMANDO)
                comando=archivito.read()
                archivito.close()
                os.remove(ARCHIVO_COMANDO)
                if comando:
                    comando=comando.strip()
                    print(comando)
                    window=sublime.active_window()
                    view=window.active_view()
                    if comando.find("side_bar")!=-1:
                        window.run_command(comando)
                    elif comando.startswith("code_"):
                        rutaJson=sublime.packages_path()+os.sep+"snippets"+os.sep+utils.get_language()+".json"
                        if os.path.exists(rutaJson):
                            comando=comando.replace("code_", "")
                            d=utils.load_json(rutaJson)
                            if d.get(comando) :view.run_command('insert_snippet', {"contents":utils.agregarCursores(d[comando])})
                    elif comando.startswith("make_"):
                        window=sublime.active_window()
                        view=window.active_view()
                        comando=comando.replace("make_", "")   
                        view.run_command("load_template", {"nombre":comando})
                    else:
                        view.run_command(comando)
            time.sleep(1)

class BuildCommands(sublime_plugin.TextCommand):
    def run(self, edit):
        archivos=utils.get_files({"folder":sublime.packages_path(), "ext":"py"})
        comandos=[]
        for archivo in archivos:
            texto=utils.file_read(archivo)
            comandos+=re.findall("class\s+([\w]+)\(sublime_plugin.TextCommand\):", texto, flags=re.IGNORECASE)
        comandos=list(set(comandos))
#        print(comandos)
        for comando in comandos:
            self.generar_comando(comando)

    def generar_comando(self, comando):
        if comando.endswith("Command"):comando=comando[:-7]
        comando_sublime=comando[0]
        i=1
        l=len(comando)
        while i< l:
            if comando[i].isupper():comando_sublime+="_"
            comando_sublime+=comando[i]
            i+=1
        comando_sublime=comando_sublime.lower()
        utils.file_write(CARPETA_COMANDOS+comando_sublime+".bat", "echo "+comando_sublime+" > "+ARCHIVO_COMANDO)
