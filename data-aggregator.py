#!/usr/bin/env python
import csv, os, Tkinter, tkFileDialog
from Tkinter import *
from itertools import izip

#File Directory Basics
root = Tkinter.Tk()
dirname = tkFileDialog.askdirectory(parent=root, initialdir="/", title='Please select a directory (simdata "date")')
os.chdir(dirname)

#Input CADRI ID#
class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Enter CADRI ID number only:").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
    def ok(self):
        global CADRI
        CADRI = self.e.get()
        self.top.destroy()
d = MyDialog(root)
root.wait_window(d.top)

#Output file
fout = open('Output.csv', 'w')
heading = "heading,OP(37),OP(25),.,SH(37),SH(38),SH(25),.,SMVH(54),ReTH(69),RiTH(69)\n"
fout.writelines(heading)

#Go into scenario folder
def scenario(scene):
    os.chdir(dirname+'\scenario %d' % scene)
    print os.path.abspath(os.curdir)
    key_index = 0 #column for ID
    PM = csv.reader(open('performance monitor.csv', 'rb'))
    for rownum, row in enumerate(PM):
        if row[key_index] == CADRI:
            OP1,OP2 = row[36],row[24]
            break
        else:
            OP1,OP2 = 'empty','empty'
    NT = csv.reader(open('no traffic.csv', 'rb'))
    for rownum, row in enumerate(NT):
        if row[key_index] == CADRI:
            SH1,SH2,SH3 = row[36],row[37],row[24]
            break
        else:
            SH1,SH2,SH3 = 'empty','empty','empty'
    HT = csv.reader(open('heavy traffic.csv', 'rb'))
    for rownum, row in enumerate(HT):
        if row[key_index] == CADRI:
            SMVH = row[53]
            break
        else:
            SMVH = 'empty'
    if (scene <= 3) or (scene == 8):
        H2 = csv.reader(open('h2 start.csv', 'rb'))
        for rownum, row in enumerate(H2):
            if row[key_index] == CADRI:
                ReTH = row[68]
                break
            else:
                ReTH = 'empty'
        H1 = csv.reader(open('h1 start.csv', 'rb'))
        for rownum, row in enumerate(H1):
            if row[key_index] == CADRI:
                RiTH = row[68]
                break
            else:
                RiTH = 'empty'
    elif (4 <= scene <=7):
        H1 = csv.reader(open('h1 start.csv', 'rb'))
        for rownum, row in enumerate(H1):
            if row[key_index] == CADRI:
                ReTH = row[68]
                break
            else:
                ReTH = 'empty'
        H2 = csv.reader(open('h2 start.csv', 'rb'))
        for rownum, row in enumerate(H2):
            if row[key_index] == CADRI:
                RiTH = row[68]
                break
            else:
                RiTH = 'empty'
    scene_data_list = "S%d" % scene,OP1,OP2,".",SH1,SH2,SH3,".",SMVH,ReTH,RiTH,"\n"
    data_string = ','.join(str(x) for x in scene_data_list)
    fout.writelines(data_string)
    os.chdir('..') #move up 1 directory

i = 1
for i in range(1,4):
    scenario(i)
    i += 1

scenario(4)
scenario(5)
scenario(6)
scenario(7)
scenario(8)

fout.close()

#Pivot list
a = izip(*csv.reader(open("Output.csv", "rb")))
csv.writer(open("Output CADRI%s.csv" % CADRI, "wb")).writerows(a)

fout.close()
os.remove('Output.csv')

# os.chdir('..') #move up 1 directory
# print os.path.abspath(os.curdir)
