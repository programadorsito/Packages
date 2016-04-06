import sublime_plugin
import sublime
import utils
import os

class SampleSaveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lang=utils.get_language()
        self.rutaSamples= os.path.normpath(os.path.join(sublime.packages_path(), "..", "samples", lang+".json"))
        print("la ruta es : "+self.rutaSamples)
        if not os.path.exists(self.rutaSamples):
            utils.file_write(self.rutaSamples, "{}")
        window=sublime.active_window()
        window.show_input_panel("sample name", "", self.save, None, None)
    
    def save(self, name):
        if name==None:return
        print("antes de : "+self.rutaSamples)
        samples=utils.load_json(self.rutaSamples)
        samples[name]=utils.get_text()
        utils.save_json(self.rutaSamples, samples)


class SampleLoadCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lang=utils.get_language()
        self.rutaSamples=os.path.normpath(os.path.join(sublime.packages_path(), "..", "samples", lang+".json"))
        print("la ruta es : "+self.rutaSamples)
        if not os.path.exists(self.rutaSamples):
            return
        self.samples=utils.load_json(self.rutaSamples)
        self.keys=list(self.samples.keys())
        window=sublime.active_window()
        window.show_quick_panel(self.keys,self.load)

    def load(self, item):
        if item==-1:return
        key=self.keys[item]
        text=self.samples[key]
        utils.set_text(text)