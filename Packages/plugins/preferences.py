import utils
import sublime_plugin
import sublime

class SetPreferenceProjectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        utils.input(self.defKey, "key")

    def defKey(self, key):
        self.key=key
        utils.input(self.defValue, "value")

    def defValue(self, valor):
        utils.set_preference(self.key, valor, "project")

class SetPreferenceUserCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        utils.input(self.defKey, "key")

    def defKey(self, key):
        self.key=key
        utils.input(self.defValue, "value")

    def defValue(self, valor):
        utils.set_preference(self.key, valor, "user")


class ShowPreferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        preferences=utils.get_preferences()
        if(preferences==None):return
        if(preferences.get("user")==None):preferences["user"]={}
        listKeys=list(preferences["user"].keys())
        print("estas son  : ",listKeys)
        for key in preferences["project"].keys():
            print(preferences["project"][key])
            listKeys+=list(preferences["project"][key].keys())
        utils.select(listKeys)
        

                
