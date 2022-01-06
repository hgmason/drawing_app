#built in
import time
import random
import colorsys
import os
from math import *
from io import BytesIO


#not built in and not fixed
import pygame, sys
from pygame.locals import *
import win32clipboard
from PIL import Image

#brush picker
class BrushPicker:
    def __init__(self, windowSurface, window_size, horz_offset = 0, vert_offset = 0):
        #constants
        self.window_size = window_size
        self.height = int(self.window_size*1.3)
        self.actual_height = int(self.height*.8)
        self.width = int(self.window_size)
        self.MOUSE_DOWN = MOUSEBUTTONDOWN
        self.MOUSE_UP = MOUSEBUTTONUP
        self.MOUSE_MOVE = MOUSEMOTION
        self.SPACE = 32
        self.pressed = False
        self.windowSurface = windowSurface
        self.horz_offset = horz_offset
        self.vert_offset = vert_offset
        self.section_height = self.height//7
        self.spacing = (self.height - self.section_height*6)//5
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.GREEN = (0, 255, 0)
        self.PINK = (255, 56, 215)

        #not constants
        self.type = 0 #0 = cirle, 1 = square
        self.eraser = 0 #0 = no, 1 = yes
        self.size = 1 #sizes are 1-6
        self.size_boxes = []
        #self.brush_scalars = [1,2,3,4,5,6]
        self.brush_scalars = [1,3,5,7,10,15]
        self.min_brush = int(5 * self.window_size/510)
        self.circ_type = [0,0,0] #x,y,rad
        self.rec_type = Rect(0,0,0,0) #left, top, width, height
        self.era_type = Rect(0,0,0,0) #left, top, width, height

        #setup
        self.brush_size = self.min_brush*self.brush_scalars[self.size-1]
        self.draw()
        return
    def draw(self):
        self.draw_background()
        self.draw_border()
        #draw "type" text
        X = self.window_size//2 + self.horz_offset
        Y = self.vert_offset + (self.spacing*3)//2
        font = pygame.font.Font('freesansbold.ttf', int(32 * self.window_size / 255.0 / 2))
        text = font.render("TYPE", True, self.BLACK, self.WHITE)
        textRect = text.get_rect()
        textRect.center = (X, Y)
        self.windowSurface.blit(text, textRect)
        #draw the circle option
        demo_size = int(self.section_height/2*.8)
        y = int(self.vert_offset + (self.spacing*3)//2 + self.section_height*2/3)
        x = int(self.horz_offset + self.window_size/2*2/3/1.5)
        if self.type == 0 and self.eraser == 0:
            pygame.draw.circle(self.windowSurface, (128,128,0), (x,y), demo_size, 0)
        else:
            pygame.draw.circle(self.windowSurface, self.BLACK, (x,y), demo_size, 0)
        self.circ_type = x,y,demo_size
        #draw the rectangle
        top = int(self.vert_offset + (self.spacing*3)//2 + self.section_height*2/3 - demo_size)
        left = int(self.window_size/2 + self.horz_offset - demo_size)
        self.rec_type = Rect(left, top, demo_size*2, demo_size*2)
        if self.type == 1 and self.eraser == 0:
            pygame.draw.rect(self.windowSurface, (128,128,0), self.rec_type, 0)
        else:
            pygame.draw.rect(self.windowSurface, self.BLACK, self.rec_type, 0)
        #draw the eraser option
        if self.type == 1:
            top = int(self.vert_offset + (self.spacing*3)//2 + self.section_height*2/3 - demo_size)
            left = int(self.window_size/2 + self.horz_offset - demo_size + self.width/3.5)
            self.era_type = Rect(left, top, demo_size*2, demo_size*2)
            if self.eraser == 1:
                pygame.draw.rect(self.windowSurface, (128,128,0), self.era_type, int(5*self.window_size/510))
            else:
                pygame.draw.rect(self.windowSurface, self.BLACK, self.era_type, int(5*self.window_size/510))
        else:
            y = int(self.vert_offset + (self.spacing*3)//2 + self.section_height*2/3)
            x = int(self.window_size/2 + self.horz_offset + self.width/3.5)
            self.era_type = [x,y,demo_size]
            if self.eraser == 1:
                pygame.draw.circle(self.windowSurface, (128,128,0), (x,y), demo_size, int(5*self.window_size/510))
            else:
                pygame.draw.circle(self.windowSurface, self.BLACK, (x,y), demo_size, int(5*self.window_size/510))
        #draw the "size" text
        X = self.window_size//2 + self.horz_offset
        Y = self.vert_offset + (self.spacing*6)//2 + self.section_height
        font = pygame.font.Font('freesansbold.ttf', int(32 * self.window_size / 255.0 / 2))
        text = font.render("SIZE", True, self.BLACK, self.WHITE)
        textRect = text.get_rect()
        textRect.center = (X, Y)
        self.windowSurface.blit(text, textRect)
        #draw the sizes
        self.size_boxes = []
        count = 1
        ii = [0,1,0,1,0,1]
        jj = [0,0,1,1,2,2]
        for j in range(3):
            for i in range(2):
                if self.type == 0:
                    radius = self.min_brush*self.brush_scalars[count-1]
                    demo_size = int(self.section_height/2*.8)
                    y = int(self.vert_offset + (self.spacing*3)//2 + self.section_height*(6 + 4*j)/3)
                    x = int(self.horz_offset + self.window_size/2*2/3*(1 + i))
                    if count != self.size:
                        pygame.draw.circle(self.windowSurface, self.BLACK, (x,y), radius, 0)
                    else:
                        pygame.draw.circle(self.windowSurface, (128,128,0), (x,y), radius, 0)
                    self.size_boxes.append([x,y,radius])
                else:
                    size = self.min_brush*self.brush_scalars[count-1]
                    demo_size = int(self.section_height/2*.8)
                    top = int(self.vert_offset + (self.spacing*3)//2 + self.section_height*(6 + 4*j)/3 - size)
                    left = int(self.horz_offset + self.window_size/2*2/3*(1 + i) - size)
                    rec_type = Rect(left, top, size*2, size*2)
                    if count != self.size:
                        pygame.draw.rect(self.windowSurface, self.BLACK, rec_type, 0)
                    else:
                        pygame.draw.rect(self.windowSurface, (128,128,0), rec_type, 0)
                    self.size_boxes.append(rec_type)
                count = count + 1
        return

    def draw_background(self):
        rect = Rect(self.horz_offset,self.vert_offset, self.width, int(self.height*.8))
        pygame.draw.rect(self.windowSurface, (255,255,255), rect)
        return

    def handle_event(self, event):
        within_bound = False
        if event.type == self.MOUSE_DOWN or event.type == self.MOUSE_UP or event.type == self.MOUSE_MOVE:
            pos = event.pos
            within_bound = pos[1] >= self.vert_offset and pos[1] <= (self.height*.8 + self.vert_offset) and pos[0] >= self.horz_offset and pos[0] <= (self.horz_offset + self.width)
        if event.type == self.MOUSE_DOWN:
            done = False
            pos = event.pos
            if pos[1] >= self.vert_offset and pos[1] <= (self.height*.8 + self.vert_offset) and pos[0] >= self.horz_offset and pos[0] <= (self.horz_offset + self.width):
                if self.circ_overlap(self.circ_type, pos):
                    self.type = 0
                    self.eraser = 0
                    done = True
                elif self.rect_overlap(self.rec_type, pos):
                    self.type = 1
                    self.eraser = 0
                    done = True
                elif self.type == 0:
                    if self.circ_overlap(self.era_type, pos):
                        self.eraser = 1
                        done = True
                elif self.type == 1:
                    if self.rect_overlap(self.era_type, pos):
                        self.eraser = 1
                        done = True
                if not done:
                    rad = self.min_brush*self.brush_scalars[5]
                    for i in range(len(self.size_boxes)):
                        if not done:
                            if self.type == 0:
                                if self.circ_overlap(self.size_boxes[i],pos, rad = rad):
                                    self.size = i + 1
                                    done = True
                            if self.type == 1:
                                if self.rect_overlap(self.size_boxes[i],pos, rad = rad):
                                    self.size = i + 1
                                    done = True
            #update the things
            self.brush_size = self.min_brush*self.brush_scalars[self.size-1]
            self.draw()
            pygame.display.update()

        return within_bound

    def draw_border(self):
        for i in range(int(10 * self.window_size/255)):
            border_rect = Rect(self.horz_offset - i,self.vert_offset - i, self.width + i*2, int(self.height * .8)+i*2)
            pygame.draw.rect(self.windowSurface, (0,0,0), border_rect, 1)
        return

    def millis(self):
        return time.time()*1000

    def circ_overlap(self, circ, pos, rad = None):
        diff = sqrt((pos[0] - circ[0])**2 + (pos[1] - circ[1])**2)
        if rad:
            return diff <= rad
        else:
            return diff <= circ[2]

    def rect_overlap(self, rect, pos, rad = None):
        if rad == None:
            if pos[0] < rect[0]:
                return False
            if pos[1] < rect[1]:
                return False
            if pos[0] > rect[0] + rect[2]:
                return False
            if pos[1] > rect[1] + rect[3]:
                return False
        else:
            centerx = rect[0] + rect[2]/2
            centery = rect[1] + rect[3]/2
            if abs(pos[0] - centerx) > rad:
                return False
            if abs(pos[1] - centery) > rad:
                return False
        return True

#color picker
class ColorPicker:
    def __init__(self, windowSurface, resolution, scalar, horz_offset = 0, vert_offset = 0):
        #constants
        self.resolution = resolution
        self.scalar = scalar
        self.window_size = int(self.resolution*self.scalar)
        self.height = int(self.window_size*1.3)
        self.width = int(self.window_size)
        self.size = self.window_size
        self.MOUSE_DOWN = 1025
        self.MOUSE_UP = 1026
        self.MOUSE_MOVE = 1024
        self.SPACE = 32
        self.pressed = False
        self.windowSurface = windowSurface
        self.horz_offset = horz_offset
        self.vert_offset = vert_offset

        #not constants
        self.hue = 0; #between 0 and 1
        self.sat = 1; #between 0 and 1
        self.val = 1; #between 0 and 1
        self.color = [255,0,0]
        self.main_rect = Rect(self.horz_offset,self.vert_offset, self.size, self.size)
        self.satval_pos = (self.size + horz_offset, self.vert_offset)
        self.hue_pos = (self.horz_offset, self.vert_offset + int(self.size*1.05))

        #setup stuff
        self.draw_satval_square()
        self.draw_hue_rect()
        self.draw()
        self.adjusting_hue = False
        self.adjusting_satval = False
        self.start = self.millis()
        self.thresh = 500
        return
    def draw_all(self):
        self.draw_satval_square()
        self.draw_hue_rect()
        self.draw_border()
        self.draw_satval_pointer()
        self.draw_hue_pointer()
    def draw(self):
        color = colorsys.hsv_to_rgb(self.hue, self.sat, self.val)
        self.color = [int(c*255) for c in color]
        bottom_rect = Rect(self.horz_offset,self.vert_offset + int(self.size*1.1), self.size, int(self.size*.2))
        pygame.draw.rect(self.windowSurface, (0,0,0), bottom_rect)
        bottom_rect = Rect(self.horz_offset,self.vert_offset + int(self.size*1.1 + 5), self.size, int(self.size*.2 - 5))
        pygame.draw.rect(self.windowSurface, self.color, bottom_rect)
        X = self.size//2 + self.horz_offset
        Y = int(self.size*1.3 - self.size*.1) + self.vert_offset
        font = pygame.font.Font('freesansbold.ttf', int(32 * self.size / 255.0 / 2))
        RGBval = sum(self.color)/3/255
        #if self.val < .6 or self.sat > .5:
        if RGBval < .5:
            text = font.render(str(self.color).replace("[","(").replace("]",")"), True, (255,255,255), self.color)
        else:
            text = font.render(str(self.color).replace("[","(").replace("]",")"), True, (0,0,0), self.color)
        textRect = text.get_rect()
        textRect.center = (X, Y)
        self.windowSurface.blit(text, textRect)
        self.draw_border()
        self.draw_hue_pointer()
        self.draw_satval_pointer()
        return
    def adjust_hue(self, pos):
        #draw over the previous pos
        self.cover_hue_pointer()
        #update the new stuff
        new_hue = (pos[0] - self.horz_offset)/self.size
        if new_hue >= 0 and new_hue <= 1:
            self.hue = new_hue
            self.hue_pos = pos
        return
    def adjust_satval(self, pos):
        #draw over the previous pos
        self.cover_satval_pointer()
        #update the new stuff
        new_sat = (pos[0] - self.horz_offset)/self.size
        new_val = 1 - (pos[1] - self.vert_offset)/self.size
        if new_sat >= 0 and new_sat <= 1 and new_val >=0 and new_val <= 1:
            self.sat = new_sat
            self.val = new_val
            self.satval_pos = pos
        return
    def draw_hue_pointer(self):
        pygame.draw.circle(self.windowSurface, (0,0,0), self.hue_pos, self.size//255 + int(6 * self.window_size/255), 0)
        pygame.draw.circle(self.windowSurface, (255,255,255), self.hue_pos, self.size//255 + int(5 * self.window_size/255), 0)
        pygame.draw.circle(self.windowSurface, self.color, self.hue_pos, self.size//255 + int(3 * self.window_size/255), 0)
        return
    def draw_satval_pointer(self):
        temp_pos = (self.satval_pos[0], self.satval_pos[1])
        pygame.draw.circle(self.windowSurface, (0,0,0), temp_pos, self.size//255 + int(6 * self.window_size/255), 0)
        pygame.draw.circle(self.windowSurface, (255,255,255), temp_pos, self.size//255 + int(5 * self.window_size/255), 0)
        pygame.draw.circle(self.windowSurface, self.color, temp_pos, self.size//255 + int(3 * self.window_size/255), 0)
        return
    def cover_hue_pointer(self):
        x_res = int((self.hue_pos[0] - self.horz_offset)/self.size * self.resolution)
        replace_size = 8 * (255*2) // self.window_size
        slice_width = self.size//self.resolution
        for i in range(x_res - replace_size, x_res + replace_size + 1):
            if i >= 0 and i < 256:
                hue = i/255.0 * 255.0/self.resolution
                color = colorsys.hsv_to_rgb(hue, 1, 1)
                color = [int(c*255) for c in color]
                slice_rect = Rect(slice_width*i+self.horz_offset,self.size+self.vert_offset, slice_width, int(self.size*.1))
                pygame.draw.rect(self.windowSurface, color, slice_rect)
        return
    def cover_satval_pointer(self):
        x_res = int((self.satval_pos[0] - self.horz_offset)/self.size * self.resolution)
        y_res = int(self.resolution - (self.satval_pos[1] - self.vert_offset)/self.size * self.resolution)
        replace_size = 8 * (255*2) // self.window_size
        pixel_width = self.size//self.resolution
        for i in range(x_res - replace_size, x_res + replace_size + 1):
            for j in range(y_res - replace_size, y_res + replace_size + 1):
                if i >= 0 and j >= 0 and i < 256 and j < 256:
                    hue = self.hue * 255.0/self.resolution
                    sat = i/255.0 * 255.0/self.resolution
                    val = j/255.0 * 255.0/self.resolution
                    color = colorsys.hsv_to_rgb(hue, sat, val)
                    color = [int(c*255) for c in color]
                    if max(color) < 255 and min(color) >= 0:
                        pixel_rect = Rect(pixel_width*(i)+self.horz_offset,pixel_width*(self.resolution-j)+self.vert_offset, pixel_width, pixel_width)
                        pygame.draw.rect(self.windowSurface, color, pixel_rect)
        return
    def draw_satval_square(self, resolution_scalar = 1):
        temp_res = int(self.resolution*resolution_scalar)
        pixel_width = self.size//temp_res
        for i in range(temp_res+1):
            for j in range(temp_res+1):
                hue = self.hue * 255.0/temp_res
                sat = i/255.0 * 255.0/temp_res
                val = j/255.0 * 255.0/temp_res
                color = colorsys.hsv_to_rgb(hue, sat, val)
                color = [int(c*255) for c in color]
                pixel_rect = Rect(pixel_width*(i)+ self.horz_offset,pixel_width*(temp_res-j)+ self.vert_offset, pixel_width, pixel_width)
                pygame.draw.rect(self.windowSurface, color, pixel_rect)
        return
    def draw_hue_rect(self):
        slice_width = self.size//self.resolution
        for i in range(self.resolution+1):
            hue = i/255.0 * 255.0/self.resolution
            color = colorsys.hsv_to_rgb(hue, 1, 1)
            color = [int(c*255) for c in color]
            slice_rect = Rect(slice_width*i+ self.horz_offset,self.size+ self.vert_offset, slice_width, int(self.size*.1))
            pygame.draw.rect(self.windowSurface, color, slice_rect)
        return
    def handle_event(self, event):
        #ret = (pos[0] >= self.horz_offset and pos[0] <= (self.horz_offset+self.width) and pos[1] >= self.vert_offset and pos[1] <= (self.vert_offset + self.height))
        within_bound = False
        if event.type == self.MOUSE_DOWN or event.type == self.MOUSE_UP or event.type == self.MOUSE_MOVE:
            pos = event.pos
            within_bound = (pos[0] >= self.horz_offset and pos[0] <= (self.horz_offset+self.width) and pos[1] >= self.vert_offset and pos[1] <= (self.vert_offset + self.height))
        if within_bound:
            if event.type == self.MOUSE_DOWN or (self.MOUSE_MOVE and self.pressed):
                self.pressed = True
                pos = event.pos
                if pos[1] >= self.vert_offset:
                    if pos[1] > (self.size + self.vert_offset) and pos[1] < (self.size*1.1 + self.vert_offset):
                        self.adjusting_hue = True
                        self.adjusting_satval = False
                        self.adjust_hue(pos)
                        self.draw_satval_square()
                    elif pos[1] < (self.size + self.vert_offset):
                        self.adjusting_hue = False
                        self.adjusting_satval = True
                        self.adjust_satval(pos)
                        if pos[1] > (self.size - 100*self.window_size//(255*2) + self.vert_offset):
                            self.draw_hue_rect()
                            self.draw_hue_pointer()
            if event.type == self.MOUSE_UP:
                self.pressed = False
                pos = event.pos

        #update the things
        self.draw()
        pygame.display.update()
        return within_bound

    def draw_border(self):
        for i in range(int(10 * self.window_size/255)):
            border_rect = Rect(self.horz_offset - i,self.vert_offset - i, self.width + i*2, self.height+i*2)
            pygame.draw.rect(self.windowSurface, (0,0,0), border_rect, 1)
        return

    def millis(self):
        return time.time()*1000

#constants
MOUSE_DOWN = 1025
MOUSE_UP = 1026
MOUSE_MOVE = 1024
pressed = False
drawing = False
last_drawn_pos = (0,0)

# set up pygame
pygame.init()

# set up the window
width = 1000
height = 700
windowSurface = pygame.display.set_mode((width, height), 0, 32)
windowSurface.fill((255,255,255))
pygame.display.set_caption('drawing ^-^')

#functions
def draw_gap():
    gap_rect = Rect(sidebar_width,0,gap_width,height)
    pygame.draw.rect(windowSurface, (0,0,0), gap_rect)

# draw the background onto the surface
sidebar_width = 255+9*2
sidebar_rect = Rect(0,0,sidebar_width,height)
pygame.draw.rect(windowSurface, (0,0,0), sidebar_rect)
color_picker = ColorPicker(windowSurface, 255, 1, horz_offset = 8)
brush_picker = BrushPicker(windowSurface, 255, horz_offset = 8, vert_offset = int(color_picker.height+40))
brush = [brush_picker.type, brush_picker.eraser, brush_picker.brush_size, color_picker.color]
gap_width = 35
draw_gap()

button_width = int(sidebar_width*.8)
button_rect = Rect((sidebar_width)//2 - button_width//2,color_picker.height +20 - 20,button_width,40)
#the save button
def draw_save(color = (100,100,100), message = "click to copy img to clipboard"):
    X = (sidebar_width)//2
    Y = color_picker.height + 20
    font = pygame.font.Font('freesansbold.ttf', int(15))
    text = font.render(message, True, (255,255,255), color)
    textRect = text.get_rect()
    textRect.center = (X, Y)
    pygame.draw.rect(windowSurface,color,button_rect)
    windowSurface.blit(text, textRect)
    pygame.display.update()
draw_save()

clear_width = int(sidebar_width*.8)
clear_rect = Rect((sidebar_width)//2 - button_width//2,color_picker.height + 40 + brush_picker.actual_height + 10,button_width,40)
def draw_clear(color = (100,100,100), message = "click to clear screen"):
    X = (sidebar_width)//2
    Y = color_picker.height + 40 + brush_picker.actual_height + 20 + 10
    font = pygame.font.Font('freesansbold.ttf', int(15))
    text = font.render(message, True, (255,255,255), color)
    textRect = text.get_rect()
    textRect.center = (X, Y)
    pygame.draw.rect(windowSurface,color,clear_rect)
    windowSurface.blit(text, textRect)
    pygame.display.update()
draw_clear()


def rect_overlap(rect, pos):
    if pos[0] < rect[0]:
        return False
    if pos[1] < rect[1]:
        return False
    if pos[0] > rect[0] + rect[2]:
        return False
    if pos[1] > rect[1] + rect[3]:
        return False
    return True

def millis():
    return time.time()*1000

def sign(n):
    if n >= 0:
        return 1
    else:
        return -1

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == MOUSE_DOWN:
            pressed = True
        if event.type == MOUSE_UP:
            pressed = False
        if event.type == MOUSE_UP or event.type == MOUSE_DOWN or event.type == MOUSE_MOVE:
            if event.type == MOUSE_UP:
                drawing = False
            if pressed:
                brush = [brush_picker.type, brush_picker.eraser, brush_picker.brush_size, color_picker.color]
                if event.pos[0] >= (sidebar_width + gap_width):
                    if drawing: #make line between last point and this point
                        if brush[1] == 0:
                            color = brush[3]
                        else:
                            color = (255,255,255)
                        horz_diff = (event.pos[0] - last_drawn_pos[0])
                        vert_diff = (event.pos[1] - last_drawn_pos[1])
                        if abs(horz_diff) > abs(vert_diff):
                            num_points = abs(horz_diff)
                        else:
                            num_points = abs(vert_diff)
                        ii = [int(last_drawn_pos[0] + i*horz_diff/num_points) for i in range(num_points)]
                        jj = [int(last_drawn_pos[1] +j*vert_diff/num_points) for j in range(num_points)]
                        for i in range(num_points):
                            pygame.draw.circle(windowSurface, color, (ii[i],jj[i]), brush[2])
                        if brush[0] == 0:
                            pygame.draw.circle(windowSurface, color, event.pos, brush[2])
                            draw_gap()
                        else:
                            rect = Rect(int(event.pos[0]-brush[2]),int(event.pos[1]-brush[2]),brush[2]*2,brush[2]*2)
                            pygame.draw.rect(windowSurface, color, rect)
                            draw_gap()
                    else:
                        drawing = True
                        if brush[1] == 0:
                            color = brush[3]
                        else:
                            color = (255,255,255)
                        if brush[0] == 0:
                            pygame.draw.circle(windowSurface, color, event.pos, brush[2])
                            draw_gap()
                        else:
                            rect = Rect(int(event.pos[0]-brush[2]),int(event.pos[1]-brush[2]),brush[2]*2,brush[2]*2)
                            pygame.draw.rect(windowSurface, color, rect)
                            draw_gap()
                    last_drawn_pos = event.pos
                else:
                    if not drawing:
                        brush_picker.handle_event(event)
                        color_picker.handle_event(event)
                        if event.type == MOUSE_DOWN:
                            if rect_overlap(button_rect, event.pos):
                                start = millis()
                                draw_save((50,50,50), "copying...")
                                #save the image
                                pygame.image.save(windowSurface, "temp.jpg")
                                #copy to clipboard
                                filepath = 'temp.jpg'
                                image = Image.open(filepath)
                                imwidth, imheight = image.size
                                image = image.crop((sidebar_width+gap_width, 0, imwidth, imheight))
                                #image.show()
                                output = BytesIO()
                                image.convert("RGB").save(output, "BMP")
                                data = output.getvalue()[14:]
                                output.close()
                                send_to_clipboard(win32clipboard.CF_DIB, data)
                                #remove temp file
                                os.remove("temp.jpg")
                                while (millis() - start) < 700:
                                    x = 1
                                draw_save((75,75,75), "copied! use ctrl-v to paste")
                                start = millis()
                                while (millis() - start) < 1000:
                                    x = 1
                                draw_save()
                            if rect_overlap(clear_rect, event.pos):
                                screen_rect = Rect(sidebar_width,0,width-sidebar_width,height)
                                pygame.draw.rect(windowSurface, (255,255,255), screen_rect, 0)
                                draw_gap()
            pygame.display.update()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
