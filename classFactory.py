import globals,copy,os

class Object(object):
    pass

objects = Object()
entities = Object()
actors = Object()

objects.database = []
objects.dict = {}

entities.database = []
entities.dict = {}

actors.database = []
actors.dict = {}
flagDefinitions = {
    "base":{"devname":""},
    "item":{"pos":(0,0),"sprite":1,"displayname":"","weight":1,"meleedamage":1},
    "furniture":{"pos":(0,0),"sprite":1},
    "door":{"state":False,"spriteTrue":1,"spriteFalse":1},
    "sign":{"text":""}
}
saveableData = [
    "pos","state","text"
]
blueprints = []
for file in sorted(os.listdir("data/blueprints")):
    loadedItems = globals.readFromFile("data/blueprints/"+file,True)
    blueprints.extend(loadedItems)
def initObject(entity):
    def door():
        if entity.state == True:
            entity.sprite = entity.spriteTrue
            try:
                entity.flags.remove("blocks")
            except:
                pass
        else:
            entity.sprite = entity.spriteFalse
            if "blocks" not in entity.flags:
                entity.flags.append("blocks")
    objectTypes = {"door":door}
    for flag in entity.flags:
        if flag in objectTypes:
            objectTypes[flag]()
def createObject(flags,data):
    item = Object()
    item.flags = flags
    for flag in flags:
        if flag in flagDefinitions:
            definition = flagDefinitions[flag]
            for attribute in definition:
                if attribute != "flags":
                    setattr(item,attribute,definition[attribute])
            if "flags" in definition:
                for innerFlag in definition["flags"]:
                    if innerFlag not in item.flags:
                        item.flags.append(innerFlag)
    for attribute in data:
        setattr(item,attribute,data[attribute])
    return item
def loadObjects():
    for object in blueprints:
        itemClass = createObject(object["flags"],object["data"])
        objects.dict[itemClass.devname] = len(objects.database)
        objects.database.append(itemClass)
def getObject(Devname):
    if Devname in objects.dict:
        item = copy.deepcopy(objects.database[objects.dict[Devname]])
        return item
