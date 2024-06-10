from mcstatus import BedrockServer

# look for locally running server instance
server = BedrockServer.lookup("localhost")
didPlayersJoin = False

def IsServerEmpty():
    status = server.status()
    
    return status.players.online == 0

def IsServerAbandonded():
    isEmpty = IsServerEmpty()

    # players joined possibly for the first time
    if not isEmpty:
        global didPlayersJoin
        didPlayersJoin = True

    return isEmpty and didPlayersJoin