import os
import sublime_plugin
import sublime
import utils
import codecs


class ChangeDbOracleUserClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        self.actual_username=utils.get_preference("oracle.user")
        if not self.actual_username:
            window.show_input_panel("actual username", "", self.setActualUsername, None, None)
        self.new_username=utils.get_preference("oracle.newuser")
        if not self.new_username:
            window.show_input_panel("new username", "", self.setNewUsername, None, None)
        if self.actual_username and self.new_username:
            self.replace()
    
    def setActualUsername(self, username):
        if not username:return
        self.actual_username=username
        window=sublime.active_window()
        window.show_input_panel("new username", "", self.setNewUsername, None, None)

    def setNewUsername(self, username):
        if not username:return
        self.new_username=username
    
    def replace(self):
        text=utils.get_text()
        text=text.replace('"%s"'%(self.actual_username), '"%s"'%(self.new_username))
        text=text.replace("%s."%(self.actual_username), "%s."%(self.new_username))
        sublime.set_clipboard(text)        
    
class JoinAllSqlFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("from:to", "from:to", self.arrancar, None, None)

    def arrancar(self, fromTo):
        if not fromTo:return
        self.actual_username=fromTo[:fromTo.find(":")]
        self.new_username=fromTo[fromTo.find(":")+1:]
        window=sublime.active_window()
        carpeta=window.folders()[0]
        archivos=utils.get_files({"folder":carpeta, "ext":"sql"})
        archivos=sorted(archivos)
        todo=""
        texto=""
        for archivo in archivos:
            print(archivo)
            try:texto="-- archivo : "+archivo+"\n"+utils.file_read(archivo)    
            except:texto="--problema en : "+archivo
            todo+=texto+"\n"
        self.replace(todo)
    
    def replace(self, texto):
        text=texto
        text=text.replace('"%s"'%(self.actual_username), '"%s"'%(self.new_username))
        text=text.replace("%s."%(self.actual_username), "%s."%(self.new_username))
        sublime.set_clipboard(text)        