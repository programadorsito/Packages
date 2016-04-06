import os
import sublime_plugin
import sublime
import utils
import re

class CuadrarMensajesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lang=utils.get_language()
        if lang not in ["jsf", "java", "xml"]:return
        match=None
        text=utils.get_text()
        labels=[]
        ext=self.ext="properties"
        if lang=="java":
            match=utils.get_preference("messages.file")
            if not match:match="messages"
            labels=re.findall('mostrarInfo\("([\w\d_]+)"\)', text, flags=re.IGNORECASE)
            labels+=re.findall('mostrarError\("([\w\d_]+)"\)', text, flags=re.IGNORECASE)
            labels+=re.findall('mostrarAdvertencia\("([\w\d_]+)"\)', text, flags=re.IGNORECASE)
            labels+=re.findall('getMsg\("([\w\d_]+)"\)', text, flags=re.IGNORECASE)
            labels=labels
        elif lang=="jsf":
            match=utils.get_preference("labels.file")
            if not match:math="label"
            stringLabel=re.findall("#\{label\.([\w\d_]+)\}", text, flags=re.IGNORECASE)
            stringMsg=re.findall("#\{msg\.([\w\d_]+)\}", text, flags=re.IGNORECASE)
            if stringLabel:labels=stringLabel
            if stringMsg:labels=stringMsg
        elif lang=="xml":
            match="strings"
            ext=self.ext="xml"
            stringStrings=re.findall('@string/([^"]+)', text, flags=re.IGNORECASE)
            if stringStrings:labels=stringStrings

        if not labels:
            print("no se tienen labels")
            return
        labels=list(set(labels))
        filesLabel=utils.get_files({"ext":ext,"ignores":["target", "build", ".svn", ".git", "bin"], "match":match})
        self.pendientes=[]
        self.i=0
        self.total=0
        for ruta in filesLabel:
            archivo=open(ruta)
            texto=archivo.read()
            archivo.close()
            mensajes=re.findall("([\w]+)\s*=", texto, flags=re.IGNORECASE)
            if ext=="xml":mensajes=re.findall('<string\s+name="([\w]+)">', texto, flags=re.IGNORECASE)
            for label in labels:
                if not label in mensajes:
                    self.total+=1
                    self.pendientes.append([ruta, label])
        if len(self.pendientes)>0:
            self.pedir()


    def pedir(self, value=None):
        window=sublime.active_window()
        if not value:
            nombreArchivo=os.path.basename(self.pendientes[self.i][0])
            label=self.pendientes[self.i][1]
            window.show_input_panel(nombreArchivo,label, self.pedir, None, None)
        else:
            self.pendientes[self.i].append(value)
            self.i+=1
            if self.i>=self.total:self.llenar()
            else:
                nombreArchivo=os.path.basename(self.pendientes[self.i][0])
                label=self.pendientes[self.i][1]
                window.show_input_panel(nombreArchivo,label, self.pedir, None, None)
    
    def llenar(self):
        ruta=""
        archivo=None
        for pendiente in self.pendientes:
            if pendiente[0]!=ruta:
                if archivo:
                    archivo.flush()
                    archivo.close()
                ruta=pendiente[0]
                archivo=open(ruta,"a")
            if self.ext=="xml":archivo.write('\n\t<string name="'+pendiente[1]+'">'+pendiente[2]+'</string>')
            else:archivo.write("\n"+pendiente[1]+"="+pendiente[2])
        if archivo:
            archivo.flush()
            archivo.close()
            if self.ext=="xml":utils.file_write(ruta,utils.file_read(ruta).replace("</resources>", "")+"\n</resources>")
          