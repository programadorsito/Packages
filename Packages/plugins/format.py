import sublime
import sublime_plugin
class FormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        filename=view.file_name()
        texto=view.substr(sublime.Region(0, view.size()))
        lineas=texto.splitlines()
        newLines=[]
        i=0
        for linea in lineas:
            lineaOriginal=linea
            linea=linea.strip()
            if linea.startswith("<?"):
                newLines.append(linea)
                continue

            if linea.startswith("<!") or linea.startswith("<link ") or linea.startswith("<meta "):
                newLines.append(("\t"*i)+linea)
                continue
            
            if linea.startswith("</") and linea.count("<")==1:
                i-=1
                newLines.append(("\t"*i)+linea)
                continue

            if linea.startswith("<") and linea.endswith("/>"):
                newLines.append(("\t"*i)+linea)
                continue

            if linea.startswith("<") and linea.count("<")==1:
                newLines.append(("\t"*i)+linea)
                i+=1
                continue

            if linea.startswith("<") and linea.find("</")!=-1:
                newLines.append(("\t"*i)+linea)
                continue    

            newLines.append(lineaOriginal)
        print(newLines)
        texto=""
        for linea in newLines:texto+=linea+"\n"
        view.run_command("replace_all", {"text":texto})
