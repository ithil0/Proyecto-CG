from cmath import e
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

vertex= [(0,0),(0,1),(1,1),(1,0),
         (-1,0),(-1,1),(0,2),(1,2)]
aristas=((0,1,2,3),
         (0,4,5,1),
         (1,6,7,2))
         
colors=((1,0,1),
        (1,1,0),
        (0,1,1),
        (1,0,0),
        (0,0,1),
        (0,1,0),
        (1,0,1),
        (1,1,0),
        (1,1,1))

texturas=[]

def load_texture(texture): 
    image = pg.image.load(texture)  
    img_data = pg.image.tostring(image, "RGBA",1)
    image_width, image_height = image.get_rect().size
    glEnable(GL_TEXTURE_2D)
    textura = glGenTextures(1) 
    glBindTexture(GL_TEXTURE_2D, textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  
    
    return textura

def tex():
    global texturas
    texturas.append(load_texture('red.png'))
    texturas.append(load_texture('green.png'))
    texturas.append(load_texture('yellow.png'))
    texturas.append(load_texture('left.jpg'))
    texturas.append(load_texture('right.png'))
    texturas.append(load_texture('paper.png'))
    texturas.append(load_texture('tij.jpg'))
    texturas.append(load_texture('rock.jpg'))
    texturas.append(load_texture('tie.png'))

class Cube:
    def __init__(self, vertices, aristas, colores, texturas):
        self.vertexs = vertices
        self.edges = aristas
        self.colors = colores
        self.texturas=texturas
        self.coords=[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]]
        self.gamet=[0,1,2]
    
    def inicio(self):        
        for i in range(3):
            #glPushMatrix()
            glEnable(GL_TEXTURE_2D) 
            #glTranslatef(*[0, 0, 0])
            glBindTexture(GL_TEXTURE_2D, self.texturas[self.gamet[i]])
            glBegin(GL_QUADS)
            #x=x+1
            #glColor3fv(self.colors[x])            
            for j in range(4):
                glTexCoord2f(self.coords[j][0],self.coords[j][1])
                glVertex2f(self.vertexs[self.edges[i][j]][0],self.vertexs[self.edges[i][j]][1])      
          
            glEnd()
    
    def dibujar(self):
        self.keys=pg.key.get_pressed()        
        a=random.choice(range(2,5))
        d=random.choice(range(2,5))
        if self.keys[K_a]:
            glEnable(GL_TEXTURE_2D) 
            glBindTexture(GL_TEXTURE_2D, self.texturas[a])
            glBegin(GL_QUADS)
            for j in range(4):
                glTexCoord2f(self.coords[j][0],self.coords[j][1])
                glVertex2f(self.vertexs[self.edges[1][j]][0],self.vertexs[self.edges[1][j]][1])
            glEnd()
        if self.keys[K_d]:
            glEnable(GL_TEXTURE_2D) 
            glBindTexture(GL_TEXTURE_2D, self.texturas[d])
            glBegin(GL_QUADS)
            for j in range(4):
                glTexCoord2f(self.coords[j][0],self.coords[j][1])
                glVertex2f(self.vertexs[self.edges[0][j]][0],self.vertexs[self.edges[0][j]][1])
            glEnd()
       
       
    
    def update(self):      
        #self.keys=pg.key.get_pressed()  
        #if self.keys[K_a]:
         #   self.gamet[1]=random.choice(range(5,8))     
        #self.event=pg.event.get()  
        #if self.event.key==pg.K_a:
        #    self.gamet[1]=random.choice(range(5,8))


        self.mouse=pg.mouse.get_pressed()
        pos=pg.mouse.get_pos()
        x=(int(pos[0])-490)/60
        y=(490-int(pos[1]))/60
        #print(x,y)
        for v1,v2 in self.vertexs:
            if abs(x-v1)<0.5 and abs(y-v2)<0.5 and self.mouse[0]:
                index = self.vertexs.index((v1,v2))             
                self.vertexs[index]=(x,y)
                
   
def main():
    pg.init()
    rockSound = pg.mixer.Sound("rock.wav")
    paperSound = pg.mixer.Sound("paper.wav")
    tijSound = pg.mixer.Sound("scissors.wav")
    #glMatrixMode(GL_PROJECTION)
    display=(980,980)
    pg.display.set_mode(display,pg.DOUBLEBUF|pg.OPENGL)
    gluPerspective(60,display[0]/display[1],1,150)
    #glMatrixMode(GL_MODELVIEW)
    glTranslatef(0,0.0,-15)
    #glRotatef(45,0,1,0)
    objeto=Cube(vertex,aristas,colors,texturas)  
    programa=True  
    ini=True
    tex()
    a=-1
    d=-2    
    while programa:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                quit()
            if event.type==pg.KEYDOWN:                
                if event.key==pg.K_a:
                    a=random.choice(range(5,8))
                    objeto.gamet[1]=a
                    if a==5:
                        paperSound.play()     
                    if a==6:
                        tijSound.play()
                    if a==7:
                        rockSound.play()               
                if event.key==pg.K_d:
                    d=random.choice(range(5,8))
                    objeto.gamet[0]=d
                    if d==5:
                        paperSound.play()     
                    if d==6:
                        tijSound.play()
                    if d==7:
                        rockSound.play()
                if a==d:
                    objeto.gamet[2]=8
                if (a==5 and d==6) or (a==6 and d==7) or (a==7 and d==5):
                    objeto.gamet[2]=4
                if (a==5 and d==7) or (a==6 and d==5) or (a==7 and d==6):
                    objeto.gamet[2]=3
                if event.key==pg.K_r:                    
                    objeto.gamet[0]=0
                    objeto.gamet[1]=1
                    objeto.gamet[2]=2
                    a=-1
                    d=-2
                
                if event.key==pg.K_ESCAPE:
                    programa=False           
        
        objeto.update()
                

        glEnable( GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #if ini==True:
           # objeto.inicio()
        objeto.inicio()
        pg.display.flip()
        pg.time.wait(10)
main()