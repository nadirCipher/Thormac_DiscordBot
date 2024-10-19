from account_manager import create_account
from account_manager import edit_account
from account_manager import read_data

diffrence_weight = 0.75
match_deminish = 4

def score_calc(user1, user2, winner):
    user1_score = read_data(user1, "scale") 
    user1_weight: int = read_data(user1, "matches")
    user2_score = read_data(user2, "scale")
    user2_weight: int = read_data(user2, "matches")
    # print(user2_score)
    # print(user2_weight)
    # print(user1_score)
    # print(user1_weight)

    if winner == user1:
        if user1_score == user2_score:
            user2_new = user2_score - 0.5
            user1_new = user1_score + 0.5
        else:
            score_diff = user1_score - user2_score
            user1_new = user1_score + ((score_diff * diffrence_weight) / (1 + (user1_weight + 1) / match_deminish))
            user2_new = user2_score - ((score_diff * diffrence_weight) / (1 + (user2_weight + 1) / match_deminish))
    elif winner == user2:
        if user1_score == user2_score:
            user2_new = user2_score + 0.5
            user1_new = user1_score - 0.5
        else:
            score_diff = user2_score - user1_score
            user2_new = user2_score + ((score_diff * diffrence_weight) / (1 + (user2_weight + 1) / match_deminish))
            user1_new = user1_score - ((score_diff * diffrence_weight) / (1 + (user1_weight + 1) / match_deminish))
    else:
        user2_new = user2_score
        user1_new = user1_score
        print("draw")
    
    if user1_new > 20:
        user1_new = 20
    if user2_new > 20:
        user2_new = 20
    if user1_new < 1:
        user1_new = 1
    if user2_new < 1:
        user2_new = 1
    edit_account(user1, "scale", user1_new)
    edit_account(user2, "scale", user2_new)
    edit_account(user1, "matches", int(user1_weight + 1))
    edit_account(user2, "matches", int(user2_weight + 1))
    print("--------------------------")
    read_data(user1, "scale") 
    read_data(user1, "matches")
    read_data(user2, "scale")
    read_data(user2, "matches")
    print("--------------------------")

# score_calc("test1","test2","test1")

