#!/usr/bin/env python
import subprocess
import sys
import pyinotify
import fnmatch
import argparse


class EventCmd(pyinotify.ProcessEvent):
    def __init__(self, pattern, cmd):
        self.cmd = cmd
        self.pattern = pattern

    def _run_cmd(self, cmd):
        print '\033[95m ==> Modification detected \ncmd=%s \033[0m'%(cmd)
        subprocess.call(cmd, shell=True)
        print '\033[95m ==> Waiting modify \033[0m'

    def process_default(self, event):
        pathname = event.pathname
        for p in self.pattern:
            if fnmatch.fnmatch(pathname, p):
               if event.mask & pyinotify.IN_MODIFY:
                   print "%s changed"%(pathname)  + event.maskname 
                   self._run_cmd(self.cmd)
               break

def auto_cmd(path, pattern, cmd):
    print "path: " + path
    print "pattern: " + str(pattern)
    print "cmd: " + cmd
    wm = pyinotify.WatchManager()
    processer = EventCmd(pattern, cmd)
    wm.add_watch(path, pyinotify.ALL_EVENTS, proc_fun=processer, rec=True, auto_add=True)
    print '==> Start monitoring %s (type c^c to exit)' % path
    notifier = pyinotify.Notifier(wm)
    notifier.loop()

if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description="auto run command when file changed")
    parser.add_argument('--path', action='store', required=True, help='path to monitor')
    parser.add_argument('--pattern', action='append', required=True, help='path to monitor')
    parser.add_argument('--cmd', action='store', required=True, help='command to run')
    args = parser.parse_args()
    auto_cmd(args.path, args.pattern, args.cmd) 

