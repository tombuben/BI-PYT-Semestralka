#! /usr/bin/python3
# -*- coding: utf-8 -*-
#0000;0000;0000
#0000;****;7/16
#3/16;5/16;1/16
#poměry
from math import *
from tkinter import *
import numpy as np
from PIL import Image, ImageTk


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class aplikace:
    def __init__(self):
        self.okno=Tk()
        self.buttons = Frame(self.okno)

        self.basic = Frame(self.buttons,bd=3,relief=RAISED)
        Grid.columnconfigure(self.basic, 0,weight=1)

        self.dotPrint=Button(self.basic, text="dot",command=self.kresliDobre)
        self.dotPrint.grid(row=0,column=0,sticky=("N", "S", "E", "W"))
        self.threshold=Button(self.basic, text="threshold",command=self.kresliPrah)
        self.threshold.grid(row=1,column=0,sticky=("N", "S", "E", "W"))

        self.dotSlide = Scale(self.basic, from_=2, to=20, orient=HORIZONTAL)
        self.dotSlide.set(2)
        self.dotSlide.grid(row=0,column=1)

        self.thresholdSlide = Scale(self.basic,from_=0, to=255, orient=HORIZONTAL)
        self.thresholdSlide.set(128)
        self.thresholdSlide.grid(row=1,column=1)

        self.brighten = Button(self.basic, text="Brighten",command=self.kresliSvetlost)
        self.brighten.grid(row=0,column=3,sticky=("N", "S", "E", "W"))
        self.brightSlide = Scale(self.basic,from_=-1, to=1, orient=HORIZONTAL, resolution=0.05)
        self.brightSlide.set(0)
        self.brightSlide.grid(row=0,column=4)

        self.inverse = Button(self.basic,text="Invert",command=self.kresliInverse)
        self.inverse.grid(row=1,column=3,sticky=("N", "S", "E", "W"))

        self.basic.grid(row=0,column=0, rowspan=2)

        self.convolution = Frame(self.buttons,bd=3,relief=RAISED)


        self.matrix = [[Entry(self.convolution, width=3) for x in range(3)] for y in range(3)]
        for x in range(3):
            for y in range(3):
                self.matrix[x][y].insert(0,"0")
                self.matrix[x][y].grid(row=x,column=y)

        self.convSide = Frame(self.convolution)

        self.useConv = Button(self.convSide,text="convolute",command=self.kresliMatrix)
        self.useConv.grid(row=0,column=2,sticky=("N", "S", "E", "W"))
        self.divisor = Entry(self.convSide,width=5)
        self.divisor.insert(0,"1")
        self.divisor.grid(row=1,column=2)

        self.convSide.grid(row=0,rowspan=3,column=3)

        self.convolution.grid(row=0,column=1, rowspan=2)


#
        self.presets = Frame(self.convolution)
        self.blur = Button(self.presets,text="blur",command=lambda: self.setMatrix("blur"))
        self.sharpen = Button(self.presets,text="sharpen",command=lambda: self.setMatrix("sharpen"))
        self.edge = Button(self.presets,text="edges",command=lambda: self.setMatrix("edge"))
        self.blur.pack(fill=BOTH)
        self.sharpen.pack(fill=BOTH)
        self.edge.pack(fill=BOTH)
        self.presets.grid(row=0,column=4, rowspan=3)
#
        self.rotate = Frame(self.buttons)
        self.angle = Scale(self.rotate,  from_=-45, to=45, orient=HORIZONTAL)
        self.angle.set(0)
        self.angle.grid(row=0,column=0,columnspan=2)

        self.rotButton = Button(self.rotate, text="rotate",command=self.rotAngle)
        self.rotButton.grid(row=1,column=0,sticky=("N", "S", "E", "W"))

        self.rotButFast = Button(self.rotate, text="fast",command=self.rotFast)
        self.rotButFast.grid(row=1,column=1,sticky=("N", "S", "E", "W"))

        self.rotCCW = Button(self.rotate,text="CCW",command=lambda: self.rot90(-1))
        self.rotCCW.grid(row=2,column=0)

        self.rotCW = Button(self.rotate,text="CW",command=lambda: self.rot90(1))
        self.rotCW.grid(row=2,column=1)

        self.rotate.grid(row=0,column=4, rowspan=2)
#

        self.buttons.pack()

        self.imageSpace = Frame(self.okno)

        self.imagePlatno=Canvas(self.imageSpace,width=512,height=512)
        self.imagePlatno.grid(row=0,column=0)
        self.platno=Canvas(self.imageSpace,width=512,height=512,bg="white")
