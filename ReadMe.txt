So for my code, it's organized into two main modes. One mode is a cutscene and plays a sound, waits for a pre-determined amount of time, and then switches to the next mode (which may be another cutscene). This is almost entirely the same as the splash screen example in class but with added sound functionality. 

The other main mode is the room exploration mode. Rooms have both exits and hotspots. Exits just move you from room to room (and the term room is used very loosely, a different room could be just a different angle), while hotspots play a sound.

Hotspots are also handled in the mouse_button_up() handler because they can have effects like changing global flags. 

To play the game, you just have to click on things. The arrows will lead you from room to room while certain hotspots in each area will also affect things, so click whatever looks interesting. I recommend the cookie. Cookies are delicious.

Also, my design has not changed much from the original design document. The prototype is obviously a small porion of the game with limited puzzles, limited interactivity, and limited tools to build an ambiance, but I think it still holds up well. The main change I made was that I'm relying more on global flags and have disabled the inventory for now. If I end up working more on this game for the final project, I'm sure the inventory will come back, if only for puzzle variety.