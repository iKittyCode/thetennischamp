currentscore = {
    "playergamescore": 0,
    "gamescore":0,
    "playersetscore": 0, 
    "opponentgamescore":0,
    "winner": None,
    "opponentsetscore":0,
    "istiebreak" : False

}
isplayerserving = True
point_over = False
def scoring(pointwin): 
    global isplayerserving
    if pointwin == "player":
        if currentscore["playergamescore"] == 0 or currentscore["playergamescore"] == 15:
            currentscore["playergamescore"] +=15
        elif currentscore["playergamescore"] == 30:
            currentscore["playergamescore"] += 10
        elif currentscore["playergamescore"] == 40 and currentscore["opponentgamescore"] != 40:
            currentscore["playergamescore"] = 0
            currentscore["opponentgamescore"] = 0
            isplayerserving = not isplayerserving

            
            if currentscore["playersetscore"] != 6:
                currentscore["playersetscore"] +=1
                if currentscore["playersetscore"] == 6 and currentscore["opponentsetscore"] < 5: 
                    currentscore["winner"] = "player"

        elif currentscore["playergamescore"] == 40 and currentscore["opponentgamescore"] == 40: 
            currentscore["playergamescore"] = 1 # AD scoring system
            currentscore["opponentgamescore"] = -1 
            
        elif currentscore["playergamescore"] == 1: 
            currentscore["playergamescore"] = 0
            currentscore["opponentgamescore"] = 0
            isplayerserving = not isplayerserving

            
            if currentscore["playersetscore"] != 6:
                currentscore["playersetscore"] +=1 
        elif currentscore["playergamescore"] == -1:
            currentscore["playergamescore"] = 40
            currentscore["opponentgamescore"] = 40
    else: 
        if currentscore["opponentgamescore"] == 0 or currentscore["opponentgamescore"] == 15:
            currentscore["opponentgamescore"] += 15
        elif currentscore["opponentgamescore"] == 30:
            currentscore["opponentgamescore"] += 10
        elif currentscore["opponentgamescore"] == 40 and currentscore["playergamescore"] != 40:
            currentscore["opponentgamescore"] = 0
            currentscore["playergamescore"] = 0
            isplayerserving = not isplayerserving

            
        
            if currentscore["opponentsetscore"] != 6:
                currentscore["opponentsetscore"] += 1
        elif currentscore["playergamescore"] == 40 and currentscore["opponentgamescore"] == 40: 
            currentscore["playergamescore"] = 1 # AD scoring system
            currentscore["opponentgamescore"] = -1 
            
        elif currentscore["opponentgamescore"] == 1: 
            currentscore["playergamescore"] = 0
            currentscore["opponentgamescore"] = 0
            isplayerserving = not isplayerserving

            



            

             
                
        elif currentscore["opponentgamescore"] == -1:
            currentscore["playergamescore"] = 40
            currentscore["opponentgamescore"] = 40

        
            
            
