import threading
import time
import os
import sublime_plugin
import sublime
import re
import utils

class SearchDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        self.lang=utils.get_language()

        self.regMetodos={
            "python":"def\\s+%(nombre)s\\(",
            "python3":"def\\s+%(nombre)s\\(",
            "ruby":"def\\s+%(nombre)s",
            "java":"[\w].+\s+%(nombre)s\(",
            "javascript":"function\\s*%(nombre)s\\(|%(nombre)s\\s*=\\s*function\\(",
            "nodejs":"function\\s*%(nombre)s\\(|%(nombre)s\\s*=\\s*function\\(",
            "c":"\\b%(nombre)s\\([^)]*\\)\\s*\\n?\\s*\\{",
            "c#":"\\b%(nombre)s\\([^)]*\\)\\s*\\n?\\s*\\{",
            "c++":"\\b%(nombre)s\\([^)]*\\)\\s*\\n?\\s*\\{"
        }

        self.regVariables={
            "python":"\\b%(nombre)s\\s*=[^=]?|\\b%(nombre)s\\s+in\\s+|def [\\w_]+\\(.*\\b%(nombre)s",
            "python3":"\\b%(nombre)s\\s*=[^=]?|\\b%(nombre)s\\s+in\\s+|def [\\w_]+\\(.*\\b%(nombre)s",
            "ruby":"\\b%(nombre)s\\s*=[^=]?|\\b%(nombre)s\\s+in\\s+|def [\\w_]+\\(.*\\b%(nombre)s",
            "java":"\\b%(nombre)s\\s*=[^=]?|[\\w]+\\s+%(nombre)s;|[\\w]+\\s+%(nombre)s,",
            "javascript":"\\b%(nombre)s\\s*=[^=]?|var+\\s+%(nombre)s;|var+\\s+%(nombre)s,",
            "nodejs":"\\b%(nombre)s\\s*=[^=]?|var+\\s+%(nombre)s;|var+\\s+%(nombre)s,",
            "c":"\\b%(nombre)s\\s*=[^=]?|[\\w]+\\s+%(nombre)s;|[\\w]+\\s+%(nombre)s,",
            "c#":"\\b%(nombre)s\\s*=[^=]?|[\\w]+\\s+%(nombre)s;|[\\w]+\\s+%(nombre)s,",
            "c++":"\\b%(nombre)s\\s*=[^=]?|[\\w]+\\s+%(nombre)s;|[\\w]+\\s+%(nombre)s,",
            "jsf":'id\\s*=\\s*"%(nombre)s"'
        }

        self.comentarios={
            "python":'#[^\\n]\\n|"""[^"]"""',
            "python3":'#[^\\n]\\n|"""[^"]"""',
            "ruby":'#[^\\n]\\n|"""[^"]"""',
            "java":"//[^\\n]\\n|/[*][^/]*[*]/",
            "javascript":"//[^\\n]\\n|/[*][^/]*[*]/",
            "nodejs":"//[^\\n]\\n|/[*][^/]*[*]/",
            "c":"//[^\\n]\\n|/[*][^/]*[*]/",
            "c#":"//[^\\n]\\n|/[*][^/]*[*]/",
            "c++":"//[^\\n]\\n|/[*][^/]*[*]/",
            "jsf":"<!--[^-]->"
        }

        var=utils.get_word_signature()
        print(var)
        isMethod=utils.is_method()
        isUnique=var.find(".")==-1
        if self.lang=="python" and var.startswith("self."):
            isUnique=True
            var=var[var.find(".")+1:]
        elif self.lang=="java" and var.startswith("this."):
            isUnique=True
            var=var[var.find(".")+1:]

        if isMethod:
            if isUnique:self.goto_method(var)
            else:self.goto_class_method(var[:var.find(".")], var[var.find(".")+1:])
        else:
            if isUnique:
                self.goto_definition(var)
                paquete=re.findall("import\s+([\w._]+\."+var+");", utils.get_text(), flags=re.IGNORECASE)
                if var[0].isupper() and paquete:
                    print("va hacia la clase")
                    self.goto_class(paquete[0])
            else:
                self.goto_class_definition(var[:var.find(".")], var[var.find(".")+1:])
                print("no unico")
        
    def goto_method(self, nombre):
        window=sublime.active_window()
        view=window.active_view()
        regiones=view.find_all(self.regMetodos[self.lang]%{"nombre":nombre})
        linea=utils.get_line_of_point(regiones[-1].a)
        utils.go_line(linea)

    def goto_class_method(self, clase, nombre):
        if clase[0].islower():print("va a ir primero a encontrar el tipo")
        print("va a ir a metodo de clase")
        window=sublime.active_window()
        view=window.active_view()
        texto=view.substr(sublime.Region(0, view.sel()[0].a))
        definicion=re.findall("([A-Z][\w]+)\s+"+clase, texto)[0]
        paquete=re.findall("import\s+([\w._]+\."+definicion+");", texto, flags=re.IGNORECASE)
        if definicion[0].isupper() and paquete:
            print("va hacia la clase")
            view=self.goto_class(paquete[0])
        self.nombreMetodo=nombre
        threading.Thread(target=self.goto_method_async).start()
    
    def goto_method_async(self):
        while True:
            window=sublime.active_window()
            view=window.active_view()
            if not view.is_loading():break
            time.sleep(1)
        regiones=view.find_all(self.regMetodos[self.lang]%{"nombre":self.nombreMetodo})
        linea=utils.get_line_of_point(regiones[-1].a)
        utils.go_line(linea)

    def goto_definition(self, nombre):
        window=sublime.active_window()
        view=window.active_view()
        regiones=view.find_all(self.regVariables[self.lang]%{"nombre":nombre})
        point=view.sel()[0].a
        r=None
        comentarios=view.find_all(self.comentarios[self.lang])
        for region in regiones:
            sirve=True
            if region.b > point and not self.lang in ["jsf"]:break
            for comentario in comentarios:
                if region.a > comentario.a and region.a<comentario.b:
                    sirve=False
            if sirve:r=region
        try:
            print(r.a)
            linea=utils.get_line_of_point(r.a)
            utils.go_line(linea)
        except:pass

    def goto_class_definition(self, clase, definition):
        if clase[0].islower():print("va a ir primero a encontrar tipo")
        print("va a ir a definicion de clase")

    def goto_class(self, paquete):
        paquete=paquete.replace(".", os.sep)+".java"
        archivos=utils.get_files_java()
        print(paquete)
        for archivo in archivos:
            if archivo.endswith(paquete):
                window=sublime.active_window()
                return window.open_file(archivo)