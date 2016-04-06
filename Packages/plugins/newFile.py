import time
import os
import utils
import sublime_plugin
import sublime
import re


TEMPLATES_PATH="d:/sublime3/data/templates/"

class NuevoArchivoCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
        self.carpeta=args["folder"] if args.get("folder")!=None else None
        archivos=utils.get_files({"folder":TEMPLATES_PATH})
        opciones=[]
        extensiones=[]
        for archivo in archivos:
            rutaArchivo=os.path.dirname(archivo)
            carpeta=os.path.basename(rutaArchivo)
            nombreArchivo=os.path.basename(archivo)
            extensiones.append(nombreArchivo[nombreArchivo.rfind(".")+1:])
            nombreArchivo=nombreArchivo[:nombreArchivo.rfind(".")]
#            nombreArchivo=nombreArchivo[0].upper()+nombreArchivo[1:]
            opcion=carpeta+" : "+nombreArchivo
            opciones.append(opcion)
        window=sublime.active_window()
        self.opciones=opciones
        self.extensiones=extensiones
        window.show_quick_panel(self.opciones, self.seleccionar)

    def seleccionar(self, index):
        if index==-1:return
        self.opcion=self.opciones[index]
        self.extension=self.extensiones[index]
        print("la extension es : "+self.extension)
        self.crearArchivo()

    #Crea el archivo aparte de lo que se selecciono
    def crearArchivo(self):
        archivo=self.opcion.split(":")
        print(archivo)
        self.lang=archivo[0].strip()
        lang=self.lang
        archivo=lang+"/"+archivo[1].strip()+"."+self.extension
        archivo=TEMPLATES_PATH+archivo
        print("la ubicacion del archivo es : "+archivo)
        self.text=utils.file_read(archivo)
        print(self.text)
        window=sublime.active_window()
        window.show_input_panel("File Name", "", self.pedirNombre, None, None)
#        utils.file_write(archivo, )

    def pedirNombre(self, nombre):
        if nombre==None:return
        self.nombre=nombre
        if not self.carpeta:self.carpeta=utils.get_filedir()
        self.rutaNewFile=self.carpeta+os.sep+nombre+"."+self.extension
        self.procesar()
        
    #procesar preferencias d eusuario, fechas actuales, y toros datos referentes de cdaa lenguaje
    def procesar(self):
        paquete=utils.get_file_package({"filepath":utils.get_filedir({"filepath":self.rutaNewFile})})
        if not paquete:paquete=""
        self.text=self.text.replace("~filename~", self.nombre)
        print("texto despues de filename : "+self.text)
        self.text=self.text.replace("~package~", paquete)
        self.text=self.text.replace("~currentDate~", time.strftime("%d/%m/%Y"))
        self.values=[]
        self.i=0
        self.window=sublime.active_window()
        self.parametros=re.findall("~([\w]+)~", self.text)
        self.parametros=list(set(self.parametros))
        print("los parametros son : ", self.parametros)
        self.leer(None)


    def leer(self, value):
        if value:self.values.append(value)
        self.i+=1
        if self.i==len(self.parametros)+1:
            self.escribirArchivo()
        else:self.window.show_input_panel("param",self.parametros[self.i-1],self.leer, None, None)

    def escribirArchivo(self):
        for i in range(len(self.parametros)):
            print(i)
            param=self.parametros[i]
            value=self.values[i]
            self.text=self.text.replace("~"+param+"~", value)
            self.text=self.text.replace("~lf:"+param+"~", value[0].lower()+value[1:])
            self.text=self.text.replace("~uf:"+param+"~", value[0].upper()+value[1:])
            self.text=self.text.replace("~lo:"+param+"~", value.lower())
            self.text=self.text.replace("~up:"+param+"~", value.upper())
        utils.file_write(self.rutaNewFile, self.text)
        window=sublime.active_window()
        window.open_file(self.rutaNewFile)
        


class SaveTempalteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("Template Name", "", self.pedirNombre, None, None)
    
    def pedirNombre(self, nombre):
        self.nombre=nombre
        self.guardarTemplate()

    def guardarTemplate(self):
        lang=utils.get_language()
        ruta=TEMPLATES_PATH+lang
        filename=utils.get_filename()
        rutaArchivo=os.path.join(ruta,"x."+lang)

