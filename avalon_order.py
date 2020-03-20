#!/usr/bin/env python

from libavalon import getPlayers
import random

if __name__ == "__main__":
    players, _ = getPlayers("players.txt")
    random.shuffle(players)
    print("lady: %s" % players[0])
    print(players)
