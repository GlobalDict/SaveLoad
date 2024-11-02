Workd in standalone !!

This component is designed to demonstrate how game data is saved and retrived efficiently in Range Engine.
Feel free to modify the script to suit your needs.
Func(s) "save()" and "load()" contains code responsible for saving and loading.
Func "movement()" contains code responsible for moving player around.
Func "buttons" contains code responsible for GUI elements functionalities and save_load triggers

hasDict.txt file is very essential. Read saveLoad.py line 52-57.
Pehaps you delete the "{self.rangeFile}.range~{rangeFile}" folder intentionally or unintentionally,
consider manually opening and deleting string "yes" from hasDict.txt because if load button is pressed,
hasDict.txt.yes will authorise Range to find a saved dictionary which is not there and Range runtime will freeze
