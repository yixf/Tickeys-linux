#!/usr/bin/env python
# coding:utf-8

from __future__ import with_statement

import os
import commands

executable_filename = "tickeys"
python2 = os.popen('python2 -V 2>&1').read().startswith('Python 2.') and 'python2' or 'python'
DesktopEntryName = 'Tickeys.desktop'
StartupPath = ['/etc/xdg/autostart', '~/.config/autostart', '~/.config/openbox/autostart']


def check_startup_file():
    return any(
        os.path.isfile(dirname+'/'+DesktopEntryName)
        for dirname in map(os.path.expanduser, StartupPath))


def delete_startup_linux():
    try:
        for dirname in map(os.path.expanduser, StartupPath):
            fileName = dirname+'/'+DesktopEntryName
            if os.path.isfile(fileName):
                os.remove(fileName)
    except Exception:
        return False
    return True


def command_exist(command='gksu'):
    command += ' --help'
    try:
        if commands.getstatusoutput(command)[0] != 32512:
            return True
        else:
            return False
    except Exception:
        return False


def add_startup_linux():
    filename = os.path.abspath(__file__)
    dirname = os.path.dirname(filename)
    command = 'gksu' if command_exist() else 'sudo'

    if dirname.find('library.zip') != -1:
        realPath = dirname.strip('library.zip')
        # In a package
        DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Application;
Path=%s
Exec=%s sh %s
Terminal=true
Icon=%s/tickeys.png
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
''' % (realPath, command, executable_filename, realPath)

    elif command_exist('tickeys'):
        # used pip installed
        DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Application;
Exec=%s /usr/bin/python /usr/local/bin/tickeys
Icon=%s/tickeys.png
Terminal=true
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
''' % (command, dirname)
    else:
        # not install yet(run in py)
        DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Application;
Path=%s
Exec=%s python run.py
Terminal=true
Icon=%s/tickeys.png
Hidden=false
NoDisplay=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
Name=Tickeys
Comment=Instant audio feedback when typing. For Linux.
''' % (dirname, command, dirname)
    try:
        for dirname in map(os.path.expanduser, StartupPath):
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            if os.path.isdir(dirname):
                filename = os.path.join(dirname, DesktopEntryName)
                with open(filename, 'w') as fp:
                    fp.write(DESKTOP_FILE)
                os.chmod(filename, 0777)
    except Exception:
        return False
    return True
