currentscore = {
    "playergamescore": 0,
    "gamescore":0,
    "playersetscore": 0, 
    "opponentgamescore":0,
    "winner": None

}
point_over = False
def scoring(pointwin): 
    if pointwin == "player":
        if currentscore["playergamescore"] == 0 or currentscore["playergamescore"] == 15:
            currentscore["playergamescore"] +=15
        elif currentscore["playergamescore"] == 30:
            currentscore["playergamescore"] += 10
        elif currentscore["playergamescore"] == 40 and currentscore["playergamescore"] != 40:
            currentscore["playergamescore"] = 0
            if currentscore["playersetscore"] != 6:
                currentscore["playersetscore"] +=1 
    else: 
        if currentscore["opponentgamescore"] == 0 or currentscore["opponentgamescore"] == 15:
            currentscore["opponentgamescore"] +=15
        elif currentscore["opponentgamescore"] == 30:
            currentscore["opponentgamescore"] += 10
        elif currentscore["opponentgamescore"] == 40 and currentscore["opponentgamescore"] != 40:
            currentscore["opponentgamescore"] = 0
            if currentscore["opponentsetscore"] != 6:
                currentscore["opponentsetscore"] += 1
