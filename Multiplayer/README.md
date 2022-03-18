# Multiplayer README

Source Code:
- building_blocks.py: Contains utility functions for the socket connection, as well as game logic. These functions encapsulate operations such as sending and retrieving the game state asynchronously, processing actions, and establishing connections.
- overcookedIRL_client.py: Contains the code needed to start up the client, register, and connect to the game hosting server.
- overcookedIRL_server.py: Contains the code needed to start up the server, establish connections with clients, process game data sent by the player, and more.

References:
For the code on allocating threads to different connections, as well as implementing multi-threaded functions, please refer to this link as a starter: https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/

Design:
The socket client-server connection uses nonblocking asynchronous logic to ensure that player requests can be handled immediately, without blocking (which holds up the connection. Additionally, threaded functions will run in the background of the game logic functions, to ensure that clients are able to receive live updates to the game state and so that the server can send any changed game states immediately.

Bugs:
Since the text game is merely a placeholder (we plan to hook up this framework to the visuals based single-player prototype that we demoed during the final presentation), there are flaws on the server side processing the data (e.g. what if we input an invalid command?). Additionally, the server is programmed to handle two teammates for now, but obviously we would like more customizeability on this later Spring Quarter 2022.

Plan:
- Integrate with the visuals-based prototype game.
- Add more fail safe checks to guard against invalid inputs (e.g. if speech recognized the ingredient name incorrectly, how should the server process this incorrect name?)
- Further customizeability with different game modes and setups.
- The implementation with the user interface (intro screen, title screen, etc.) in the 'Newton' branch has not been merged with the 'main' branch as there are currently some merge conflictions that need to be dealt with. 
