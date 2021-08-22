#!/usr/bin/

import requests
import hashlib
import os, pwd
import time
import subprocess
import platform
import string, random


class ANSI():
    def green_color(self):
        return "\33[92m"

    def red_color(self):
        return "\33[91m"

    def yellow_color(self):
        return "\33[93m"

    def blue_color(self):
        return "\33[94m"
    def reset(self):
        return  "\u001b[0m"


line = ANSI().reset() + "========================================================================================="
strapFileUrl = "https://blackarch.org/strap.sh"


def checkRequirements():
    if os.getuid() != 0:
        print(ANSI().red_color() + "[-] Please run me as root. Quitting ...")
        quit()
    if os.name == 'nt':
        print(ANSI().red_color() + "[-] This program cannot be run on Microsoft Windows. Quitting ...")
        quit()
    if not "arch" in platform.platform():
        print(ANSI().red_color() + "[-] You are not using Arch Linux. Quitting ...")
        quit()
    else:
        pass

def animatedText(text):
    try:
        for x in text:
            print(x, end="", flush=True)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print(ANSI().yellow_color() + "\nCancelling ...")
        quit()

def animatedDots(numberOfDots, end):
    dots = "."
    if end == "":
        dots = dots * numberOfDots
    elif end == "\n":
        dots = dots * numberOfDots + "\n"
    
    for x in dots:
        print(x, end="", flush=True)
        time.sleep(0.5)


def getStrapDotSh():
    ## Get strap.sh
    try:
        print(line)
        animatedText(ANSI().blue_color() + "[i] Downloading strap.sh ...\n")
        strap = requests.get(strapFileUrl)
    except KeyboardInterrupt:
        print(ANSI().yellow_color() + "\nCancelling ...")
        quit()
    except:
        print(ANSI().red_color() + "\n[-] Error downloading strap.sh, please retry.")
        quit()
    
    
    ## Save strap.sh
    path = os.getcwd() + '/strap.sh'
    with open(path, "wb") as file:
        file.write(strap.content)
        file.close()
    return path

def verifyIntegrity(path):
    try:
        print(line)
        animatedText(ANSI().blue_color() + "[i] Verifying integrity ...")
        time.sleep(1)
        def calculateSHA256Sum():
            with open(path, "rb") as file:
                bytes = file.read()
                sha256 = hashlib.sha256(bytes).hexdigest()
            return sha256
        sha256 = calculateSHA256Sum()
        if sha256 == "b80271f6a4daac8430435ddb3d3ff097cd2c28044f4cf8ca8aac4881f5c14bbf":
            print(ANSI().green_color() + "\n[+] Checksums match !")
        else:
            print(ANSI().red_color() + "\n[-] Error ! Checksums do not match ! Please retry.")
            quit()
    except KeyboardInterrupt:
        print(ANSI().yellow_color() + "\nCancelling ...")
        quit()


def execStrap():
    try:
        print(line)
        animatedText(ANSI().blue_color() + "[i] Executing strap.sh ...\n")
        subprocess.call("chmod +x strap.sh", shell=True)
        subprocess.call("./strap.sh", shell=True)
    except KeyboardInterrupt:
        print(ANSI().yellow_color() + "\nCancelling ...")
        quit()

def multilib():
    def enableMultilib():
        # try:
        config = open("/etc/pacman.conf", "r")
        readPacmanConf = config.read()
        config.close()
        try:
            with open("/etc/pacman.conf", "w") as pacmanconf:
                readPacmanConf.replace("#Include = /etc/pacman.d/mirrorlist", "Include = /etc/pacman.d/mirrorlist")
                pacmanconf.write(readPacmanConf)
            animatedText(ANSI().green_color() + "[+] Multilib enabled successfully !")
            time.sleep(1)
        except KeyboardInterrupt:
            print(ANSI().yellow_color() + "\nCancelling ...")
            quit()
        except:
            animatedText(ANSI().red_color() + "[-] Unexpected error. Quitting ...")
            quit()
        
        try:
            animatedText(ANSI().blue_color() + "\n[i] Upgrading system ...\n" + ANSI().reset())
            try:
                subprocess.call("pacman -Syyu", shell=True)
                animatedText(ANSI().green_color() + "[+] System successfully upgraded !")
            except KeyboardInterrupt:
                print(ANSI().yellow_color() + "\nCancelling ...")
                quit()
            except:
                print(ANSI().red_color() + "[-] Unexpected error. Quitting ...")
                quit()
        except KeyboardInterrupt:
            print(ANSI().yellow_color() + "\nCancelling ...")
            quit()

    print(line)
    enableMultilib()
    

def cleanUp():
    animatedText(ANSI().blue_color() + "\n[i] Cleaning up ...\n")
    
    def generateData(length):
        chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.SystemRandom().choice(chars) for i in range(length))

    ld = os.path.getsize("strap.sh")
    with open("strap.sh",  "w") as fh:
        for _ in range(int(38)):
            data = generateData(ld)
            fh.write(data)
            fh.seek(0,  0)
    os.remove("strap.sh")
    print(line)


def main():
    checkRequirements()
    text1 = "Hey there !"
    text2 = "\nPlease follow this program which will install BlackArch tools on you Arch Linux System."
    text3 = "\nLet's start "

    try:
        animatedText(text1)
        time.sleep(1)
        animatedText(text2)
        time.sleep(1)
        animatedText(text3)
        animatedDots(3, end="\n")
    except KeyboardInterrupt:
        print(ANSI().yellow_color() + "\nCancelling ...")
        quit()

    path = getStrapDotSh()
    verifyIntegrity(path)
    execStrap()
    multilib()
    cleanUp()

    text4 = ANSI().green_color() + "\nBlackArch Repositories have been successfully installed on your Arch Linux System !\n"
    text5 = ANSI().green_color() + "Now, you can install any tool you want.\n"
    text6 = ANSI().reset()+ "To list all of the available tools, run : \nsudo pacman -Sgg | grep blackarch | cut -d' ' -f2 | sort -u"
    text7 = "\nTo install all of the tools, run : sudo pacman -S blackarch\n"
    text8 = "To install a category of tools, run : sudo pacman -S blackarch-<category>\n"
    text9 = "To see the blackarch categories, run : sudo pacman -Sg | grep blackarch\n"
    text10 = "Note - it maybe be necessary to overwrite certain packages when installing blackarch tools. \nIf you experience \"failed to commit transaction\" errors, use the --needed and --overwrite switches.\nFor example : sudo pacman -Syyu --needed blackarch --overwrite='*'"

    try:
        animatedText(text4)
        time.sleep(1)
        animatedText(text5)
        time.sleep(1)
        animatedText(text6)
        time.sleep(1)
        animatedText(text7)
        time.sleep(1)
        animatedText(text8)
        time.sleep(1)
        animatedText(text9)
        time.sleep(1)
        animatedText(text10)
        time.sleep(1)
        quit()
    except KeyboardInterrupt:
        print(ANSI().yellow_color() + "\nCancelling ...")
        quit()

main()
