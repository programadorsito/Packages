import os
import sublime
import sublime_plugin


class GeneradorHibernate:
    def notacionSql(self, word):
        texto=word[0]
        word=word[1:]
        for c in word:
            if c.isupper():texto+="_"
            texto+=c
        return texto.upper()

    def getHibernate(self, linea):
        lineaOriginal=linea
        nombreClase=nombre=linea[:linea.find("{")].strip()
        linea=linea[linea.find("{")+1:-1]
        partes=linea.split(",")
        atributos=[]
        primero=True
        key={}
        for parte in partes:
            parte=parte.strip()
            nombreAtributo=parte[:parte.find(" ")]
            parte=parte[parte.find(" "):].strip()
            if parte.find(" ")!=-1:
                tipo=parte[:parte.find(" ")]
                parte=parte[parte.find(" "):].strip()
            else:
                tipo=parte
                parte=""

            atributo={"nombre":nombreAtributo, "tipo":tipo.lower(), "columna":self.notacionSql(nombreAtributo) ,"sql":parte}
            atributos.append(atributo)
            if primero:
                key=atributo
                primero=False

        txtAtributos=""

        for atributo in atributos:
            if atributo==key:continue
            txtAtributos=txtAtributos+"""
        <property name="%(nombre)s" type="%(tipo)s" column="%(columna)s" />"""%atributo
        txtClave="""
        <id name="%(nombre)s" type="%(tipo)s">
            <column name="%(columna)s" not-null="true" />
            <generator class="increment" />            
        </id>"""%key

        return """
<?xml version="1.0"?>
<!DOCTYPE hibernate-mapping PUBLIC "-//Hibernate/Hibernate Mapping DTD 3.0//EN" "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
<hibernate-mapping>
    <class name="paquete.%(clase)s" table="%(tabla)s">
        %(clave)s
        %(atributos)s
    </class>
</hibernate-mapping>
"""%{"clase":nombreClase, "tabla":self.notacionSql(nombreClase), "atributos":txtAtributos, "clave":txtClave, "linea":lineaOriginal}

class GenerateHibernate(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.status_message("va a generar el archivo hibernate")
        window=sublime.active_window()
        view=window.active_view()
        line=view.line(view.sel()[0].a)
        clase=view.substr(line)
        if not clase:return
        hibernate=GeneradorHibernate().getHibernate(clase)
        print(hibernate)
        view.run_command("replace_from_selection", {"text":hibernate})