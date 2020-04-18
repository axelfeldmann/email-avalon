#!/usr/bin/env python

import random
from collections import defaultdict as ddict
from libemail import Message, sendEmails
from libavalon import getPlayers
import copy


class Roles:

    def __init__(self, players):
        assert(len(players) > 1)
        self.players = players
        self.good, self.bad = self.parseRoles(players, "roles.txt")

    def parseRoles(self, players, roleFilename):
        numPlayers = len(players)
        roleFile = open(roleFilename, "r")
        lines = roleFile.readlines()
        game = lines[numPlayers]
        good, bad = game.split("|")
        good = [x.strip() for x in good.split(",")]
        bad = [x.strip() for x in bad.split(",")]
        roles = good + bad
        assert(len(roles) == len(players))
        random.shuffle(roles)
        self.playerDict = {}
        self.roleDict = ddict(list)
        for role, player in zip(roles, players):
            self.playerDict[player] = role
            self.roleDict[role].append(player)
        roleFile.close()
        return good, bad

    def getRole(self, player):
        return self.playerDict[player]

    def visibleRoles(self, role):
        if role == "merlin":
            return [x for x in self.bad if (x != "mordred")] + ["dean kamen"]
        if role == "morgana":
            return [x for x in self.bad if (x != "oberon" and x != "broberon")]
        if role == "mordred":
            return [x for x in self.bad if (x != "oberon" and x != "broberon")]
        if role == "guinevere":
            return ["good lancelot", "bad lancelot"]
        if role == "percival":
            return ["morgana", "merlin"]
        if role == "bad lancelot":
            return [x for x in self.bad if (x != "oberon" and x != "broberon")]
        if role == "bad townie":
            return [x for x in self.bad if (x != "oberon" and x != "broberon")]
        return []

    def visibleHands(self, player):
        role = self.playerDict[player]
        visibleRoles = self.visibleRoles(role)
        visibleHands = []
        for r in visibleRoles:
            visibleHands.extend(self.roleDict[r])
        
        if player in visibleHands:
            visibleHands.remove(player)
        if(len(visibleHands) == 0):
            return "no one"
        else:
            return ", ".join(visibleHands)

def sendRoles(players, emails):
    roles = Roles(players)

    _players = copy.copy(players)
    random.shuffle(_players)
    order = "lady: %s\n" % _players[0]
    order += ", ".join(_players)

    msgs = []
    for email, player in zip(emails, players):
        role = roles.getRole(player)
        visibleHands = roles.visibleHands(player)
        msgs.append(
                Message("Role Assignment", email, 
                    "your role is %s\nyou see %s\n\n%s" % (role, visibleHands, order))
                )
    sendEmails(msgs)



def main():
    players, emails = getPlayers("players.txt")
    sendRoles(players, emails)

if __name__ == "__main__":
    main()
