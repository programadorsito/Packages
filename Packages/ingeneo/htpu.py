import os
import sublime
import sublime_plugin
import platform


class HtpuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        os.chdir(sublime.active_window().folders()[0])
        #comando='start /min mvn clean install && timeout /t:15 /NOBREAK && cd Acreditacion-EAR/target && start /min standalone && timeout /t:15 /NOBREAK && jboss-cli "connect,deploy --force Acreditacion-EAR-1.0.ear"'
        comando='mvn -q package -DskipTests && cd Acreditacion-EAR/target && rm -f D:/jboss-eap-6.4/jboss-eap-6.4/standalone/deployments/Acreditacion-EAR-1.0.ear && rm -f D:/jboss-eap-6.4/jboss-eap-6.4/standalone/deployments/Acreditacion-EAR-1.0.ear.deployed && rm -f D:/jboss-eap-6.4/jboss-eap-6.4/standalone/deployments/Acreditacion-EAR-1.0.ear.undeployed && cp Acreditacion-EAR-1.0.ear D:/jboss-eap-6.4/jboss-eap-6.4/standalone/deployments && exit'
        archivo=open(sublime.packages_path()+os.sep+"start.cmd", "w")
        archivo.write(comando)
        archivo.close()
        os.system("start /min "+sublime.packages_path()+os.sep+"start.cmd") 