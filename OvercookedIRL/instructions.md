v0.1 Instructions:

Note: This version is not robust and prone to errors. It will probably be easy to "break" the game. Any errors you discover while playing the game will become fixes for us in the future.

pub.py needs to be running in another window. It's a mqtt publisher that the game publishes and subscribes to.

Move:
    Click on an area for the character to walk there.
    
Registering a location:
    Click on the counter in order to register that the character is at the counter. Actions can only be performed if a location is registered. 
    Be wary of clicking "too far" off the counter; the character may get stuck and you may not be able to gain control of its movement after that. 

Actions:
    Actions are performed by pressing the 'a', 'u', 'd', or 'c' buttons.
    Viable buttons will vary per station.
    While a button is pressed, a corresponding message will be sent to a publisher (overcooked_mic), and the publisher will send a reponse back. Depending on the response recevied, an action sequence will commence. 
    Make sure that pub.py is running in order for actions to be registered (character waits for response from mqtt pulisher running on pub.py).
    Note about button sensitivity: it may be difficult to trigger a button press (due to the implementation of checking when the button is experiecing a key_up event), so you may need to spam the button a few times before it is registered. If an animation starts playing, then the button press has been registered. Continuing to spam a button after the action has been registered could "break" the game; this is a possible test for us to perform.

Animations:
    Thought Bubbble: the thought bubble will play once an action as been registered and until a response is received from the publisher. In the final game, it will probably play while speech detection is being peformed and until a word is recognized. 

Locations:
    Ingredients Stand
    Left Counter
    Right Counter
    Top Counter
    Bottom Counter
    Cooking Station
    Chopping Station
    Plates Station

Ingredients Stand:
    From L to R: 1-Tomato, 2-Lettuce, 3-Meat, 4-Bun
    Actions: 
        'a' to get ingredient. Fridge open animation means getting ingredient sequence has started 


Left Counter
Right Counter
Top Counter
Bottom Counter:
    Actions:
        'u' to pick up
        'd' to put down
    Thought bubble animation means waiting for publisher response to confirm action


Cooking Station
    Actions:
        'u' to pick up
        'd' to put down
        'c' to start chopping
    When the cooking sequence is initiated, the game will wait for three "Chop" messages from the publisher. The publisher is hardcoded to send a "Chop" message once every 5 seconds. 

Chopping Station
    Actions:
        'u' to pick up
        'd' to put down
        'c' to start cooking
    When the cooking sequence is initiated, the game will wait for three "Stir" messages from the publisher. The publisher is hardcoded to send a "Stir" message once every 5 seconds. 


Plates Station
    Actions:
        'u' to pick up

