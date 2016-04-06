import utils
import sublime_plugin
import sublime
import socket
import sys
import time
import threading 

class ServirViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        HiloServidor().start()

class HiloServidor(threading.Thread):
    def run(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 8888))
        s.listen(15)
        while True:
            con, addr=s.accept()
            con.sendall(bytes(utils.get_text(), 'UTF-8'))
        s.close()