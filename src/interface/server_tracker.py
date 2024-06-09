from mcstatus import MinecraftServer

# look for locally running server instance
server = MinecraftServer.lookup("localhost:25565")
didPlayersJoin = False

def IsServerEmpty():
    query = server.query()

    if query.players.online == 0:
        return True
    
    return False

def IsServerAbandonded():
    isEmpty = IsServerEmpty()

    # players joined possibly for the first time
    if not isEmpty:
        global didPlayersJoin
        didPlayersJoin = True

    if isEmpty and didPlayersJoin:
        return True
    
    return False