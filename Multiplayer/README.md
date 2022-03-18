Source code:
  1. Combins source code from Multiplayer text based and old final game implementation (new version is in branch 'v0.1').
  2. input_box.py: contains code to create an input box that players can type in
  3. button.py: contains code to create a button

Design: Adds a user interace to the multiplayer aspect version of our game so that players can see that they must connect to a server and wait for all other players to connect. With a proper connection and all players ready to play, the old implementation of our game will appear signaling the simultaneous start of the game for both players.

References:
  1. For the button: https://github.com/russs123/pygame_tutorials/tree/main/Button
  2. For the input box: https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

Bugs: There are many bugs as this is not our full implemenation of our game. For example, the Multiplayer version is currently text based and our visuals do not correspond with that so inherently the logic is flawed. This is mainly to test the multiplayer framework and to get a working user interface. 

Plans: The user interface will continue to be improved to allow for a player to be able to customize the game. The first player who joins will be deemed the 'Host' and can make these changes. For example, changing the time and score limit as well as stating how many players are playing.
