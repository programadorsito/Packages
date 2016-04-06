import re
import sublime_plugin
import sublime
import utils

class BuildBeanFromViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lang=utils.get_language()
        if not lang in ["java"]:return
        self.vistas=utils.get_files({"ext":"xhtml", "ignores":["target", "build", ".svn", ".git", "bin"]})
        window=sublime.active_window()
        window.show_quick_panel(self.vistas,self.seleccionarVista)

    def seleccionarVista(self, index):
        if index==-1:return
        archivo=open(self.vistas[index])
        texto=texto=archivo.read()
        self.text=utils.get_text()
        archivo.close()
        nombreClase=re.findall("public\s+class\s+([\w]+)", self.text, flags=re.IGNORECASE)
        claseHereda=re.findall("public\s+class\s+[\w]+\s+extends\s+([\w]+)", self.text, flags=re.IGNORECASE)
        
        nombreClase=nombreClase[0]
        if claseHereda:
            claseHereda=claseHereda[0]
            archivos=utils.get_files({"match":claseHereda+".java", "ignores":["target", "build", ".svn", ".git", "bin"]})
            print("los archivos encontrados son : ")
            print(archivos)
            if archivos:self.text+=open(archivos[0]).read()
        print("el nombre de la clase es : "+nombreClase)
            #{"ext":"java", "ignores":["target", "build", ".svn", ".git", "bin"]}
        
        reg_listener='listener=\s*"#\{%s\.([\w]+)\}"'%nombreClase
        reg_actionListener='actionListener=\s*"#\{%s\.([\w]+)\}"'%nombreClase
        reg_action='action=\s*"#\{%s\.([\w]+)\}"'%nombreClase
        reg_complete_method='completeMethod=\s*"#\{%s\.([\w]+)\}"'%nombreClase
        
        metodos=re.findall(reg_listener, texto, flags=re.IGNORECASE)
        metodos+=re.findall(reg_actionListener, texto, flags=re.IGNORECASE)
        metodos+=re.findall(reg_complete_method, texto, flags=re.IGNORECASE)
        metodos+=re.findall(reg_action, texto, flags=re.IGNORECASE)

        
        texto=re.sub(reg_listener, "", texto,flags=re.IGNORECASE)
        texto=re.sub(reg_actionListener, "", texto,flags=re.IGNORECASE)
        texto=re.sub(reg_action, "", texto,flags=re.IGNORECASE)
        texto=re.sub(reg_complete_method, "", texto,flags=re.IGNORECASE)
        
        atributos=re.findall("#\{%s\.([\w]+)\}"%nombreClase, texto, flags=re.IGNORECASE)

        atributos=list(set(atributos))
        metodos=list(set(metodos))
        self.generado=""
        print(atributos)
        print(metodos)
        self.listAtributos=[]
        self.listMetodos=[]
        self.total=0
        self.i=0

        for atributo in atributos:
            if self.text.find("get"+atributo[0].upper()+atributo[1:]+"(")==-1:
                self.listAtributos.append([atributo])
                self.total+=1
        
        for metodo in metodos:
            if self.text.find(metodo)==-1:
                self.listMetodos.append(metodo)
        
        print(self.listAtributos)
        print(self.listMetodos)
        if not self.listAtributos and self.listMetodos:
            self.llenar()
            return
        if not self.listAtributos and not self.listMetodos:return
        self.pedir()

    def pedir(self, value=None):
        window=sublime.active_window()
        if not value:
            atributo=self.listAtributos[self.i][0]
            window.show_input_panel("tipo("+atributo+")", "", self.pedir, None, None)
        else:
            self.listAtributos[self.i].append(value)
            self.i+=1
            if self.i>=self.total:self.llenar()
            else:
                atributo=self.listAtributos[self.i][0]
                window.show_input_panel("tipo("+atributo+")", "", self.pedir, None, None)
    
    def llenar(self):
        strCabecera=""
        strMetodos=""

        for metodo in self.listMetodos:
            strMetodos+="""
    public void %s(){

    }
"""%metodo

        for atributo in self.listAtributos:
            d={"atributo":atributo[0],"tipo":atributo[1],"atributoC":atributo[0][0].upper()+atributo[0][1:]}
            strCabecera+="""
    private %(tipo)s %(atributo)s;"""%d

            self.generado+="""
    public %(tipo)s get%(atributoC)s(){return this.%(atributo)s;}
    public void set%(atributoC)s(%(tipo)s %(atributo)s){this.%(atributo)s=%(atributo)s;}
"""%d
        
        atributosYMetodos=strCabecera+"\n"+strMetodos
        print(self.generado)
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("insertar", {"text":atributosYMetodos})
        view.run_command("insertar", {"text":self.generado, "point":view.find_all("\}")[-1].a})

