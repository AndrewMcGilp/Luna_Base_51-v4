#Luna Base 51 -Pi- by Andrew McGilp March-2020
#A Python Pygame 

import pygame, math, sys, random
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480#for smal screen
SCR_RES = 0
SCR_FULL = 0
SND_LEVEL = 3
IMG_NO = 0
MENU_SET = 1#First time run

#Color    R    G    B
WHITE  = (255, 255, 255)
GREEN  = (0  , 255,   0)
RED    = (255, 0  ,   0)
BLUE   = ( 80, 150, 255)
YELLOW = (255, 255,  80)

LEFT = 1
MIDDLE = 2
RIGHT = 3
UP = 4
DOWN = 5
MENU_NO = 0

# All the bool stuff true/false
done = False
showMsg = False
pauseGame = False
endGame = False
editName = False

#Player Position
posX = 0
posY = 0
#Mouse Pos
posx = 0
posy = 0
loopCount = 0
numIndex = 0

char = '_'
strName0 = 'Pi_0...'#Your Name or input your name

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)# plays better in full screen mode
pygame.display.set_caption('Luna Base 51')
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

#----------Load sprites images sound and fonts----------
#Load Font's
myHudFont = pygame.font.SysFont("none", 28)
myMsgFont = pygame.font.SysFont("none", 92)

strMsg = myMsgFont.render('Update ME-0!', True, GREEN)
strMsg1 = myHudFont.render('Update ME-1!', True, WHITE)

settList = []
nameList = []
scoreList = []
charList = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','U','R','S','T','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9','$','@','*','_','&','!']

#Load image's
bgImg = pygame.image.load('Stars_Earth1.png').convert()
startImg = pygame.image.load('GameStart.png').convert_alpha()
underLayImg = pygame.image.load('UnderLay1.png').convert_alpha()
overLayImg = pygame.image.load('OverLay1.png').convert_alpha()
crossHairImg = pygame.image.load('CrossHair.png').convert_alpha()
baseImg = pygame.image.load('MoonBase4.png').convert_alpha()
coverImg = pygame.image.load('MtlPlate2.png').convert_alpha()
laserImg = pygame.image.load('Laser.png').convert_alpha()
asteroidImg = pygame.image.load('Asteroid3.png').convert_alpha()
expoldImg = pygame.image.load('Explod5.png').convert_alpha()
damageImg = pygame.image.load('Damage3.png').convert_alpha()
playerImg = pygame.image.load('player4.png').convert_alpha()
ufoImg = pygame.image.load('UFO4.png').convert_alpha()
missileImg = pygame.image.load('Bomb2.png').convert_alpha()
powerUpImg = pygame.image.load('PowerUp1.png').convert_alpha()
shieldUpImg = pygame.image.load('ShieldUp1.png').convert_alpha()
shieldGridImg = pygame.image.load('ShieldGrid.png').convert_alpha()

#Load Sounds
pygame.mixer.pre_init(44100,16, 2, 4096)
laserSnd = pygame.mixer.Sound('laser.wav')
explodSnd = pygame.mixer.Sound('explos.wav')
    
hiScore = 0
score = 0
asteroidQty = 0
ufoQty = 0
ufosToShoot = 0
bonusPoints = 0
levelNo = 0
health = 0
oldHealth = 0
dropX = 0
rank = 0
rndRangeY = -400
shieldLevel = 0
bombCount = 0
vibePosX  = 0
vibeTime = 0

# The player sprite
player_list = pygame.sprite.Group()
screen_rect = screen.get_rect()
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.myTexture1 = playerImg
        self.position = (posX, posY)
        self.direction = 0

    def update(self):

        self.position = (posX, posY)
        tan = math.atan2((posy - posY), (posx - posX))
        deg = math.degrees(tan)
        tRot = round(deg, 0)
        self.direction = -(tRot + 90)
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
       
#Add the player
player = Player()
player_list.add(player)               

# The laser sprite
laser_list = pygame.sprite.Group()
class Laser(pygame.sprite.Sprite):
 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.myTexture1 = laserImg
        self.position = (posX, posY)# player position
        self.speed = 40
        self.direction = Direction
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        
    def update(self):
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += - self.speed*math.sin(rad)
        y += -self.speed*math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.speed = 5
        
