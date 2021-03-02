import globals
import classes
def move_object(object,amount):
    globals.initialize()
    ourUniverse = globals.multiverse[globals.currentUniverse]
    if (object.pos[0]+amount[0],object.pos[1]+amount[1]) in ourUniverse.board:
        curBoard = ourUniverse.board[tuple(map(sum, zip(object.pos, amount)))]
        def actor():
            pass
        def wall():
            pass
        def empty():
            object.pos=curBoard.pos
        collisions = {"actor":actor,"wall":wall,"empty":empty}
        if (curBoard.pos) in ourUniverse.objectMap:
            target = ourUniverse.objectMap[curBoard.pos]
            if target.type is not None:
                if target.type in collisions:
                    collisions[target.type]()
                else:
                    pass
        elif (curBoard.pos) in ourUniverse.board:
            target = ourUniverse.board[curBoard.pos]
            if target.type in collisions:
                collisions[target.type]()


        else:
             collisions["empty"]()
def alter_tile(tile,id):
    globals.initialize()
    ourUniverse = globals.multiverse[globals.currentUniverse]
    if tile in ourUniverse.board:
        ourUniverse.board[tile].__init__(tile[0],tile[1],id)
    else:
        ourUniverse.board[tile] = classes.Tile(tile[0],tile[1],"empty")