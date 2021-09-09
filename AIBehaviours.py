from enum import Enum
import globals
class behaviour(Enum):
    WANDER = 0
    APPROACH = 1
    EAT = 2
def ParseBehaviour(actor,behaviour):
    def wander():
        actor.move_object((0,1))
    def approach():
        target = globals.multiverse[globals.currentUniverse].actors[globals.playerId]
        distance = pygame.math.Vector2(tuple(map(sub, target.pos, actor.pos)))
        if distance != (0, 0):
            direction = pygame.math.Vector2(tuple(map(sub, target.pos, actor.pos))).normalize()
            direction = (math.floor(direction.x), math.floor(direction.y))
            actor.move_object(direction)
    def eat():
        pass
    listOfBehaviour = {behaviour.EAT:eat,behaviour.WANDER:wander,behaviour.APPROACH:approach}
    if behaviour in listOfBehaviour:
        listOfBehaviour[behaviour]()