#The asteroid stuff
asteroid_list = pygame.sprite.Group()
class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self, speedY, aType):
        super().__init__()
        self.myTexture1 = asteroidImg
        self.image = self.myTexture1
        self.rect = pygame.Rect(20, 20, 40, 40)
        self.type = aType
        self.speedY = speedY
        
    def update(self):
        self.rect.y += self.speedY     

#Create Ufo's aka Mothership or UFO's
ufo_list = pygame.sprite.Group()
class Ufo(pygame.sprite.Sprite):
    
    def __init__(self, speed):
        super().__init__()
        self.myTexture1 = ufoImg
        self.image = self.myTexture1
        self.rect = pygame.Rect(self.myTexture1.get_rect())
        self.health = 100
        self.speed = speed
        
    def update(self):

        self.rect.x += self.speed
           
#Explosion  effect     
explod_list = pygame.sprite.Group()       
class Explod(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, size, num):
        super().__init__()
        
        if (num == 0):
            self.myTexture1 = expoldImg
        elif (num == 1):
            self.myTexture1 = shieldUpImg
        else:
            self.myTexture1 = powerUpImg
        
        self.image = self.myTexture1
        self.rect = pygame.Rect(self.myTexture1.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        self.timer = 0
        self.size = size
        self.scaler = 30 * size
       
    def update(self):
        self.rect.y -= self.size * 0.5
        self.rect.x -= self.size * 0.5
        self.scaler += self.size
        self.image = pygame.transform.scale(self.myTexture1, (self.scaler , self.scaler)) 
        self.timer += 1
        
#Shield
shield_list = pygame.sprite.Group()
class Shield(pygame.sprite.Sprite):

    def __init__(self, posx, posy, health):
        super().__init__()
        self.myTexture1 = shieldGridImg
        self.image = self.myTexture1
        self.rect = pygame.Rect(self.myTexture1.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        
    def update(self):
        self.health -= 50
        
#Create Damage        
damage_list = pygame.sprite.Group()
class Damage(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy):
        super().__init__()
        self.myTexture1 = damageImg
        self.image = self.myTexture1
        self.rect = pygame.Rect(self.myTexture1.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        
    def update(self):
        self.rect.x = self.rect.x + vibePosX
        
def CreateLaser():#Fire the laser
    
    laser = Laser()
    laser_list.add(laser)
    laser.rect.x = posX
    laser.rect.y = posY
    if SND_LEVEL > 0:
        laserSnd.play()
        
def CreateMissile():#Drop the Missile using the asteroid class
    
    asteroid = Asteroid(3.0, 0)
    asteroid.image = missileImg
    asteroid.rect.x = dropX
    asteroid.rect.y = 35
    asteroid_list.add(asteroid)
    
def CreateShieldIcn():#Shield icon
    
    asteroid = Asteroid(2.0, 2)
    asteroid.image = shieldUpImg
    asteroid.rect.x = random.randrange(60, 740)
    asteroid.rect.y = -100
    asteroid_list.add(asteroid)

def CreatePowerUpIcn():#Power Up icon
    
    asteroid = Asteroid(2.0, 3)
    asteroid.image = powerUpImg
    asteroid.rect.x = random.randrange(60, 740)
    asteroid.rect.y = -100
    asteroid_list.add(asteroid)
    
def CreateAsteroids():
    
    global asteroidQty
    
    qty = levelNo * 10 + 20
    
    for i in range(qty):
        asteroidQty += 1
        asteroid = Asteroid(1.0, 1)
        asteroid.image = asteroidImg
        asteroid.rect.x = random.randrange(20, 740)
        asteroid.rect.y = random.randrange(rndRangeY, -200)
        asteroid_list.add(asteroid)
              
#Create UFO  
def CreateUfo(spd, x, y):
    
    global ufoQty
    ufoQty += 1
    
    ufo = Ufo(spd)
    ufo.rect.x = x
    ufo.rect.y = y
    ufo_list.add(ufo)    

def CreateUfos(type):
    
    global ufosToShoot
    ufosToShoot = 0      

    if (type == 0):
        CreateUfo(2, -350, 30)
    elif (type == 1):
        CreateUfo(-2, 1150, 30)
    elif (type == 2):
        CreateUfo(2, -350, 30)
        CreateUfo(-2, 1150, 30)
    elif (type == 5):
        ufosToShoot = 4  
        CreateUfo(5, -500, 50)
        CreateUfo(-5, 1300, 50)
        CreateUfo(5, -350, 150)
        CreateUfo(-5, 1150, 150) 
    elif (type == 10):
        ufosToShoot = 6
        CreateUfo(5, -500, 50)
        CreateUfo(-5, 1175, 100)
        CreateUfo(5, -350, 150)
        CreateUfo(-5, 1025, 200) 
        CreateUfo(5, -500, 250)
        CreateUfo(-5, 1175, 300)
    else:
        ufosToShoot = 6
        CreateUfo(5, -350, 50)
        CreateUfo(5, -500, 100)
        CreateUfo(5, -350, 150)
        CreateUfo(5, -500, 200) 
        CreateUfo(5, -350, 250)
        CreateUfo(5, -500, 300)

#Create Shields
def CreateShields():
    
    global shieldLevel
    
    posYadder = shieldLevel * 30
    shield = [
    Shield(25, SCREEN_HEIGHT - 100 - posYadder, 100),
    Shield(175, SCREEN_HEIGHT - 130 - posYadder, 100),
    Shield(325, SCREEN_HEIGHT - 160 - posYadder, 100),
    Shield(475, SCREEN_HEIGHT - 130 - posYadder, 100),
    Shield(625, SCREEN_HEIGHT - 100 - posYadder, 100)
    ]
    shield_list.add(*shield)
 
    if (shieldLevel < 2):
        shieldLevel += 1
    else:
        shieldLevel = 0
        
#Create damage
def CreateDamage(posx, posy, vTime):
    
    global vibeTime
    
    damage = Damage(posx, posy)
    damage_list.add(damage)
    vibeTime = vTime
    
#Create explotion effect   
def CreateExplod(posx, posy, size, num):
    
    explod = Explod(posx, posy, size, num)  
    explod_list.add(explod)
    if (SND_LEVEL > 0):
        explodSnd.play()
        

#Write all the game settings        
def WriteFile(settList, nameList, scoreList, infoList):
    
    content = (settList + '-' + nameList + '-' + scoreList + '-' + infoList)   
    
    try:
        f = open('settings.txt', "w")
        f.write(content)#\n
        f.close()
         
    except IOError:
        print('Could not create a file!')

#Read and load all the game settings        
def ReadFile():

    try:    
        f = open('settings.txt', "r")
        if f.mode == 'r':
            objFile = f.read()                  
            f.close()
            ParseData(objFile)
    except:#If no file create it
        print('Could not Find File!')
        SetDefaults()

def ParseData(strMain):#Pares data

    global IMG_NO
    global SND_LEVEL   
    global settList
    global nameList
    global scoreList
    global strName0
    
    SND_LEVEL = 0
    
    try:

        listMain = strMain.split('-')
        
        settList.clear()
        for i in range(0, 5, 1):
            settList.append(int(listMain[i]))
        #Set the screen sound
        SetScreen(settList[0], settList[1])
        SetSound(settList[2])
        IMG_NO = settList[3]
        SetMenu(settList[4])
        
        nameList.clear()
        for i in range(5, 10, 1):
            nameList.append(listMain[i])        

        scoreList.clear()
        for i in range(10, 15, 1):
            scoreList.append(int(listMain[i]))
            
        strName0 = listMain[15]
          
        listMain.clear()
        
    except:
        print('Could not Pars Data!')
        SetDefaults()

    UpdateRank(0)

def SetDefaults():
    
    print('Default game settings!')#Load default settings
    WriteFile('0-0-3-0-0', 'Pi_5...-Pi_4...-Pi_3...-Pi_2...-pi_1...', '100-200-300-400-500', strName0)
    ParseData('0-0-3-0-4-Pi_5...-Pi_4...-Pi_3...-Pi_2...-pi_1...-100-200-300-400-500-' + strName0)
    
def SetScreen(resValue, fullScr):

    global SCR_RES
    global SCR_FULL
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global posX
    global posY

    SCR_RES = resValue
    SCR_FULL = fullScr

    if (SCR_RES == 1):
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
    else:
        SCREEN_WIDTH = 800  
        SCREEN_HEIGHT = 480
        
    if (fullScr == 1):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN, 16)  
    else:      
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)

    #Set the position of the player
    posX = SCREEN_WIDTH / 2 
    posY = SCREEN_HEIGHT - 20
    SetMenu(0)
    

def SetSound(value):
    
    global SND_LEVEL
    global nameList
    
    SND_LEVEL += value
    
    if (SND_LEVEL < 0):
        SND_LEVEL = 0
    elif (SND_LEVEL > 9):
        SND_LEVEL = 9
        
    explodSnd.set_volume(SND_LEVEL * 0.04)# Set sound effect volume
    laserSnd.set_volume(SND_LEVEL * 0.05)# Set sound effect volume
    SetMenu(0)

def SetMenu(value):

    global MENU_NO
    global strMsg1
    
    MENU_NO += value   
    
    if (MENU_NO < 0):
        MENU_NO = 6
    elif (MENU_NO > 6):
        MENU_NO = 0    
    
    if MENU_NO == 0:   
        strMsg1 = myHudFont.render('START GAME :', True, WHITE)#
    if MENU_NO == 1:
        if SCR_FULL == 1:
            strMsg1 = myHudFont.render('FULL SCREEN : OFF', True, GREEN)#
        else:
            strMsg1 = myHudFont.render('FULL SCREEN : ON', True, YELLOW)#
    if MENU_NO == 2:
        strMsg1 = myHudFont.render('SOUND FX LEVEL : %s' %SND_LEVEL, True, GREEN)#
    if MENU_NO == 3:
        if SCR_RES  == 1:
            strMsg1 = myHudFont.render('RESOLUTION : 800X480 ', True, GREEN)#
        else:
            strMsg1 = myHudFont.render('RESOLUTION : 800X600 ', True, YELLOW)#         
    if MENU_NO == 4:   
        strMsg1 = myHudFont.render('HELP SCREEN :', True, GREEN)#
        SetText(0)
    if MENU_NO == 5:
        strMsg1 = myHudFont.render('HALL OF FAME :', True, BLUE)#
        SetText(1)
            
    if MENU_NO == 6:     
        strMsg1 = myHudFont.render('QUIT:', True, RED)#

def EditName(num0, num1):
    
    global nameList
    global strName0
    global strMsg1
    global numIndex
    global editName
    
    char = charList[numIndex]
    listLen = len(charList) - 1
 
    if (num1 == 0):#Scroll up and down through the alphabet and numbers

        if (len(strName0) < 10):
            
            numIndex += num0
            
            if (numIndex < 0):
                numIndex = listLen
            elif (numIndex > listLen):
                numIndex = 0
            
            char = charList[numIndex]
        else:
            char = charList[0]

    elif (num1 == 1):#Add Selected char

        if (len(strName0) < 10):
            strName0 += char
        
        numIndex = 0
        char = charList[numIndex]
        
    elif (num1 == 2):
        
        if (len(strName0)>0):
            strName0 = strName0[:-1]
            
        numIndex = 0
        char = charList[numIndex]
        
    elif (num1 == 3):#Save and Exit
        
        try:
            num2 = nameList.index('***~~***')
            nameList.pop(num2)
            nameList.insert(num2, strName0)
            
        except:#print('COULD NOT EDIT NAME!')
            strMsg1 = myHudFont.render('COULD NOT EDIT NAME!', True, RED)
           
        numIndex = 0
        UpdateRank(0)
        SetText(1)
        editName = False

    else:
        print('Out Of Range!')
        
    if (editName):  
        strMsg1 = myHudFont.render('EDIT NAME: ' + strName0 + '_[' + char + ']', True, RED)
    else:
        strMsg1 = myHudFont.render('HALL OF FAME :', True, BLUE)
        
def UpdateRank(score0):

    global strName1
    global strName2
    global strName3
    global strName4 
    global strName5
    
    global score1 
    global score2 
    global score3 
    global score4 
    global score5
    global hiScore
    
    global nameList
    global scoreList
    global editName

    try:#Update Rankings

        scoreList.append(score0)
        scoreList.sort()
        num = scoreList.index(score0)

        if (num != 0):
            nameList.insert(num, '***~~***')
            nameList.remove(nameList[0])

        scoreList.remove(scoreList[0])
            
        strName1 = nameList[0]
        strName2 = nameList[1]
        strName3 = nameList[2]
        strName4 = nameList[3]
        strName5 = nameList[4]

        score1 = scoreList[0]
        score2 = scoreList[1]
        score3 = scoreList[2]
        score4 = scoreList[3]
        score5 = scoreList[4]
               
        hiScore = score5
        
    except:
        print('Could not Update Rank!')
      
    if (num != 0):
        SetMenu(5)       
        editName = True
        EditName(0, 0)
        SetText(2)
        
    
def SetText(num):

    global strLine0
    global strLine1
    global strLine2
    global strLine3
    global strLine4   
    global strLine5
    global strLine6

    try:
        if (num == 0):
    
            strLine0 = '_________***HELP-SCREEN***_________ '
            strLine1 = 'MOUSE - MOVE TO AIM'
            strLine2 = 'LEFT CLICK - ENTER OR FIRE'
            strLine3 = 'RIGHT CLICK - RETURN OR PAUSE'
            strLine4 = 'MIDDLE CLICK - DEL OR SCREEN SHOT'
            strLine5 = 'WHEEL - SCROLL UP OR DOWN MENU'
            strLine6 = '_________________________HAVE FUN!'
        else:
        
            strLine0 = '_________***HALL-OF-FAME***_________ '
            strLine1 = 'RANK_1 : ' + strName5 + ' :    ' + str(score5)
            strLine2 = 'RANK_2 : ' + strName4 + ' :    ' + str(score4)
            strLine3 = 'RANK_3 : ' + strName3 + ' :    ' + str(score3)
            strLine4 = 'RANK_4 : ' + strName2 + ' :    ' + str(score2)
            strLine5 = 'RANK_5 : ' + strName1 + ' :    ' + str(score1)
        
            if (num == 1):
                strLine6 = '_______________________________END.'
            else:  
                strLine6 = 'LMB=SAVE_:_CMB=DEL_:_RMB=SELECT'

    except:
        print('Could not set text!')
        #SetDefaults()
        
    strLine0 = myHudFont.render(strLine0, True, BLUE)#
    strLine1 = myHudFont.render(strLine1, True, WHITE)
    strLine2 = myHudFont.render(strLine2, True, WHITE)
    strLine3 = myHudFont.render(strLine3, True, WHITE)
    strLine4 = myHudFont.render(strLine4, True, WHITE)
    strLine5 = myHudFont.render(strLine5, True, WHITE)
    strLine6 = myHudFont.render(strLine6, True, RED)
     
        
def ResetGame():# Reset all game values

    global asteroidQty
    global ufoQty
    global health 
    global oldHealth 
    global bombCount
    global shieldLevel
    global score
    global rank
    global rndRangeY
    global pauseGame
    global levelNo
    global endGame
    global vibeTime
    
    UpdateRank(score)
    score = 0
    pauseGame = False
    endGame = False
    asteroidQty = 0
    ufoQty = 0
    health = 0
    oldHealth = 0
    bombCount = 0
    shieldLevel = 0   
    rank = 0
    rndRangeY = -400
    RemoveSprites()
    levelNo = 0
    vibeTime = 0
       
def RemoveSprites():

    for damage in damage_list:
        damage_list.remove(damage)
    for laser in laser_list:
        laser_list.remove(laser)
    for asteroid in asteroid_list:
        asteroid_list.remove(asteroid)
    for ufo in ufo_list:
        ufo_list.remove(ufo)
    for shield in shield_list:
        shield_list.remove(shield)
    for explod in explod_list:
        explod_list.remove(explod)
        
def NewLevel():

    global levelNo 
    global asteroidQty
    global rndRangeY 
    global loopCount
    global strMsg
    global health
    global oldHealth
    global rank
    global bonusPoints
    global score
    global bonusPoints

    levelNo += 1
    rndRangeY -= 50
    loopCount = -50
    
    if (levelNo % 5 == 0):
        bonusPoints = 50
        CreateUfos(levelNo)
        strMsg = myMsgFont.render('BONUS UFOs!', True, RED)
        
    else:
        CreateAsteroids()
    
        if (bonusPoints == 0):
            if (health == oldHealth):
                rank += 1
                strMsg = myMsgFont.render('  PERFECT!', True, BLUE)           
            else:
                strMsg = myMsgFont.render('GET READY!', True, YELLOW)
        else:
            if (ufosToShoot == 0):
                bonusPoints = bonusPoints * 2
                strMsg = myMsgFont.render('****  ' + str(bonusPoints) + '  ****', True, RED)
            else:
                strMsg = myMsgFont.render('****  ' + str(bonusPoints) + '  ****', True, YELLOW)

        if (levelNo % 2 == 0):
            rndUfo = random.randrange(0,2)
            CreateUfos(rndUfo)
            
    score += bonusPoints
    oldHealth = health
    bonusPoints = 0
        
def GameOver():
    
    global strMsg
    global endGame
    global loopCount

    endGame = True
    loopCount = -200
    strMsg = myMsgFont.render('GAME OVER!', True, RED)

    for i in range(30):
        x = random.randrange(0, 750)
        y = random.randrange(15, 60)
        CreateDamage(x, SCREEN_HEIGHT - y, 150)
        
    explod = [
    Explod(0, SCREEN_HEIGHT - 85, 4, 0),
    Explod(125, SCREEN_HEIGHT - 100, 5, 0),
    Explod(250, SCREEN_HEIGHT - 115, 6, 0),
    Explod(375, SCREEN_HEIGHT - 115, 6, 0),
    Explod(500, SCREEN_HEIGHT - 100, 5, 0),
    Explod(625, SCREEN_HEIGHT - 85, 4, 0)
    ]
    explod_list.add(*explod)
    

    
    if SND_LEVEL  > 0:
        channel = explodSnd.play()

def ScreenShot():
    
    global IMG_NO
    
    #fileName = ('/home/pi/Desktop/scrShot-' + str(IMG_NO) + '-.png')
    fileName = ('scrShot-' + str(IMG_NO) + '-.png')
    pygame.image.save(screen, fileName)
    strMsg1 = myHudFont.render('SCREENSHOT TAKEN! :', True, YELLOW)
    IMG_NO += 1

def SaveGame():
    
    global nameList
    try:
        settList = (str(SCR_RES) + '-' + str(SCR_FULL) + '-' + str(SND_LEVEL) + '-' + str(IMG_NO) + '-' + str(0))
        nameList = '-'.join(nameList)
        scoreList = (str(score1) + '-' + str(score2) + '-' + str(score3) + '-' + str(score4) + '-' + str(score5))
        WriteFile(settList, nameList, scoreList, strName0)
    except:
        print('Could not save game settings')
                
def BtnLeft():#Update Inter and or Fire btn

    global MENU_NO
    global levelNo
    global strMsg
    global pauseGame
    global health
    global SCR_FULL
    global SCR_RES
    global SND_LEVEL
    global done
    
    if (MENU_NO == 0 and endGame == False):
        if health > 0:
            if (loopCount == 0):
                CreateLaser()
            pauseGame = False
        else:
            if (levelNo > 0):
                ResetGame()
            else:
                health = 100
                                
    elif (MENU_NO == 1):
        if (SCR_FULL == 1):
            SCR_FULL = 0
        else:
            SCR_FULL = 1
        SetScreen(SCR_RES, SCR_FULL)
    elif (MENU_NO == 2):
        SetSound(-1)

    elif (MENU_NO == 3):
        if (SCR_RES == 1):
            SCR_RES = 0
        else:
            SCR_RES = 1
            
        SetScreen(SCR_RES, SCR_FULL)
        
    elif (MENU_NO == 4):
        SetMenu(-4)
        
    elif (MENU_NO == 5):
        
        if (editName):
            EditName(0, 3)
        else:
            SetMenu(-5)        
            
    elif (MENU_NO == 6):
        done = True
        
def BtnCenter():

    if (editName):
        EditName(0, 2)
    else:
        ScreenShot()

def BtnRight():#Update return or back

    global levelNo
    global pauseGame
    global strMsg
    global health
    global done


    if (levelNo > 0):
        if (pauseGame == False and health > 0):
            pauseGame = True
            strMsg = myMsgFont.render('   PAUSED!', True, GREEN)
        else:
            ResetGame()            
    else:
        
        if (MENU_NO == 2):
            SetSound(1)
            
        elif (MENU_NO == 4):
            SetMenu(-4)
        
        elif (MENU_NO == 5):
            
            if (editName):
                EditName(0, 1)
            else:
                SetMenu(-5)
        
        elif (MENU_NO == 6):
            done = True

def BtnUp():#Up btn

    if (editName):
        EditName(1, 0)
    else:
        if (levelNo == 0):
            SetMenu(1)
               
def BtnDown():#Down btn

    if (editName):
        EditName(-1, 0)
    else:
        if (levelNo == 0):
            SetMenu(-1)       

def UpdateMouse():

    global posx
    global posy
    global done
    
    #Handel input **Mouse** or **RAT**
    for event in pygame.event.get():
        
        pos = pygame.mouse.get_pos()
        posx = pos[0]
        posy = pos[1]#
        
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:#Left click
                BtnLeft()
                    
            elif event.button == MIDDLE:# Middle click 
                BtnCenter()

            elif event.button == RIGHT:#Right click
                BtnRight()

            elif event.button == UP:# Wheel Up 
                BtnUp()
                
            elif event.button == DOWN:# Wheel Down
                BtnDown()

           
#Read and load the game settings        
ReadFile()

while not done:
#____________________The Main game loop___________________

    UpdateMouse()
        
#Game Logik
    #check for collitions
    for laser in laser_list:
            
        laser_hit_list = pygame.sprite.spritecollide(laser, asteroid_list, False)  
            
        for asteroid in laser_hit_list:
            asteroid_list.remove(asteroid)
            laser_list.remove(laser)
            if (asteroid.type == 0):
                score += 50 * rank
                CreateExplod(asteroid.rect.x - 40, asteroid.rect.y - 40, 4, 0)
            elif (asteroid.type == 1):
                score += 10
                asteroidQty -= 1
                CreateExplod(asteroid.rect.x - 5, asteroid.rect.y - 1, 2, 0)
            elif (asteroid.type == 2):
                CreateExplod(asteroid.rect.x - 5, asteroid.rect.y - 1, 2, 1)                
                CreateShields()
                
  
            elif (asteroid.type == 3):
                score += 50
                CreateExplod(asteroid.rect.x - 5, asteroid.rect.y - 1, 2, 2)
                health += 50

                if (health == oldHealth):
                    oldHealth = health

        ufo_hit_list = pygame.sprite.spritecollide(laser, ufo_list, False)   
        for ufo in ufo_hit_list:
            CreateExplod(laser.rect.x + 3, laser.rect.y - 20,1, 0)
            laser_list.remove(laser)
            score += 20

            if (ufo.rect.x > 80 and ufo.rect.x < 600 and ufo.speed > -5 and ufo.speed < 5):
            
                ufo.speed = ufo.speed * 2
                bombCount += 1
                
                if (ufo.speed > 0):
                    dropX = ufo.rect.x + 40
                else:
                    dropX = ufo.rect.x + 30               

                if bombCount == 3:
                    CreatePowerUpIcn()
                elif bombCount == 6:
                    CreateShieldIcn()
                    bombCount = 0
                
                CreateMissile()

            else: #add bonus UFOs and points
                       
                if (ufo.speed == 5 or ufo.speed == -5):
                    ufosToShoot -= 1
                    bonusPoints += 50
                    ufo.speed = ufo.speed * 4

            
        if (laser.rect.y < -10 or laser.rect.y > SCREEN_HEIGHT + 10):
            laser_list.remove(laser)
            
        if (laser.rect.x < -10 or laser.rect.x > SCREEN_WIDTH + 10):
            laser_list.remove(laser)
     
    for shield in shield_list:
        
        shield_hit_list = pygame.sprite.spritecollide(shield, asteroid_list, False) 
        
        for asteroid in shield_hit_list:
            asteroid_list.remove(asteroid)
            shield_list.remove(shield)
            if asteroid.type == 1:
                asteroidQty -= 1
            score += 5    
            CreateExplod(asteroid.rect.x - 5, asteroid.rect.y - 1, 2, 0)    
            
    for asteroid in asteroid_list:
    
        if (asteroid.rect.y > SCREEN_HEIGHT -50):

            if (asteroid.type == 0):#Bomb
                CreateDamage(asteroid.rect.x + 20, asteroid.rect.y - 5, 50)
                CreateDamage(asteroid.rect.x - 25, asteroid.rect.y - 5, 50)
                CreateExplod(asteroid.rect.x - 100, asteroid.rect.y - 80, 8, 0)
                
            elif (asteroid.type == 1):#Asteroid
                asteroidQty -= 1
                CreateDamage(asteroid.rect.x - 5, asteroid.rect.y - 5, 10)
                CreateExplod(asteroid.rect.x - 5, asteroid.rect.y - 1, 2, 0)

            asteroid_list.remove(asteroid)

            if (health > 0):
                if (asteroid.type == 0):
                    health -= 50
                else:
                    health -= 10
        
    for player in player_list:
        Direction = player.direction
 
    for explod in explod_list:
        if (explod.timer > 26):
            explod_list.remove(explod)
            
    for ufo in ufo_list:
        if (ufo.rect.x > SCREEN_WIDTH + 600 or ufo.rect.x < -600):
            ufoQty -= 1
            ufo_list.remove(ufo)
            

    if (health > 0):
        
        if (asteroidQty == 0  and ufoQty == 0):
            NewLevel()
            
        if (hiScore < score):
            hiScore = score

        if (loopCount < 0):
            loopCount += 1
            showMsg = True
        else:
            showMsg = False

    else:        
        
          if (levelNo != 0):
            
            if (endGame == False):
                GameOver()
                loopCount = -200

            if (loopCount < 0):
                loopCount += 1
                showMsg = True
            else:
                showMsg = False
                levelNo = 0
                ResetGame()      
             
 
    #Update all the sprites if not paused
    if (pauseGame == False):
        asteroid_list.update()
        laser_list.update()    
        player_list.update()
        explod_list.update()
        ufo_list.update()
        damage_list.update()
        
        if (vibeTime > 0):
            if (vibeTime % 2 == 0):
                vibePosX = 1
            else:
                vibePosX = -1
            vibeTime -= 1
        else:
            vibePosX = 0

#___________________RENDERING________________
    
    #screen.fill((0, 0, 0))
    screen.blit(bgImg, (0, 0))
    screen.blit(baseImg, (vibePosX, SCREEN_HEIGHT - 239))
    laser_list.draw(screen)
    player_list.draw(screen)
    shield_list.draw(screen)
    screen.blit(coverImg, (338 + vibePosX, SCREEN_HEIGHT - 28))
    damage_list.draw(screen)
    asteroid_list.draw(screen)
    ufo_list.draw(screen)
    explod_list.draw(screen)
       
    if (levelNo > 0):        
        # String text for hud
        hudHealth = myHudFont.render('POWER : %s' % health, True, WHITE)#health
        hudLevel = myHudFont.render('LEVEL : %s' % levelNo, True, WHITE)#Level
        hudHiScore = myHudFont.render('HI-SCORE : %s' % hiScore, True, WHITE)#hi score
        hudScore = myHudFont.render('SCORE : %s' % score, True, WHITE)#score
        hudRank = myHudFont.render('RANK : %s' % rank, True, WHITE)#rank ranking vibePosX vibeTime endGame loopCount asteroidQty bonusPoints
        #Draw the HUD
        screen.blit(hudScore, (20, 10))
        screen.blit(hudHiScore, (220, 10))
        screen.blit(hudHealth, (440, 10))
        screen.blit(hudLevel, (580, 10))
        screen.blit(hudRank, (690, 10))
        if (showMsg or pauseGame):
            screen.blit(strMsg, (200, 200))            
    else:
        screen.blit(underLayImg, (185, 30))
        
        if (MENU_NO == 4 or MENU_NO == 5):#Hall of Fame and Help Screen
            
            screen.blit(overLayImg, (185, 30))
            
            screen.blit(strLine0, (205, 55))
            screen.blit(strLine1, (205, 85))
            screen.blit(strLine2, (205, 115))
            screen.blit(strLine3, (205, 145))
            screen.blit(strLine4, (205, 175))
            screen.blit(strLine5, (205, 205))
            screen.blit(strLine6, (205, 235))
            
        screen.blit(strMsg1, (290, 390))
        screen.blit(startImg, (100, 10))
    
    screen.blit(crossHairImg, (posx - 15, posy - 15))
    
    pygame.display.flip()
    clock.tick(30)
    
#__________________EXIT_THE_GAME____________
#Save the game settings

SaveGame()
pygame.quit()
sys.exit()

#Make asteroid rotate at random speeds and make them randomly differant size
#Make Shield go thiner if hit
#Make the tower collapse
#Cue the sound
#Fix Buggs
