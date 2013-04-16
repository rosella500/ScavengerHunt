#!/opt/local/bin/python2.7

import os, pygame, json
from pygame.locals import *
from utils import *
from modes import ModeManager, GameMode, SimpleMode

kDataDir = 'data'
kGlobals = 'globals.json'
globals = ''

##Keep track of last gameMode (room)
global lastMode

class Cutscene(GameMode):
    def __init__( self, image, sound, duration_in_milliseconds, next_mode_name ):
        '''
        Given a duration to show the splash screen 'duration_in_milliseconds',
        and the name of the next mode,
        displays 'image' until either a mouse click or 'duration_in_milliseconds'
        milliseconds have elapsed.
        '''
        ## Initialize the superclass.
        GameMode.__init__( self )
        
        self.image = image
        self.sound = sound
        self.duration = duration_in_milliseconds
        self.next_mode_name = next_mode_name
    
    def enter( self ):
        '''
        Reset the elapsed time and hide the mouse.
        '''
        self.so_far = 0
        pygame.mouse.set_visible( 0 )
        self.sound.play()
    
    def exit( self ):
        '''
        Show the mouse.
        '''
        pygame.mouse.set_visible( 1 )
        if (type(self.sound).__name__ != 'instance'):
            self.sound.stop()
    
    def draw( self, screen ):
        '''
        Draw the splash screen.
        '''
        screen.blit( self.image, ( 0,0 ) )
        pygame.display.flip()
    
    def update( self, clock ):
        '''
        Update the elapsed time.
        '''
        
        self.so_far += clock.get_time()
        
        ## Have we shown the image long enough?
        if self.so_far > self.duration:
            self.switch_to_mode( self.next_mode_name )
            
    def mouse_button_down(self,event):
        if (type(self.sound).__name__ != 'instance'):
            self.sound.stop()
        self.switch_to_mode(self.next_mode_name)
        
    def key_down(self,event):
        if event.key == K_ESCAPE:
            if (type(self.sound).__name__ != 'instance'):
                self.sound.stop()
            self.switch_to_mode(self.next_mode_name)

class MainMenu( GameMode ):
    def __init__( self ):
        ## Initialize the superclass.
        GameMode.__init__( self )
        
        self.image, _ = load_image( 'MainMenu.jpg' )
        ##load and play music
        try:
            backgroundMusic = os.path.join(kDataDir,'Eternal Memory.ogg')
            pygame.mixer.music.load( backgroundMusic )
        except pygame.error, message:
            print 'Cannot load music:'
            raise SystemExit, message
        self.start_rect = pygame.Rect( 12, 81, 173, 111 )
        
        self.mouse_down_pos = (-1,-1)
    
    def enter(self):
        pass
        pygame.mixer.music.play(1)
        
    def exit(self):
        pass
        pygame.mixer.music.stop()
    
    def mouse_button_down( self, event ):
        self.mouse_down_pos = event.pos
    
    def mouse_button_up( self, event ):
        
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )
        
        if collides_down_and_up( self.start_rect ):
            print 'play!'
            self.switch_to_mode( 'Intro' )
    
    def draw( self, screen ):
        ## Draw the HUD.
        screen.blit( self.image, ( 0,0 ) )
        pygame.display.flip()

class Pause( GameMode ):
    def __init__( self ):
        ## Initialize the superclass.
        GameMode.__init__( self )
        
        self.image, _ = load_image( 'Pause.jpg' )
        self.start_rect = pygame.Rect( 23, 70, 150, 110 )
        
        self.mouse_down_pos = (-1,-1)
    
    def enter(self):
        pass
        
    def exit(self):
        pass
    
    def mouse_button_down( self, event ):
        self.mouse_down_pos = event.pos
    
    def mouse_button_up( self, event ):
        
        global lastMode
        
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )
        
        if collides_down_and_up( self.start_rect ):
            print 'play!'
            self.switch_to_mode( lastMode )
    
    def draw( self, screen ):
        ## Draw the HUD.
        screen.blit( self.image, ( 0,0 ) )
        pygame.display.flip()


class Hotspot():
    def __init__(self, rect, sound, name):
        self.rect = rect
        self.sound = sound
        self.name = name
        
class Exit():
    def __init__(self, rect, target):
        self.rect = rect
        self.target = target
class Object():
    def __init__(self, rect, item):
        self.rect = rect;
        self.item = item;
        

        

