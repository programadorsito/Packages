import sublime_plugin
import sublime
import utils

class CrearConfiguracionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.window=sublime.active_window()
        self.window.show_input_panel("Nombre Configuracion","", self.crear, None, None)

    def crear(self, nombre):
        if not nombre:return
        self.nombre=nombre
        self.window.show_input_panel("Propiedades de conexion", '{"oracle.user":"","oracle.pass":"","oracle.host":"","oracle.port":"","oracle.service":"xe"}', self.registrar, None, None)

    def registrar(self, conexion):
        if not conexion:return
        self.conexion=conexion
        self.registrarConexion()

    def cargarConfiguraciones(self):
        self.configuraciones=utils.load_json(sublime.packages_path()+"/plugins/configuraciones.json")
        if not self.configuraciones:self.configuraciones={}
        
    def guardarConfiguraciones(self):
        utils.save_json(sublime.packages_path()+"/plugins/configuraciones.json", self.configuraciones)

    def registrarConexion(self):
        self.cargarConfiguraciones()
        self.configuraciones[self.nombre]=sublime.decode_value(self.conexion)
        self.guardarConfiguraciones()

class cargarConfiguracionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.window=sublime.active_window()
        self.cargarConfiguraciones()
        self.keys=list(self.configuraciones.keys())
        self.window.show_quick_panel(self.keys, self.configurar)

    def cargarConfiguraciones(self):
        self.configuraciones=utils.load_json(sublime.packages_path()+"/plugins/configuraciones.json")
        if not self.configuraciones:self.configuraciones={}
       
    def configurar(self, index):
        if index==-1:return
        nombre=self.keys[index]
        configuracion=self.configuraciones[nombre]
        for key in configuracion.keys():utils.set_preference(key, configuracion.get(key), "project")
