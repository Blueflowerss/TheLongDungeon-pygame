import globals

class Object(object):
    pass

items = Object()
entities = Object()
actors = Object()

items.database = []
items.dict = {}

entities.database = []
entities.dict = {}

actors.database = []
actors.dict = {}
flagDefinitions = {
    "item":{"pos":(0,0),"sprite":1,"displayname":"","weight":1,"meleedamage":1}
}
loadedItems = globals.readFromFile("data/items/general.json",True)
def createItem(flags,data):
    item = Object()
    for flag in flags:
        if flag in flagDefinitions:
            definition = flagDefinitions[flag]
            for attribute in definition:
                setattr(item,attribute,definition[attribute])
    item.flags = flags
    for attribute in data:
        setattr(item,attribute,data[attribute])
    return item
def loadItems():
    for item in loadedItems:
        itemClass = createItem(item["flags"],item["data"])
        items.dict[itemClass.devname] = len(items.database)
        items.database.append(itemClass)
def getItem(Devname):
    return items.database[items.dict[Devname]]