class Room( GameMode ):
    def __init__(self):
        GameMode.__init__(self)
        
        self.globals = json.load( open( os.path.join( kDataDir, kGlobals ) ) )
        
        
        ##Initialize to bedroom
        self.roomName = ''
        self.image = None
        self.exits = []
        self.hotspots = []
        #self.objects = []
        
        self._changeRoom('Bedroom')
        
        """    
        self.inventory = Inventory()
        self.message = ""
        """
        
        self.mouse_down_pos = (-1,-1)
        
    def _changeRoom(self, target):
        
        global lastMode
        lastMode = 'Room'
        
        if target is 'Bedroom':
            self.roomName = 'Bedroom'
            self.image, _ = load_image('NotePillow.jpg')
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(0,0,150,500), 'Kitchen'))
            self.hotspots.append(Hotspot(pygame.Rect(265, 235, 90, 85), load_sound('MichelleNote.wav'), "note"))
            
        elif target is 'Kitchen':
            self.roomName = 'Kitchen'
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(300, 430, 90, 70), 'Bedroom'))
            self.exits.append(Exit(pygame.Rect(0, 200, 70, 90), 'Garage'))
            self.exits.append(Exit(pygame.Rect(245, 190, 85, 55), 'Spices'))
            
            if self.globals['cookieEaten'] is 0:
                self.image, _  = load_image('Kitchen.jpg')
                self.hotspots.append(Hotspot(pygame.Rect(210, 301, 22, 11), load_sound('cookie.wav'), "cookie"))
            else:
                self.image, _ = load_image('KitchenSansCookie.jpg')
           
        elif target is 'Spices':
            self.roomName = 'Spices'
            self.image, _ = load_image('PepperCloseUp.jpg')
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(300, 430, 90, 70), 'Kitchen'))
            self.hotspots.append(Hotspot(pygame.Rect(100,85,125,335), load_sound('PepperOpen.wav'), "pepper"))
            
        elif target is 'Pepper':
            self.roomName = 'Pepper'
            self.image, _ = load_image('PepperNote.jpg')
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(300, 430, 90, 70), 'Kitchen'))
            self.hotspots.append(Hotspot(pygame.Rect(200,245,100,85), load_sound('ReadCombination.wav'), "combination"))
            
        elif target is 'Garage':
            self.roomName = 'Garage'
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(525, 0, 145, 500), 'Kitchen'))
            if self.globals['atticLocked'] is 1:
                self.image, _ = load_image('LockedAttic.jpg')
                self.exits.append(Exit(pygame.Rect(295, 80, 20, 30), 'Lock'))
            else:
                self.image, _ = load_image('OpenAttic.jpg')
                self.exits.append(Exit(pygame.Rect(200,0,220,500), 'Attic'))
            
        elif target is 'Lock':
            self.roomName = 'Lock'
            self.image, _ = load_image('Lock.jpg')
            self.hotspots = []
            if self.globals['haveCombination'] is 0:
                sound = load_sound('LockedLock.wav')
            else:
                sound = load_sound('OpenLock.wav')
            self.hotspots.append(Hotspot(pygame.Rect(205,20,240,330), sound, "lock"))
            self.exits = []
            self.exits.append(Exit(pygame.Rect(300, 430, 90, 70), 'Garage'))
            
        elif target is 'Attic':
            self.roomName = 'Attic'
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(300, 430, 90, 70), 'Garage'))
            if self.globals['atticDark'] is 1:
                self.image, _ = load_image('DarkAttic.jpg')
                self.hotspots.append(Hotspot(pygame.Rect(340, 245, 35, 35), load_sound('None'), "switch"))
            else:
                self.image, _ = load_image('LightAttic.jpg')
                self.exits.append(Exit(pygame.Rect(600, 200, 70, 90), 'Box'))
                
        elif target is 'Box':
            self.roomName = 'Box'
            self.image, _ = load_image('Box.jpg')
            self.hotspots = []
            self.exits = []
            self.exits.append(Exit(pygame.Rect(0, 200, 70, 90), 'Attic'))
            self.exits.append(Exit(pygame.Rect(110,65,560,435), 'CloseUpBox'))
            
        elif target is 'CloseUpBox':
            self.roomName = 'CloseUpBox'
            self.image, _ = load_image('CloseUpBox.jpg')
            self.hotspots = []
            self.hotspots.append(Hotspot(pygame.Rect(0,0,670,500), load_sound('BoxOpen.wav'), 'box'))
            self.exits = []
            
        
    def mouse_button_down( self, event ):
        self.mouse_down_pos = event.pos
        
    
    def mouse_button_up( self, event ):
        for hotspot in self.hotspots:
            hotspot.sound.stop()
            
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )

        for hotspot in self.hotspots:
            if collides_down_and_up( hotspot.rect):
                hotspot.sound.play()
                
                if self.roomName is 'Kitchen' and hotspot.name is 'cookie':
                    self.globals['cookieEaten'] = 1
                    self._changeRoom('Kitchen')
                elif self.roomName is 'Spices' and hotspot.name is 'pepper':
                    self._changeRoom('Pepper')
                elif self.roomName is 'Pepper' and hotspot.name is 'combination':
                    self.globals['haveCombination'] = 1
                    ##self._changeRoom('Kitchen')
                elif self.roomName is 'Attic' and hotspot.name is 'switch':
                    self.globals['atticDark'] = 0
                    self._changeRoom('Attic')
                elif self.roomName is 'Lock' and hotspot.name is 'lock' and self.globals['haveCombination'] is 1:
                    self.globals['atticLocked'] = 0
                    self._changeRoom('Garage')
                elif self.roomName is 'CloseUpBox' and hotspot.name is 'box':
                    self.switch_to_mode('End')
                print hotspot.name
                
        for exit in self.exits:
            if collides_down_and_up( exit.rect ):
                self._changeRoom(exit.target)
                print 'Change room'
         
        """         
        for object in self.objects:
            if collides_down_and_up( object.rect ):
                print 'Pick up object'
                object.item.onScreen = 0
                self.inventory.add(object.item)
                self.inventory.select(object.item.name)
                self.message = object.item.desc
        """
    
    def draw( self, screen ):
        screen.fill( ( 255,255,255) )
        screen.blit( self.image, ( 0,0 ) )
        
        """
        if pygame.font:
            font = pygame.font.Font( None, 24 )
            text = font.render( self.message, 1, ( 10, 10, 10 ) )
            textpos = text.get_rect( top = 505, bottom = 550, left = 5 )
            screen.blit( text, textpos )
       
           
       #Draw objects on screen
        for object in self.objects:
            if object.item.onScreen:
                screen.blit(object.item.onScreenImage, object.rect)
                
        ## Display Inventory
        if self.inventory.current is not None:
            screen.blit(self.inventory.current.inInvenImage, self.inventory.current.inInvenImage.get_rect(top = 575))
        """   
        
        pygame.display.flip()
        
    def key_down(self,event):
        if event.key == K_ESCAPE:
            self.switch_to_mode('Pause')
        

