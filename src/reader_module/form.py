# -*- coding: utf-8 -*-
from sys import stdout
import pygame
pygame.font.init()
try: import pyca
except: pass

class Form(pygame.Rect,object):

    def __init__(self,pos,width,fontsize,height=None,font=None,bg=(250,250,250),fgcolor=(0,0,0),hlcolor=(180,180,200),curscolor=(0xff0000),maxlines=0):
        if not font: self.FONT = pygame.font.Font(pygame.font.match_font('mono',1),fontsize)
        elif type(font) == str: self.FONT = pygame.font.Font(font,fontsize)
        else: self.FONT = font
        self.BG = bg
        self.FGCOLOR = fgcolor
        self.HLCOLOR = hlcolor
        self.CURSCOLOR = curscolor
        self._line = 0
        self._index = 0
        self.MAXLINES = maxlines
        self._splitted = ['']
        if not height: pygame.Rect.__init__(self,pos,(width,self.FONT.get_height()))
        else: pygame.Rect.__init__(self,pos,(width,height))
        self._x,self._y = pos
        self._src = pygame.display.get_surface()
        self._select = self._line,self._index
        self.TAB = 4
        self._adjust()
        self._cursor = True

    @property   
    def CURSOR(self):
        return self._cursor
    @CURSOR.setter
    def CURSOR(self,value):
        self._cursor = value
    
    @property
    def HLCOLOR(self):
        return None
    @HLCOLOR.setter
    def HLCOLOR(self,color):
        self._hlsurface = pygame.Surface((self._w,self._h),pygame.SRCALPHA)
        self._hlsurface.fill(color)
    
    @property
    def OUTPUT(self):
        return '\n'.join(self._splitted)
    @OUTPUT.setter
    def OUTPUT(self,string):
        self._splitted = string.split('\n')
    
    @property
    def FONT(self):
        return self._font
    @FONT.setter
    def FONT(self,font):
        self._font = font
        self._w,self._h = self._font.size(' ')
    
    @property
    def SELECTION(self):
        p1,p2 = sorted(((self._line,self._index),self._select))
        if p1 != p2:
            selection = [len(i) for i in self._splitted[:p2[0]]]
            return self.OUTPUT[sum(selection[:p1[0]]) + p1[0] + p1[1]:sum(selection) + p2[0] + p2[1]:]
        return ''
                
    def _adjust(self):
        if self._index < len(self._splitted[self._line]):
            rcurs = pygame.Rect(self._x+self._index*self._w,self._y+self._line*self._h,self._w,self._h)
        else:
            rcurs = pygame.Rect(self._x+len(self._splitted[self._line])*self._w,self._y+self._line*self._h,1,self._h)
        
        self._rcursor = rcurs.clamp(self)
        self._x += self._rcursor.x - rcurs.x
        self._y += self._rcursor.y - rcurs.y
    
    def screen(self):
        clip = self._src.get_clip()
        self._src.set_clip(self.clip(clip))
        try: self._src.fill(self.BG,self)
        except: self._src.blit(self.BG,self)
        
        start = (self.top - self._y) / self._h
        end = (self.bottom - self._y) / self._h + 1

        p1,p2 = sorted(((self._line,self._index),self._select))

        y = self._y + start * self._h
        for py,i in enumerate(self._splitted[start:end],start):
            x = self._x
            for px,j in enumerate(i):
                if p1<=(py,px)<p2:
                    self._src.blit(self._hlsurface,(x,y))
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                else:
                    self._src.blit(self._font.render(j,1,self.FGCOLOR),(x,y))
                x += self._w
            y += self._h
        if self._cursor:
            pygame.draw.line(self._src,self.CURSCOLOR,self._rcursor.topleft,self._rcursor.bottomleft,1)
        self._src.set_clip(clip)
    
    def show(self):
        self.screen()
        pygame.display.update(self)
        
    def wakeup(self,ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1: pyca.focus(self)
        self.update(ev)
            
    def update(self,ev):
        
        line,index = self._line,self._index
        shift = pygame.key.get_pressed()
        shift = shift[pygame.K_RSHIFT]|shift[pygame.K_LSHIFT]
        
        def clear():
            p1,p2 = sorted(((self._line,self._index),self._select))
            if p1 != p2:
                selection = [len(i) for i in self._splitted[:p2[0]]]
                self.OUTPUT = self.OUTPUT[:sum(selection[:p1[0]]) + p1[0] + p1[1]] + self.OUTPUT[sum(selection[:p2[0]]) + p2[0] + p2[1]:]
                self._select = self._line,self._index = p1

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RIGHT:
                if self._index < len(self._splitted[self._line]):
                    self._index += 1
                elif self._line < len(self._splitted)-1:
                    self._index = 0
                    self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_LEFT:
                if self._index > len(self._splitted[self._line]):
                    self._index = len(self._splitted[self._line])
                if self._index:
                    self._index -= 1
                elif self._line:
                    self._line -= 1
                    self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
            
            elif ev.key == pygame.K_UP:
                if self._line: self._line -= 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
                
            elif ev.key == pygame.K_DOWN:
                if self._line < len(self._splitted)-1: self._line += 1
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index
                
            elif ev.key == pygame.K_DELETE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]):
                        self._index = len(self._splitted[self._line])
                        self._select = self._line + 1,0
                    else:
                        self._select = self._line,self._index + 1
                clear()
                
            elif ev.key == pygame.K_END:
                self._index = len(self._splitted[self._line])
                if not pygame.mouse.get_pressed()[0] and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_HOME:
                self._index = 0
                if not pygame.mouse.get_pressed()[0] and not shift and not shift: self._select = self._line,self._index

            elif ev.key == pygame.K_BACKSPACE:
                if self._select == (self._line,self._index):
                    if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                    if self._index == 0:
                        if self._line: self._select = self._line - 1,len(self._splitted[self._line - 1])
                    else: self._select = self._line,self._index - 1
                clear()

            elif ev.key == pygame.K_TAB:
                clear()
                sp = self.TAB-self._index%self.TAB
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ' '*sp + self._splitted[self._line][self._index:]
                self._index += sp
                self._select = self._line,self._index

            elif ev.key == pygame.K_RETURN or ev.key == pygame.K_KP_ENTER or ev.unicode == '\n':
                clear()
                if not self.MAXLINES or self.OUTPUT.count('\n') < self.MAXLINES - 1:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + '\n' + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._line += 1
                    self._index = 0
                    self._select = self._line,self._index
                
            elif ev.unicode:
                clear()
                self._splitted[self._line] = self._splitted[self._line][:self._index] + ev.unicode + self._splitted[self._line][self._index:]
                self._index += 1
                self._select = self._line,self._index
                
        elif ev.type == pygame.MOUSEBUTTONDOWN and self.collidepoint(ev.pos):
            if ev.button < 3:
                self._line = (ev.pos[1] - self._y) / self._h
                self._index = (ev.pos[0] - self._x) / self._w
                if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
                if self._line > len(self._splitted)-1:
                    self._line = len(self._splitted)-1
                    self._index = len(self._splitted[self._line])
                if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])
                if ev.button == 2:
                    self._splitted[self._line] = self._splitted[self._line][:self._index] + self.SELECTION + self._splitted[self._line][self._index:]
                    self.OUTPUT = self.OUTPUT
                    self._index += len(self.SELECTION)
                
                self._select = self._line,self._index
            
            elif ev.button == 4:
                y = self._y
                if self._y + self._h*3 > self.top: self._y = self.top
                else: self._y += self._h*3
                self._rcursor.move_ip(0,self._y-y)
                return
                
            elif ev.button == 5:
                y = self._y
                h = len(self._splitted) * self._h
                if h > self.height:
                    if self._y - self._h*3 < self.bottom - h: self._y = self.bottom - h
                    else: self._y -= self._h*3
                    self._rcursor.move_ip(0,self._y-y)
                return
        
        elif ev.type == pygame.MOUSEMOTION and ev.buttons[0] and self.collidepoint(ev.pos):
            self._line = (ev.pos[1] - self._y) / self._h
            self._index = (ev.pos[0] - self._x) / self._w
            if ((ev.pos[0] - self._x) % self._w) > (self._w / 2): self._index += 1
            if self._line > len(self._splitted)-1:
                self._line = len(self._splitted)-1
                self._index = len(self._splitted[self._line])
            if self._index > len(self._splitted[self._line]): self._index = len(self._splitted[self._line])

        if (line,index) != (self._line,self._index):
            self._adjust()
            
if __name__ == '__main__':
    import os.path
    thisrep = os.path.dirname(__file__)
    pygame.display.set_mode((650,300))
    pygame.key.set_repeat(100,25)
    txt = Form((10,10),630,fontsize=15,height=80,bg=pygame.image.load(os.path.join(thisrep,'bg.jpg')),fgcolor=(250,250,250),hlcolor=(250,190,150,50),curscolor=(190,0,10))
    txt.OUTPUT = unicode("""This new version is simpler to use and faster with the great texts,
the constraint being that it only supports monospaced fonts.

There is still plenty of improvement to do.
You can modify this text ...""","utf8")
    txt.show()
    while True:
        if pygame.event.peek(pygame.QUIT): break
        evs = pygame.event.get()
        if evs:
            for ev in evs:
                txt.update(ev)
            txt.show()
    stdout.write(txt.OUTPUT)
    
