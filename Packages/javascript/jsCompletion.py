import sublime_plugin
import sublime
import utils
import re
import os

class JsCompletionListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        print(utils.get_language())
        lang=utils.get_language()
        if lang!="javascript" and lang!="nodejs":return
        if not utils.is_point():return

        jsonPath=sublime.packages_path()+os.sep+"javascript"+os.sep+"functions.json"
        if lang=="nodejs":jsonPath=sublime.packages_path()+os.sep+"javascript"+os.sep+"functions_node.json"

        d=utils.load_json(jsonPath)
        obj=utils.get_word(-1)
        if not d.get(obj):
            d[obj]=[];
            utils.save_json(jsonPath, d)
            return

        functions=d[obj]
        return utils.get_completion_list(functions)

    def on_pre_save(self, view):
        lang=utils.get_language()
        if lang!="javascript" and lang!="nodejs":return
        text=utils.get_text() 

        
        text=re.sub("\$\([\"'.\w#-]*\)", "jQuery", text)
        functions=re.findall("([$A-Za-z]+)\.([\w]+)\(", text)

        jsonPath=sublime.packages_path()+os.sep+"javascript"+os.sep+"functions.json"
        if lang=="nodejs":jsonPath=sublime.packages_path()+os.sep+"javascript"+os.sep+"functions_node.json"

        d=utils.load_json(jsonPath)
        for function in functions:
            key=function[0]
            if key=="$scope":continue
            value=function[1]+"()"
            if not d.get(key):d[key]=[]
            if not value in d[key]:
                d[key].append(value)
        utils.save_json(jsonPath, d)

                