#        self.platno.grid(rows=0,column=0,rowspan=1,columnspan=2)
        self.platno.grid(row=0,column=1)

        self.imageSpace.pack()


        self.image=Image.open("Lenna.png")
        self.photo=ImageTk.PhotoImage(self.image)
        self.obraz=self.imagePlatno.create_image(256,256,image=self.photo)
        self.pixely=np.asarray(self.image, dtype=np.uint8)   #2D pole hodnot pixelu

        self.pixely2=np.zeros((512,512,3))
    def kresliDobre(self):
        self.pixely2.setflags(write=1)

        l=self.dotSlide.get()-1
        blok = 255/l

        chybadalsi=[0]*512
        chybaradek=[0]*512
        self.pixely2[:,:,0] = self.pixely2[:,:,1] = self.pixely2[:,:,2] = ((self.pixely[:,:,0].astype(np.uint32) + self.pixely[:,:,1] + self.pixely[:,:,2])/3).astype(np.uint8)

        ch=0
        for y in range(512):
            for x in range(512):
                h=chybadalsi[x]+self.pixely2[x,y,0] #Tmavos mezi 0-255
                v=int(round(h/blok)*blok)
                self.pixely2[x,y]=[v,v,v]
                ch=h-v
                if (x<510 and x>0):
                    chybadalsi[x+1]+=round(7/16 *ch)
                    chybaradek[x+1]+=round(1/16 *ch)
                    chybaradek[x]  +=round(5/16 *ch)
                    chybaradek[x-1]+=round(3/16 *ch)
            chybadalsi=chybaradek
            chybaradek=[0]*512

        self.image2 = Image.fromarray(self.pixely2)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)
    
    def kresliPrah(self):
        self.pixely2.setflags(write=1)

        prah = self.thresholdSlide.get()
        # udelat cernobile
        self.pixely2[:,:,0] = self.pixely2[:,:,1] = self.pixely2[:,:,2] = ((self.pixely[:,:,0].astype(np.uint32) + self.pixely[:,:,1] + self.pixely[:,:,2])/3).astype(np.uint8)
        # odecist prah a vynasobit, pak oriznout na 0-255
        self.pixely2 = ((self.pixely2.astype(np.int32)-prah)*255).clip(0,255).astype(np.uint8)
        self.image2 = Image.fromarray(self.pixely2)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def kresliSvetlost(self):
        self.pixely2.setflags(write=1)

        alpha = self.brightSlide.get()
        if 0<alpha:
            self.pixely2 = self.pixely + (alpha*(np.full((512,512,3), 255, dtype=np.uint8) - self.pixely)).astype(np.uint8)
        else:
            self.pixely2 = self.pixely + (alpha*self.pixely).astype(np.uint8)

        self.image2 = Image.fromarray(self.pixely2)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def kresliInverse(self):
        self.pixely2.setflags(write=1)

        self.pixely2 = (np.full((512,512,3), 255, dtype=np.uint8) - self.pixely)
        self.image2 = Image.fromarray(self.pixely2)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def kresliMatrix(self):
        self.pixely2=np.zeros((512,512,3))

        ker = self.getMartix()

        self.pixely2 = self.pixely2.astype(float)
        self.pixely2[1:511,1:511] = ker[0][0]*self.pixely[0:510:,0:510:].astype(float) + ker[0][1]*self.pixely[0:510:,1:511:] + ker[0][2]*self.pixely[0:510:,2:512:] + \
                                    ker[1][0]*self.pixely[1:511:,0:510:]               + ker[1][1]*self.pixely[1:511:,1:511:] + ker[1][2]*self.pixely[1:511:,2:512:] + \
                                    ker[2][0]*self.pixely[2:512:,0:510:]               + ker[2][1]*self.pixely[2:512:,1:511:] + ker[2][2]*self.pixely[2:512:,2:512:]
        self.pixely2 = self.pixely2.clip(0,255).astype(np.uint8)

        self.image2 = Image.fromarray(self.pixely2)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def rotAngle(self):
        self.pixely2.setflags(write=1)

        a=-radians(self.angle.get())
        matrix = np.array([[ cos(a), sin(a)],
                           [-sin(a), cos(a)]])
        for x in range(512):
            for y in range(512):
                vec=np.array([x-255,y-255])
                res=matrix.dot(vec)
                nX=int(res[0]+255)
                nY=int(res[1]+255)
                if 0 <= nX < 512 and 0 <= nY < 512:
                    self.pixely2[x,y] = self.pixely[nX,nY]
                else:
                    self.pixely2[x,y] = (0,0,0)

        self.image2 = Image.fromarray(self.pixely2)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def rotFast(self):
        self.photo2=ImageTk.PhotoImage(self.image.rotate((-self.angle.get())%360))
        self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def rot90(self,direction):
        self.pixely2.setflags(write=1)


        if direction==1:
            self.pixely2 = np.rot90(self.pixely,3)
            self.image2 = Image.fromarray(self.pixely2)
            self.photo2=ImageTk.PhotoImage(self.image2)
            self.obraz2=self.platno.create_image(257,257,image=self.photo2)
        elif direction==-1:
            self.pixely2 = np.rot90(self.pixely)
            self.image2 = Image.fromarray(self.pixely2)
            self.photo2=ImageTk.PhotoImage(self.image2)
            self.obraz2=self.platno.create_image(257,257,image=self.photo2)

    def getMartix(self):
        try:
            if self.divisor.get() != '':
                divisor = float(self.divisor.get())
        except:
            divisor = 1
            print("divisor not numeral")

        if divisor==0:
            divisor = 1
            print("zero divisor, ignoring")

        values=[[0 for x in range(3)] for y in range(3)]

        for x in range(3):
            for y in range(3):
#                self.matrix[x][y].insert(0,"0")
                try:
                    if self.matrix[x][y].get() != '':
                        values[x][y] = int(self.matrix[x][y].get())*1/divisor
                except:
                    values[x][y] = 0
                    print("values not integer")

        return values

    def setMatrix(self,type):
        for x in range(3):
            for y in range(3):
                self.matrix[x][y].delete(0,END)
        self.divisor.delete(0,END)

        if type=="blur":
            mat = [ [1,1,1],
                    [1,1,1],
                    [1,1,1],
                  ]
            self.divisor.insert(0,"9")
        elif type=="sharpen":
            mat = [ [ 0,-1, 0],
                    [-1, 5,-1],
                    [ 0,-1, 0],
                  ]
            self.divisor.insert(0,"1")
        elif type=="edge":
            mat = [ [-1,-1,-1],
                    [-1, 8,-1],
                    [-1,-1,-1],
                    ]
            self.divisor.insert(0,"1")

        for x in range(3):
            for y in range(3):
                self.matrix[x][y].insert(0,str(mat[x][y]))



a=aplikace()
mainloop()
