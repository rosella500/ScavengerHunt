import os, pygame, json, csv
from cutscene import *
from hotspot import *
from exit_class import *
from object_class import *
from modes import ModeManager, GameMode, SimpleMode
from pygame.locals import *
from utils import *

kDataDir = 'data'
kGlobals = 'globals.json'
globals = ''



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
        
        print "switching to " + target
        
        with open('Rooms.csv', 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[0] == target:
                    print "Found "+ target
                    self.roomName = row[0].strip()
                    self.image, _ = load_image(row[1].strip())
                    self.hotspots = []
                    self.exits = []
                    hotspots = row[2].split(";")
                    hotspots = hotspots[:-1] ##If all rows end in a semi-colon, there will be an extra hotspot with no data
                    for spot in hotspots:
                        info = spot.split(",")
                        name = info[0].strip()
                        sound = info[1].strip()
                        x = int(info[2])
                        y = int(info[3])
                        width = int(info[4])
                        height = int(info[5])
                        self.hotspots.append(Hotspot(pygame.Rect(x,y,width,height), load_sound(sound), name))
                    
                    exits = row[3].split(";")
                    exits = exits[:-1] ##If all rows end in a semi-colon, there will be an extra exit with no data
                    for exit in exits:
                        info = exit.split(",")
                        name = info[0].strip()
                        x = int(info[1])
                        y = int(info[2])
                        width = int(info[3])
                        height = int(info[4])
                        self.exits.append(Exit(pygame.Rect(x,y,width,height), name))
                        
        
        ## Add special cases to rooms
        if target == 'Kitchen':
            print "Target is Kitchen"
            print self.globals['cookieEaten']
            if self.globals['cookieEaten'] == 0:
                self.image, _  = load_image('Kitchen.jpg')
                self.hotspots.append(Hotspot(pygame.Rect(210, 301, 22, 11), load_sound('cookie.wav'), "cookie"))
            else:
                self.image, _ = load_image('KitchenSansCookie.jpg')
           
        elif target == 'Garage':
            if self.globals['atticLocked'] == 1:
                self.image, _ = load_image('LockedAttic.jpg')
                self.exits.append(Exit(pygame.Rect(295, 80, 20, 30), 'Lock'))
            else:
                self.image, _ = load_image('OpenAttic.jpg')
                self.exits.append(Exit(pygame.Rect(200,0,220,500), 'Attic'))
            
        elif target == 'Lock':
            print self.globals['haveCombination']
            if self.globals['haveCombination'] == 0:
                sound = load_sound('LockedLock.wav')
            else:
                sound = load_sound('OpenLock.wav')
            self.hotspots.append(Hotspot(pygame.Rect(205,20,240,330), sound, "lock"))
            
        elif target == 'Attic':
            if self.globals['atticDark'] == 1:
                self.hotspots.append(Hotspot(pygame.Rect(340, 245, 35, 35), load_sound('None'), "switch"))
            else:
                self.image, _ = load_image('LightAttic.jpg')
                self.exits.append(Exit(pygame.Rect(600, 200, 70, 90), 'Box'))

            
        
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
                
                
                if hotspot.name == 'cookie':
                    self.globals['cookieEaten'] = 1
                    self._changeRoom('Kitchen')
                elif hotspot.name == 'pepper':
                    self._changeRoom('Pepper')
                elif hotspot.name == 'combination':
                    self.globals['haveCombination'] = 1
                    print self.globals['haveCombination']
                    ##self._changeRoom('Kitchen')
                elif hotspot.name == 'switch':
                    self.globals['atticDark'] = 0
                    self._changeRoom('Attic')
                elif (hotspot.name == 'lock' and self.globals['haveCombination'] == 1):
                    self.globals['atticLocked'] = 0
                    self._changeRoom('Garage')
                elif hotspot.name == 'box':
                    self.switch_to_mode('End')
                    
                print hotspot.name
                
                """
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
                """
                
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
        
    """
    def key_down(self,event):
        if event.key == K_ESCAPE:
            self.switch_to_mode('Pause')"""
