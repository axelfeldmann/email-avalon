def getPlayers(playerFilename):
    playerFile = open(playerFilename, "r")
    players, emails = [], []
    for line in playerFile.readlines():
        if line[0] == "#":
            continue
        player, email = line.split(",")
        players.append(player)
        emails.append(email.strip())
    return players, emails
