Source code:
  1. Ingredients.py: contains the class for the game's ingredients and its attributes. 
  2. Plate.py: contains the class for the game's plates and its attributes.
  3. Player.py: contains the class for the game's player and its attributes.
  4. RecipeMaker.py: contains a random recipe generator that makes use of Ingredients.py and Target_Recipes.py.
  5. Station.py: contains the class for our game's stations and its attributes.
  6. Station_Manager.py: contains the class for our station manager that manages all the different stations in our game.
  7. Target_Recipes.py: contains all the ingredients that will be used in our game along with recipes with their base ingredients. There is also a method to generate an ingredient with random cook and cut states to make randomized recipes.
  8. OvercookedTxtBased.py: the main program to run the text-based game.

Reference to learn how to make a text-based game implementation on Python was inspired by: https://www.youtube.com/channel/UCZody_lpDx8QI4BEn7frBHg

Design: Starting the OvercookedTxtBased.py file will run the game where a player can input their name and start off with nothing. The player can then move around and complete actions that require speech. All the game logic is handled here and is accurate to what we are planning to do in our final game. A submission of a recipe, whether correct or not, will yield a + or - 1 in the score and a new recipe will be generated for the player to attempt to achieve.

Bugs: The full speech implementation in regards to word processing has not been fully optimized yet. As of now, the program requires for the exact word to be captured in order to function properly. If there are words that may conflict or are not produced exactly the same as in the code, a player will be stuck. Thus, further changes need to be made to provide more leniency to the game and the player.

Plan:
  1. From test trials, gather which words are commonly mispronounced or misinterpreted and classify them with their correct words. This will allow the program to accept more types of similar results so players are not forced to always speak with 100% accuracy.
  2. Instead of using the 'Enter' key to call listen(), use a physical button attached to the Pi to call listen(); need to use MQTT based on our game's system design
