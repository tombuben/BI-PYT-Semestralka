# -*- coding: utf-8 -*-
#0000;0000;0000
#0000;****;7/16
#3/16;5/16;1/16
#poměry
from tkinter import *
from PIL import Image, ImageTk

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
        self.prah = self.prahejbatko.get();
        for y in range(512):
            for x in range(512):
                h=sum(self.pixely[x,y])/3
                if (h < self.prah):
                    self.pixely2[x,y]=(0,0,0)
                else:
                    self.pixely2[x,y]=(255,255,255)
        self.photo2=ImageTk.PhotoImage(self.image2)
        self.obraz2=self.platno.create_image(768,256,image=self.photo2)

a=aplikace()
mainloop()
