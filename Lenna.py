# -*- coding: utf-8 -*-
#0000;0000;0000
#0000;****;7/16
#3/16;5/16;1/16
#poměry
from tkinter import *
from PIL import Image, ImageTk

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class aplikace:
    def __init__(self):
        self.okno=Tk()
        self.buttons = Frame(self.okno)
#        self.dotPrint=Button(self.buttons, text="kresli Dobře",command=lambda: self.kresliDobre(255))
        self.dotPrint=Button(self.buttons, text="kresli Dobře",command=self.kresliDobre)
        self.dotPrint.grid(row=0,column=0)
        self.threshold=Button(self.buttons, text="kresli Práh",command=self.kresliPrah)
        self.threshold.grid(row=1,column=0)
#        self.bla.pack()
#        self.bla2.pack()

        self.dotSlide = Scale(self.buttons, from_=2, to=20, orient=HORIZONTAL)
        self.dotSlide.set(2)
        self.dotSlide.grid(row=0,column=1)

        self.prahejbatko = Scale(self.buttons,from_=0, to=255, orient=HORIZONTAL)
        self.prahejbatko.set(128)
        self.prahejbatko.grid(row=1,column=1)
#        self.prahejbatko.pack()

        self.brighten = Button(self.buttons, text="Brighten",command=self.kresliSvetlost)
        self.brighten.grid(row=0,column=3)
        self.brightSlide = Scale(self.buttons,from_=-255, to=255, orient=HORIZONTAL)
        self.brightSlide.set(0)
        self.brightSlide.grid(row=0,column=4)

        self.inverse = Button(self.buttons,text="Invert",command=self.kresliInverse)
        self.inverse.grid(row=1,column=3)

        self.convolution = Frame(self.buttons)


        self.matrix = [[Entry(self.convolution) for x in range(3)] for y in range(3)]
        for x in range(3):
            for y in range(3):
                self.matrix[x][y].insert(0,"0")
                self.matrix[x][y].grid(row=x,column=y)


        self.convolution.grid(row=0,rowspan=2,column=5,columnspan=1)

        self.useConv = Button(self.buttons,text="convolute",command=self.kresliMatrix)
        self.useConv.grid(row=0,column=6)
        self.divisor = Entry(self.buttons)
        self.divisor.insert(0,"1")
        self.divisor.grid(row=1,column=6)

#
        self.presets = Frame(self.buttons)
        self.blur = Button(self.presets,text="blur",command=lambda: self.setMatrix("blur"))
        self.sharpen = Button(self.presets,text="sharpen",command=lambda: self.setMatrix("sharpen"))
        self.edge = Button(self.presets,text="edges",command=lambda: self.setMatrix("edge"))
        self.blur.pack()
        self.sharpen.pack()
        self.edge.pack()
        self.presets.grid(row=0,rowspan=2,column=7)
