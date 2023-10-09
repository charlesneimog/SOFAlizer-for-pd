import argparse
import shutil
import sys
import subprocess
import os
import re

linuxLibraries = ["libm.so.6", "linux-vdso.so.1", "libc.so.6", "ld-linux-x86-64.so.2"]

class localdeps:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Local dependencies')
        self.parser.add_argument('-o', '--pdobj', help='File to parse', required=True)
        self.parser.add_argument('-i', '--includes', help='Include directories', required=False)
        self.args = self.parser.parse_args()
        if ".pd_linux" in self.args.pdobj or ".l_amd64" in self.args.pdobj:
            self.parse_linux()

    def parse_linux(self):
        # check if ldd and patchelf are installed
        if shutil.which("ldd") is None or shutil.which("patchelf") is None:
            print("Please install ldd and patchelf")
            sys.exit(1)
            
        command = []
        command.append("ldd")
        command.append(self.args.pdobj)
        ldd = subprocess.run(command, capture_output=True)
        for library_info in ldd.stdout.decode("utf-8").split("\n"):
            systemLibrary = False
            for sysLib in linuxLibraries:
                if sysLib in library_info:
                    systemLibrary = True
                    break
            if systemLibrary:
                continue
            if "not found" in library_info:
                if self.args.includes:
                    pattern = r'(\S+)\s=>'
                    match = re.search(pattern, library_info)
                    libraryFound = False
                    if match:
                        libraryName = match.group(1)
                        print("Searching for " + libraryName)
                        for include in self.args.includes.split(" "):
                            if os.path.exists(include):
                                for root, _, files in os.walk(include):
                                    for file in files:
                                        if file == libraryName:
                                            libraryFound = True
                                            if not os.path.exists("amd64/" + libraryName):
                                                shutil.copy(os.path.join(root, file), "./amd64/" + libraryName)
                        if not libraryFound:
                            print("Library not found: " + libraryName)
                            sys.exit(1)
                        os.system("patchelf --set-rpath \\$ORIGIN/amd64/" + f" {self.args.pdobj}")
            else:
                if not os.path.exists("amd64"):
                    os.mkdir("amd64")
                pattern = r'=>\s(.*?)\s'
                match = re.search(pattern, library_info)
                if match:
                    library = match.group(1)
                    libraryName = library.split("/")[-1]
                    if not os.path.exists("amd64/" + libraryName):
                        shutil.copy(library, "amd64/" + libraryName)
                    os.system("patchelf --set-rpath \\$ORIGIN/amd64/" + f" {self.args.pdobj}")


                    



if __name__ == "__main__":
    localdeps()
        



