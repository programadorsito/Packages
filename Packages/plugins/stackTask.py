import os
import utils
import sublime_plugin
import sublime

class StackTask:
    def __init__(self, done=False):
        archivo="tasks.json" if not done else "done.json"
        self.ruta=utils.get_data_path("stackTask"+os.sep+archivo)
    def get(self):
        self.folder=utils.get_folder()
        self.d=utils.load_json(self.ruta)
        if self.d.get(self.folder)==None:self.d[self.folder]=[]
        return self.d[self.folder]

    def save(self):
        utils.save_json(self.ruta, self.d)


class StackTaskAddCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        window.show_input_panel("task", "", self.add, None, None)

    def add(self, task):
        if not task:return
        stack=StackTask()
        tasks=stack.get()
#        tasks.insert(0, task)
        tasks.append(task)
        stack.save()


class StackTaskDone(sublime_plugin.TextCommand):
    def run(self, edit):
        stack=StackTask()
        tasks=stack.get()
        task=tasks.pop()
        stack.save()

        done=StackTask(done=True)
        dones=done.get()
        dones.append(task)
        done.save()
        
        sublime.status_message("Done : "+task)

class StackTaskShow(sublime_plugin.TextCommand):
    def run(self, edit):
        stack=StackTask()
        tasks=stack.get()
        task=tasks[-1]
        sublime.status_message("TODO : "+task)

class StackTaskShowAll(sublime_plugin.TextCommand):
    def run(self, edit):
        stack=StackTask()
        tasks=stack.get()
        window=sublime.active_window()
        window.show_quick_panel(tasks[::-1],None)

class StackTaskShowDone(sublime_plugin.TextCommand):
    def run(self, edit):
        stack=StackTask(done=True)
        tasks=stack.get()
        task=tasks[-1]
        window=sublime.active_window()
        window.show_quick_panel(tasks,None)