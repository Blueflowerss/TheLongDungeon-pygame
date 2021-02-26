import globals
def move_object(object,amount):
    globals.initialize()
    ourUniverse = globals.multiverse[globals.currentUniverse]
    if (object.x+amount[0],object.y+amount[1]) in ourUniverse.board:
        curBoard = ourUniverse.board[object.x + amount[0], object.y + amount[1]]
        
        def actor():
            pass
        def null():
            object.x, object.y = curBoard.x, curBoard.y
        collisions = {"actor":actor,"null":null}
        if (curBoard.x,curBoard.y) in ourUniverse.objectMap:
            target = ourUniverse.objectMap[curBoard.x,curBoard.y]
            if target.type is not None:
                if target.type in collisions:
                    collisions[target.type]()
                else:
                    pass


        else:
             collisions["null"]()