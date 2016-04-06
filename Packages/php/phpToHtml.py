import os
import sublime_plugin
import sublime
import os.path
import utils
import re

class PhpToHtml(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("Nombre proyecto","", self.phpToHtml, None,None)
    def phpToHtml(self, projectName):
        self.d=d=utils.get_dict_files({"ext":".php"})
        for archivo in d.keys():
            print(archivo)
            text=d[archivo]
            text=self.convertir(text)
            newRuta="d:/fromphp/"+archivo[archivo.find(projectName):]
            try:os.makedirs(os.path.dirname(newRuta))
            except:pass
            newRuta=newRuta.replace(".php", ".html")
            utils.file_write(newRuta, text=text)
    
    def get(self, ruta):
        for key in self.d.keys():
            if key.endswith(os.sep+ruta):
                #print("we find it :"+key)
                return self.d[key]

    def convertir(self, text):
        while text.find('include("')!=-1:
            includes=re.findall('(include\("([\w.-]+)"\);)', text)
            text=text.replace("?>", "").replace("<?php", "")
            #print(includes)
            for include in includes:
                rutaArchivo=self.get(include[1])
                if rutaArchivo:
                    print("se va a reemplazar :"+include[0])
                    text=text.replace(include[0], rutaArchivo)
                else:
                    text=text.replace(include[0], "")
        return text



                