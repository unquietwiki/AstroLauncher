# pylint: disable=invalid-name,line-too-long,missing-function-docstring

import os
import subprocess
import sys
import time

import psutil


class AstroDaemon():
    """
        Daemon process to watch the Launcher and Dedicated Server
    """

    @staticmethod
    def launch(executable, consolePID):
        if executable:
            daemonCMD = [sys.executable, '--daemon', '-l',
                         str(os.getpid()), '-c', str(consolePID)]
        else:
            daemonCMD = [sys.executable, sys.argv[0], '--daemon',
                         '-l', str(os.getpid()), '-c', str(consolePID)]
        return subprocess.Popen(daemonCMD, shell=False, creationflags=subprocess.DETACHED_PROCESS |
                                subprocess.CREATE_NEW_PROCESS_GROUP)

    @staticmethod
    def daemon(launcherPID, consolePID):
        while(psutil.pid_exists(int(launcherPID)) and psutil.pid_exists(int(consolePID))):
            time.sleep(0.5)
        try:
            process = psutil.Process(int(consolePID))
            for child in process.children(recursive=True):
                try:
                    child.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Wait for graceful termination
            psutil.wait_procs(process.children(recursive=True), timeout=3)

            # Force kill any remaining processes
            for child in process.children(recursive=True):
                try:
                    if child.is_running():
                        child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError) as e:
            print(f"Error terminating child processes: {e}")
