import pygame as pg
import numpy as np
from datetime import datetime as dt
import pygame_text as ptext

#-- Calculate pixel position of cell x,y
def coordcalc(x,y):
    coordx = x*cellsize+int(cellsize/3)
    coordy = y*cellsize+int(cellsize/5)
    return coordx,coordy

#-- Standard print routine for text with fixed font and font size
def displaytext(text,x,y,clr):
    ptext.draw(text, (x,y), sysfontname='Monospaced', fontsize=cellsize, color=clr)

#-- Display all content of the status bar, except for the message. First remove existing text
def statusbar():
    pg.draw.rect(win, black, (0,statusy,19*cellsize,cellsize))
    displaytext('Score:', int(cellsize/2),statusy, white)
    displaytext('Cells done:', 6*cellsize,statusy, white)
    displaytext('Cells left:', 13*cellsize,statusy, white)
    displaytext(str(score), 3*cellsize,statusy, white)
    displaytext(str(nrdone), 10*cellsize,statusy, white)
    displaytext(str(rows*cols-nrdone), 17*cellsize,statusy, white)
    
#-- Displays message in bottom of screen
def message(text):
    clear_message()
    x = 19*cellsize
    displaytext(text, x,statusy, yellow)

#-- Clears message area by filling it with background color
def clear_message():
    x = 19*cellsize
    dx = 15*cellsize
    dy = cellsize
    pg.draw.rect(win, black, (x,statusy,15*cellsize,cellsize)) 

#-- Clears the character at position x,y
def clearnum(x,y):
    coordx,coordy=coordcalc(x,y)
    width = cellsize-8
    height = cellsize-6
    pg.draw.rect(win, black, (coordx,coordy,width,height))    

#-- Determines window dimensions based on screen resolution and create it
def init():
    global cellsize,win,winw,winh
    disw = infoObject.current_w
    dish = infoObject.current_h
    cellsize = int(dish/1.2/rows)
    print('Screenw : '+str(disw))
    print('Screenh : '+str(dish))
    print('Cellsize: '+str(cellsize))
    winw = cellsize*cols+1
    winh = cellsize*rows+1
    print('Winw    : '+str(winw))
    print('Winh    : '+str(winh))
    win = pg.display.set_mode((winw, winh+cellsize))

#-- Draws grid and fills cells with previously generated random numbers
def create_field():
    for i in range(rows+1):
        x = 0
        y = i*cellsize
        pg.draw.lines(win, orange, False, [(x, y), (winw, y)], 1)
    for i in range(cols+1):
        x = i*cellsize
        y = 0
        pg.draw.lines(win, orange, False, [(x, y), (x, winh)], 1)
    for x in range(cols):
        for y in range(rows):
            coordx,coordy=coordcalc(x,y)
            displaytext(str(field[x,y]), coordx,coordy,green)

#-- Check whether the intended move is valid and return boolean bad
def checkmove(dx,dy):
    bad = False
    if col+dx<0 or col+dx>cols-1 or row+dy<0 or row+dy>rows-1:
        bad = True; return bad 
    dist = field[col+dx,row+dy]
    distx = dist*dx
    disty = dist*dy
    if col+distx<0 or col+distx>cols-1 or row+disty<0 or row+disty>rows-1:
        bad = True; return bad
    for i in range(1,dist+1):
        if fieldstatus[col+dx*i,row+dy*i] == 0:
            bad = True; return bad
    return bad

#-- Run through all possible moves (incl. no move) and return bad if all invalid
def checkdeath():
    bad = False
    tb = 0
    print('Bad:')
    for a in range (-1,2):
        for b in range (-1,2):
            bad = checkmove(a,b)
            if bad == True: tb = tb + 1 
    if tb == 9: message("It's over ! Q to quit"); bad = True; return bad
    return bad

#-- Handle move in 8 directions,by dx (-1,0,1) and dy (-1,0,1)
def move():
    global col,row,score,nrdone
    clear_message()
    if col+dx<0 or col+dx>cols-1 or row+dy<0 or row+dy>rows-1:
        message('Move not possible'); return
    dist = field[col+dx,row+dy]
    distx = dist*dx
    disty = dist*dy
    if col+distx<0 or col+distx>cols-1 or row+disty<0 or row+disty>rows-1:
        message('Move not possible'); bad=True; return
    for i in range(1,dist+1):
        if fieldstatus[col+dx*i,row+dy*i] == 0:
            message('Move not possible'); bad=True; return
    clearnum(col,row)
    for i in range(1,dist+1):
        clearnum(col+dx*i,row+dy*i)
        fieldstatus[col+dx*i,row+dy*i] = 0
        nrdone = nrdone+1
    score = score+field[col+dx,row+dy]
    col = col+distx
    row = row+disty
    coordx,coordy=coordcalc(col,row)
    displaytext('@',coordx,coordy,yellow)

#--------------------------------------------------------------------------------------------------------
#  Start of main procedure
#--------------------------------------------------------------------------------------------------------
white    = (255, 255, 255)
yellow   = (255, 255, 0)
green    = (55, 125, 45)
orange   = (255, 100, 0)
black    = (0,0,0)
grey     = (40,40,40)
score    = 0
nrdone   = 1
cols     = 40   # number of columns in grid, minimum = 25
rows     = 30   # number of rows in grid, minimum = 25
if cols < 25 or rows < 25: 
    print('\nGrid too small! Minimum 25x25')
    quit() 

# Some pygame initialization stuff
pg.init()
infoObject = pg.display.Info()
init()
pg.display.set_caption("Greedynum")
Font = pg.font.SysFont('Monospaced', cellsize)

# Populate arrays
field = np.random.randint(1,9,size=[cols,rows])     # array with a random number in each cell
fieldstatus = np.ones((cols,rows))                  # array that keeps track of empty or full cells

# Create screen grid, populate with random numbers and create status bar
create_field()
statusy = rows*cellsize + int(cellsize/5)
statusbar()

# Determine start position and set pointer
col = np.random.randint(0, cols - 1)
row = np.random.randint(0, rows - 1)
clearnum(col, row)
coordx,coordy = coordcalc(col,row)
displaytext('@',coordx,coordy,yellow)
fieldstatus[col,row] = 0

#--------------------------------------------------------------------------------------------------------
#  Main event loop
#--------------------------------------------------------------------------------------------------------
pg.event.clear()
while 0 == 0:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                quit()
            if event.key == pg.K_KP8:
                dx=0;dy=-1;move()
            if event.key == pg.K_KP9:
                dx=1;dy=-1;move()
            if event.key == pg.K_KP6:
                dx=1;dy=0;move()
            if event.key == pg.K_KP3:
                dx=1;dy=1;move()
            if event.key == pg.K_KP2:
                dx=0;dy=1;move()
            if event.key == pg.K_KP1:
                dx=-1;dy=1;move()
            if event.key == pg.K_KP4:
                dx=-1;dy=0;move()
            if event.key == pg.K_KP7:
                dx=-1;dy=-1;move()
            checkdeath()
            statusbar()
    pg.display.update()