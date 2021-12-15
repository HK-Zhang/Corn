ship_a = {}
ship_b = {}

def load_data(ship_a_value,ship_b_value):
    global ship_a
    global ship_b
    ship_a = ship_a_value
    ship_b = ship_b_value


def prerequisite():
    if ship_a == None or ship_b == None:
        print("Failed - Object is not recognized")
        return False
    if ship_a["size"] == None or ship_b["size"] == None:
        print("Failed - Object size is not recognized")
        return False
    return True


def collide_rule():
    if ship_a["size"] > ship_b["size"]:
        ship_a["move"] = False
        ship_b["move"] = True
    else:
        ship_a["move"] = True
        ship_b["move"] = False


def expect():
    if prerequisite() == True:
        collide_rule()
    if(ship_b["move"] == True): 
        return ship_b
    else:
        return ship_a
        
