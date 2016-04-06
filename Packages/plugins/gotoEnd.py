import sublime_plugin
import sublime

class GotoEndCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        punto=view.sel()[0].b+1
        inicio=view.substr(view.sel()[0].a).strip()
        end=""
        print("el inicio es : "+inicio)
        if inicio=="{":end="}"
        elif inicio=="(":end=")"
        elif inicio=='"':end='"'
        elif inicio=="[":end="]"
        print("el fin es : "+end)
        i=1
        while punto<view.size():
            c=view.substr(sublime.Region(punto, punto+1))
            print(c)
            punto+=1
            if c==end:
                i-=1
                if i==0:
                    print("encontro el fin")
                    break

            if c==inicio:
                i+=1
                continue
        print("i quedo en "+str(i))
        view.run_command("go", {"point":punto})