"""       
class Item():
    def __init__(self, name, onScreen, inInven, desc):
        self.name = name
        self.onScreenImage, _ = load_image(onScreen)
        self.inInvenImage, _ = load_image(inInven)
        self.desc = desc;
        
        self.onScreen = 1
        self.inInven = 0;
        
class Inventory():
    def __init__(self):
        self.dict = {}
        self.current = None
        self.listOfAllObjects = []
        
    def select(self, name):
        self.current = self.dict[name]
    
    def add(self, object):
        self.dict[object.name] = object
        self.listOfAllObjects.append(object.name)
        
    def remove(self, name):
        self.dict.remove(name)
        self.current = None;
    
    def hasEverHad(self, name):
        if self.listOfAllObjects.count(name) > 0:
            return True;
        else:
            return False;
       
 """     
        
def main():
    ### Load global variables.
    globals = json.load( open( os.path.join( kDataDir, kGlobals ) ) )
    
    
    ### Initialize pygame.
    pygame.init()
    screen = pygame.display.set_mode( globals['screen_size'] )
    pygame.display.set_caption( globals['window_title'] )
    clock = pygame.time.Clock()
    
    
    ### Set up the modes.
    modes = ModeManager()
    
    
    ### Set up Splash Screen
    image, _ = load_image( 'Splash.jpg' )
    modes.register_mode('SplashScreen',Cutscene(image,load_sound('None'),3000,'MainMenu'))
    
    ### Set up Main Menu
    modes.register_mode('MainMenu', MainMenu())
    
    ### Set up Pause Screen
    modes.register_mode('Pause', Pause())
    
    ## Set up intro cutscene modes.
    image, _ = load_image( 'BlackScreen.png' )
    sound = load_sound('MichelleIntro.wav')
    modes.register_mode( 'Intro', Cutscene(image, sound, 21000, 'Sleep' ) )
    
    modes.register_mode('End', Cutscene(image, load_sound('None'), 5000, 'End'))
    
    image, _ = load_image( 'WakeUp.jpg' )
    sound = load_sound('AhGloriousSleep.wav')
    modes.register_mode( 'Sleep', Cutscene(image, sound, 8000, 'Huh' ) )
    
    image, _ = load_image( 'NotePillowSansArrow.jpg' )
    sound = load_sound('HuhWhatsThisAndOpen.wav')
    modes.register_mode( 'Huh', Cutscene(image, sound, 5000, 'Note' ) )
    
    image, _ = load_image( 'Note.jpg' )
    sound = load_sound('CarolineNote.wav')
    modes.register_mode( 'Note', Cutscene(image, sound, 22000, 'Room' ) )
    
    
    
    modes.register_mode('Room', Room())
    
    ## Start with Splash
    modes.switch_to_mode( 'SplashScreen' )
    
    
    ### The main loop.
    fps = globals['fps']
    while not modes.quitting():
        clock.tick( fps )
        
        ## Handle Input Events
        for event in pygame.event.get():
            
            if event.type == QUIT:
                modes.switch_to_mode(None)
                break
            
            elif event.type == KEYDOWN:
                modes.current_mode.key_down( event )
            
            elif event.type == KEYUP:
                modes.current_mode.key_up( event )
            
            elif event.type == MOUSEMOTION:
                modes.current_mode.mouse_motion( event )
            
            elif event.type == MOUSEBUTTONUP:
                modes.current_mode.mouse_button_up( event )
            
            elif event.type == MOUSEBUTTONDOWN:
                modes.current_mode.mouse_button_down( event )
        
        modes.current_mode.update( clock )
        modes.current_mode.draw( screen )
    
    
    ### Game over.
    
    ## TODO: Save game state (see pygame.register_quit()).


## this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
