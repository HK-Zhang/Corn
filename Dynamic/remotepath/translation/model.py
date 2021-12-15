import sys
import os


def verify_rule(rulePath, model_result):
    sys.path.append(rulePath)
    from collide import expect, load_data

    ship_a = {"size": 5} if model_result == None else {"size": 5}
    ship_b = {"size": 10} if model_result == None else {"size": 10}
    load_data(ship_a, ship_b)
    ship_e = expect()
    if(model_result["ship_to_move"]["size"] == ship_e["size"]):
        print("success")
    else:
        print("fail")
