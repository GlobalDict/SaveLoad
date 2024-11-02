# GlobalDict :)

from Range import *

class SaveLoad(types.KX_PythonComponent):

    args = {
        "Range File Name": "",
        "Extension Name": "" ,
        "Player Speed": 2.0
    }

    def awake(self, args):
        # Add gui overlay scene to see buttons and labels
        logic.addScene("GUI", 1)

        self.scene = logic.getCurrentScene()
        self.GUI = logic.getSceneList()

        self.mouse = logic.mouse
        self.leftClick = self.mouse.inputs[events.LEFTMOUSE]

        self.keyboard = logic.keyboard.inputs
        self.W = self.keyboard[events.WKEY]
        self.S = self.keyboard[events.SKEY]
        self.A = self.keyboard[events.AKEY]
        self.D = self.keyboard[events.DKEY]

        # Define the dictionary
        self.dict = logic.globalDict

        # Make sure your string value is similar to the current .range file
        # Maybe in the future it will be possible to <logic.getCurrentRangeFileName()> or I just don't know how to do that :)
        self.rangeFile = args["Range File Name"]

        # Give your dictionary file a name of the script owner [self.object] 
        self.saveName = str(self.object.name)

        # Specify your prefered extension name.
        # Random nonsense : I dont think its wise to use "range or blend" or any other known binary file extensions :)
        self.extension = args["Extension Name"]

        # Create a full name for your dictionary by joining the current range file name and your self.saveName
        # Avoid using logic.expandPath("//") because you wont be able to save data in standalone mode. Save inside a range file instead.
        # The saved file will be in a folder named something like: {self.rangeFile}.range~{self.rangeFile} > testFile.range~testFile
        # The saved file will be named: {self.object.name.{self.extension}} > Player.myExtension
        self.dataFile = f"{self.rangeFile}\{self.saveName}"

        # Expand the current self.rangeFile directory
        self.path = logic.expandPath("//")

        # Get the data text file. 
        # This is where python will check if player saved some game data or not
        # NB: Do not delete this file. If you do, create it manually, or inside awake() by comanding:
        #           if "hasDict.txt" not in self.path:
        #               file = open(self.path + "hasDict.txt", "w")
        #               file.close()
        self.hasDict = self.path + "hasDict.txt"

        # Speed to move the player
        self.speed = args["Player Speed"]

        # Player health
        # You can also use int or float prop(s)
        self.health = 100
        
        # Create dictionary keys
        # This is not necessary but it helps "me" remember what type of data should each key get :)
        self.dict["Position"] = ()      # Manages object's world position
        self.dict["Orientation"] = ()   # Manages object's world orientation
        self.dict["Health"] = int()     # Manages object's health

    # Range developers recomends awake() instead of start()
    # simply, awake() initialises faster than start()
    def start(self, args):
        pass
    
    # Manages player movement
    def movement(self):
        # Local speed variable with global speed multiplied by the engine's delta time.
        speed = self.speed*logic.deltaTime()

        # Movement function to avoid typing "self.object.applyMovement([vector3])" over and over
        def move(x,y):
            self.object.applyMovement([x,y,0], True) # Z axis is 0 because we dont want any vertical translations

        if self.W.active: move(0, speed)  # Move forward
        if self.S.active: move(0, -speed) # Move backward
        if self.A.active: move(-speed, 0) # Move left
        if self.D.active: move(speed, 0)  # Move right

    # Manages button(s) hovers and clicks
    def buttons(self):
        # First check if a scene named "GUI" is in [self.GUI = logic.getSceneList()]
        if "GUI" in self.GUI:
           
            # If true then start getting the guiScene and elements
            gui = self.GUI["GUI"]
            
            health = gui.objects["Health"] # Text to display player's health
            saveBut = gui.objects["Save"] # Save button
            loadBut = gui.objects["Load"] # Load button
            rotateBut = gui.objects["Rotate"] # Rotate button
            selector = gui.objects["Selector"] # Hover or Selection indicator
            guiCamera = gui.objects["GuiCam"] # GUI scene's "active" camera

            # Set the health text's text attribute to self.object(player)'s health percentage
            health.text = f"{int(self.health)}%"
            
            # Create a list containing mouse cursor's screen position x and y
            cood = [self.mouse.position[0], self.mouse.position[1]] # cood for coodinates

            # Get a screen ray casted from GUI camera to the mouse position
            # The function returns a KX_GameObject hit by the ray
            mouseOver = guiCamera.getScreenRay(cood[0],cood[1],100)

            def colorChanger():
                # Change selector color if mouse left is active
                if self.leftClick.active: 
                    # Change selector color
                    mat = selector.meshes[0].materials[0].diffuseColor = (0, 0.05, 0.3)
                else:
                    # Reset selector color
                    mat = selector.meshes[0].materials[0].diffuseColor = (1, 0, 0)
           
            # Check if the mouse cursor is hovering over the Save button
            if mouseOver == saveBut:
                # Indicate by copying saveBut's x position to the selector object
                selector.worldPosition[0] = saveBut.worldPosition[0]

                colorChanger() # Allow save button to do selector color changing when clicked

                # Check if left mouse is just clicked and save the game
                if self.leftClick.activated:

                    # Write string "yes" to hasDict.txt
                    # This will allow us to check if any data has been saved. if no data, it wont be possible to do call self.load()
                    # And our game wont crush
                    with open(self.hasDict, 'w') as file:
                        file.write("yes")
                        file.close() # Always close file(s) after writing
                    self.save()
                
            # Check if the mouse cursor is hovering over the Load button
            elif mouseOver == loadBut:
                # Indicate by copying loadBut's x position to the selector object
                selector.worldPosition[0] = loadBut.worldPosition[0]

                colorChanger() # Allow load button to do selector color changing when clicked

                # Check to see if any data has been saved by reading hasData.txt
                with open(self.hasDict, "r") as file:
                    if "yes" in file.readline():
                        # Check if left mouse is just clicked and load the saved game data
                        if self.leftClick.activated:
                            self.load()
                        file.close() # Always close file(s) after reading
                
            # Check if the mouse cursor is hovering over Rotate button
            elif mouseOver == rotateBut:
                # Indicate by setting selector's x & y pos to rotateBut
                selector.worldPosition[0] = rotateBut.worldPosition[0]
                selector.worldPosition[1] = rotateBut.worldPosition[1]

                colorChanger() # Allow rotate button to do selector color changing when clicked

                if self.leftClick.active:
                    # Rotate player clockwise: for demo only
                    self.object.applyRotation([0, 0, -self.speed*logic.deltaTime()])
                    health.text = f"{self.object.name} is rotating"
                
            # Always hide the selector object
            else:
                selector.worldPosition[0] = -5.0
                selector.worldPosition[1] = -1.23056
    
    # Handles the process of saving game data
    def save(self):
        # Assign values to your dictionary keys then save
        # Do not save before assigning !
        self.dict["Position"] = tuple(self.object.worldPosition)
        self.dict["Orientation"] = tuple(self.object.worldOrientation.to_euler())
        self.dict["Health"] = self.health # You don't need an interger health propery (use a self.health from awake())

        # Save the dictionary (self.dict)
        logic.saveGlobalDict(self.dataFile, self.extension)

    # Handles the process of loading game data
    def load(self):
        # Load the dictionary first before applying dictionary data to your object
        logic.loadGlobalDict(self.dataFile, self.extension)

        self.object.worldPosition = self.dict["Position"]
        self.object.worldOrientation = self.dict["Orientation"]
        self.health = self.dict["Health"]

    def update(self):
        # Subtract 1 from health if health is above 0 to avoid negative health percentage
        if self.health > 0:
            self.health -= 1*logic.deltaTime() # multiply by delta time to avoid subtracting on every frame

        # Call your buttons and movement function here.
        # If you dont, their logic wont work
        self.buttons()
        self.movement()
