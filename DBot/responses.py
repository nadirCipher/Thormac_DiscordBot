from random import choice, randint
from maths import score_calc
from data_manager import create_account
from data_manager import read_data
from data_manager import edit_account
import json
import os

def Match_Input(Winner, Looser, Confirmer) -> str:
    #ADD "and Looser != Confirmer" BEFORE DEPLOY
    if Winner != Looser and Winner != Confirmer and Looser != Confirmer: 
        create_account(Winner)
        create_account(Looser)
        score_calc(Winner, Looser, Winner)
        return (int(read_data(Winner, "scale")), int(read_data(Looser, "scale")), Winner, Looser)
    else:
        return("You cant have the same person confirm Win AND Loose dumby XD")
    
def Score_finder(user) -> str:
    if os.path.exists("user_data.json"):
        with open("user_data.json", 'r') as file:
            accounts = json.load(file)
    if user in accounts:
        scale = float(read_data(user, "scale"))
        return(int(scale*100)/100)
    else:
        return(f"sorry but it does not seam we have data on {user} just yet")

def Opt_in(user) -> str:
    create_account(f"<@{user}>")
    if read_data(f"<@{user}>", "opt_in") == "true":
        return(f"<@{user}> Your already opted in!")
    else:
        edit_account(f"<@{user}>", "opt_in", "true")
        return(f"Glad to see <@{user}> is joining in!")

def Opt_out(user) -> str:
    create_account(f"<@{user}>")
    if read_data(f"<@{user}>", "opt_in") == "false":
        return(f"<@{user}> Your already opted out!")
    else:
        edit_account(f"<@{user}>", "opt_in", "false")
        return(f"Sad to see <@{user}> cant play any more")
    


# Match_Input("test1", "test2", "test3")