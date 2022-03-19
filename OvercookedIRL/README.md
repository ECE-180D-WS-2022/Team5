# OvercookedIRL 
This folder contains our implementation of a single-player Overcooked game with (minimally) functional game logic and visuals. 

## Files
### img

 - This folder contains the spritesheets that were used to produce the game's objects and animations. 

### src
- main.py: Contains our implementation of a Game class. The game is initiated using this file. 
- player.py: Contains our implementation of the Player class, complete with animations. The majority of the game logic is contained in this file. The player class handles collision detection with kitchen counters and checks if an action initiated by a player using a keyboard press is valid at a particular location. For instance "pick up" and "put down" actions are valid at every kitchen counter, but "chop" actions are only valid at chop counters, and "stir" actions are only valid at cook counters. Additionally, the player class publishes and receives messages from the speech recognition and gesture detection programs after an action as has been initiated. The player class is responsible for changing objects' states and producing different animations relevant to the game state. 
- pub.py: Contains our implementation of the speech recognition program, which communicates with the main game using MQTT. 
- color.py: Our localization implementation, same as the file in the main branch. 
- counters.py: Contains our implementation of the kitchen counters displayed in our game. There are 4 classes of counters and players can interact with each counter in different ways. For instance, players can only acquire ingredients at an ingredient counter. Players can pick up and put down items at a basic counter freely. Players can only place raw ingredients at a chop counter and only chopped ingredients at a cook counter. 
- ingredients.py: Contains our implementation of the Ingredients class. Each ingredient has an image, which may change after it has been chopped or cooked. The ingredients class also contain class variables tracking the number of times an ingredient has been chopped and cooked. 
- animations.py: Includes the classes used to produce animations such as the fridge door opening, the speech bubble, and knife chopping. 
 - config.py: Contains the global variables and tilemap arrays used by our game.

#### Bugs and TODO's:
- Collision detection between the player and kitchen counters is full of bugs and not robust. Currently, collision detection only works under certain conditions. If a player intends for the avatar to travel to a location whose collision detection mechanism has not been properly debugged, the avatar will get stuck at that location, and the player will lose control of their avatar's movement. The collision detection conditions need to be further tested and fixed. 
- When a player is at a chopping station or cooking station, the code is written in such a way that a player must complete three chop or cook gestures before they are allowed to perform another action or travel to another location. Additionally, if a player has initiated speech recognition, they must wait for the microphone to start, say their commands, and wait for the results of the speech recognizer before commencing with their next action. However, during the play-through of the final game, players may wish to stop an action mid-way in order to perform another action that will be more beneficial due to the time constraint. As a result, more code needs to be added to the game logic so that players are allowed to click away in the middle of an action to indicate that they wish to stop that action. 
- Currently, the game is implemented so that players can make unlimited variations of the hamburger recipes using the ingredients provided. However, a list of orders to complete and a scoring system has not yet been implemented, which is the next TODO on our list. 
