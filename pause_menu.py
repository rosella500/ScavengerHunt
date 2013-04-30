import os, pygame, json
from room import *
from hotspot import *
from modes import ModeManager, GameMode, SimpleMode
from pygame.locals import *
from utils import *

kDataDir = 'data'
kGlobals = 'globals.json'
globals = ''


class PauseMenu(GameMode):
    def __init__(self):
        GameMode.__init__(self)
        self.globals = json.load( open( os.path.join( kDataDir, kGlobals ) ) )
        self.roomName = 'PauseMenu'
        self.image, _ = load_image('PauseMenu.jpg')
        self.hotspots = []
        temp = self.globals['current_note']
        self.hotspots.append(Hotspot(pygame.Rect(20, 425, 200, 200), load_sound(temp), "current_note"))
        self.mouse_down_pos = (-1,-1)#need default position for mouse

    def mouse_button_down( self, event ):
        #print("pause menu test 1")
        self.mouse_down_pos = event.pos

    def mouse_button_up( self, event ):
        #print("pause menu test 2")
        for hotspot in self.hotspots:
            hotspot.sound.stop()
            
        def collides_down_and_up( r ):
            return r.collidepoint( self.mouse_down_pos ) and r.collidepoint( event.pos )

        for hotspot in self.hotspots:
            #print("pause menu test 3")
            if collides_down_and_up( hotspot.rect):
                hotspot.sound.play()

                if self.roomName is 'PauseMenu' and hotspot.name is 'current_note':
                    self.hotspots = []
                    temp = self.globals['current_note']
                    self.hotspots.append(Hotspot(pygame.Rect(20, 425, 200, 200), load_sound(temp), "current_note"))
                print hotspot.name
                
    def update_current_note(self, wavFile):
        self.globals['current_note'] = wavFile
        self.hotspots = []
        temp = self.globals['current_note']
        self.hotspots.append(Hotspot(pygame.Rect(20, 425, 200, 200), load_sound(temp), "current_note"))

    def draw( self, screen ):
        screen.fill( ( 255,255,255) )
        screen.blit( self.image, ( 0,0 ) )        
        pygame.display.flip()