#
        self.rotate = Frame(self.buttons)
        self.angle = Scale(self.rotate,  from_=-45, to=45, orient=HORIZONTAL)
        self.angle.set(0)
        self.angle.grid(row=0,column=0,columnspan=2)

        self.rotButton = Button(self.rotate, text="rotate",command=self.rotAngle)
        self.rotButton.grid(row=1,column=0,columnspan=2)

        self.rotCCW = Button(self.rotate,text="CCW",command=lambda: self.rot90(-1))
        self.rotCCW.grid(row=2,column=0)

        self.rotCW = Button(self.rotate,text="CW",command=lambda: self.rot90(1))
        self.rotCW.grid(row=2,column=1)

        self.rotate.grid(row=0,rowspan=2,column=8)
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
        self.pixely=self.image.load()   #2D pole hodnot pixelu
        self.image2=Image.new("RGB",(512,512),(255,255,255)) #Novej obrázek, celej bílej
        self.pixely2=self.image2.load()
        self.chybadalsi=[0]*512
        self.chybaradek=[0]*512

    def kresliDobre(self):
        l=self.dotSlide.get()-1
        blok = 256.0/l
        ch=0
        for y in range(512):
            for x in range(512):
                h=self.chybadalsi[x]+sum(self.pixely[x,y])/3 #Tmavos mezi 0-255
                v=int(round(h/blok)*blok)
                self.pixely2[x,y]=(v,v,v)
                ch=h-v
                if (x<510 and x>0):
                #   print str(ch)+str("-")+str(round(7/16.0*ch))
                    self.chybadalsi[x+1]+=round(7/16.0*ch)
                    self.chybaradek[x+1]+=round(1/16.0*ch)
                    self.chybaradek[x]+=round(5/16.0*ch)
                    self.chybaradek[x-1]+=round(3/16.0*ch)
            self.chybadalsi=self.chybaradek
            self.chybaradek=[0]*512
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(256,256,image=self.photo2)
        
    def kresliPrah(self):
        self.prah = self.prahejbatko.get()
        for y in range(512):
            for x in range(512):
                h=sum(self.pixely[x,y])/3
                if (h < self.prah):
                    self.pixely2[x,y]=(0,0,0)
                else:
                    self.pixely2[x,y]=(255,255,255)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(256,256,image=self.photo2)

    def kresliSvetlost(self):
        kolik = self.brightSlide.get()
        for y in range(512):
            for x in range(512):
                (r,g,b) = self.pixely[x,y]
                self.pixely2[x,y]=(clamp(r+kolik,0,255),clamp(g+kolik,0,255),clamp(b+kolik,0,255))
                
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(256,256,image=self.photo2)

    def kresliInverse(self):
        for y in range(512):
            for x in range(512):
                (r,g,b) = self.pixely[x,y]
                self.pixely2[x,y]=(255-r,255-g,255-b)
                
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(256,256,image=self.photo2)

    def kresliMatrix(self):
        kernel = self.getMartix()
        for y in range(1,511):
            for x in range(1,511):
                (r,g,b)=(0,0,0)
                for kernelX in range(3):
                    for kernelY in range(3):
                        (r,g,b) = (r + self.pixely[x+kernelX-1,y+kernelY-1][0] * kernel[kernelX][kernelY],
                                   g + self.pixely[x+kernelX-1,y+kernelY-1][1] * kernel[kernelX][kernelY],
                                   b + self.pixely[x+kernelX-1,y+kernelY-1][2] * kernel[kernelX][kernelY],
                                   )
                self.pixely2[x,y]=(clamp(round(r),0,255),clamp(round(g),0,255),clamp(round(b),0,255))

        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(256,256,image=self.photo2)


    def rotAngle(self, angle):
        pass

    def rot90(self,direction):
        if direction==1:
            for y in range(512):
                for x in range(512):
                    self.pixely2[512-1-y,x] = self.pixely[x,y]
            self.photo2=ImageTk.PhotoImage(self.image2)
            self.obraz2=self.platno.create_image(256,256,image=self.photo2)
        elif direction==-1:
            for y in range(512):
                for x in range(512):
                    self.pixely2[y,512-1-x] = self.pixely[x,y]
            self.photo2=ImageTk.PhotoImage(self.image2)
            self.obraz2=self.platno.create_image(256,256,image=self.photo2)




    def getMartix(self):
        try:
            if self.divisor.get() != '':
                divisor = int(self.divisor.get())
        except:
            divisor = 1
            print("divisor not integer")

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
            for x in range(3):
                for y in range(3):
                    self.matrix[x][y].insert(0,"1")
            self.divisor.insert(0,"9")
        elif type=="sharpen":
            self.matrix[0][0].insert(0,"0")
            self.matrix[0][1].insert(0,"-1")
            self.matrix[0][2].insert(0,"0")
            self.matrix[1][0].insert(0,"-1")
            self.matrix[1][1].insert(0,"5")
            self.matrix[1][2].insert(0,"-1")
            self.matrix[2][0].insert(0,"0")
            self.matrix[2][1].insert(0,"-1")
            self.matrix[2][2].insert(0,"0")
            self.divisor.insert(0,"1")
        elif type=="edge":
            self.matrix[0][0].insert(0,"-1")
            self.matrix[0][1].insert(0,"-1")
            self.matrix[0][2].insert(0,"-1")
            self.matrix[1][0].insert(0,"-1")
            self.matrix[1][1].insert(0,"8")
            self.matrix[1][2].insert(0,"-1")
            self.matrix[2][0].insert(0,"-1")
            self.matrix[2][1].insert(0,"-1")
            self.matrix[2][2].insert(0,"-1")
            self.divisor.insert(0,"1")



a=aplikace()
mainloop()
