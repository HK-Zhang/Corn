import sys
import os

# def verify(rulePath, translationPath):
#     sys.path.append(rulePath)
#     sys.path.append(translationPath)
#     import collide
#     collide.collide()

# verify(r"./remotepath/rules",r"./remotepath/translation")

model_result={"ship_to_move":{"size":5}}
rule_path = os.path.abspath(r"./remotepath/rules")
model_verfication_script = os.path.abspath(r"./remotepath/translation")
sys.path.append(model_verfication_script)
from model import verify_rule
verify_rule(rule_path,model_result)