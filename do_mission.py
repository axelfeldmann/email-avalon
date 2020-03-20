#!/usr/bin/env python


import email
import imaplib
import argparse
import uuid
import time

from libavalon import getPlayers
from libemail import Message, sendEmails, getEmails

parser = argparse.ArgumentParser()
parser.add_argument("players", type=str, nargs="+")

def main(args):
    players, emails = getPlayers("players.txt")
    emailDict = { player : email for (player, email) in zip(players, emails) }
    
    for player in args.players:
        assert(player in emailDict)
    
    missionId = uuid.uuid4().hex
    msgs = []
    for player in args.players:
        email = emailDict[player]
        msgs.append(Message("Mission %s" % missionId,
                            email,
                            "please reply PASS or FAIL"))
    sendEmails(msgs)

    while True:
        received = getEmails()
        votes = [msg for msg in received if missionId in msg.subject]
        if(len(votes) == len(args.players)):
            break
        time.sleep(5)

    #check for stefan sending in nonsense
    senders = set([x.sender for x in votes])
    assert(len(senders) == len(votes))

    passes = [x for x in votes if x.text.upper().startswith("PASS")]
    fails = [x for x in votes if x.text.upper().startswith("FAIL")]

    assert(len(passes) + len(fails) == len(votes))

    resultStr = "mission participants: %s\n" % (", ".join(args.players))
    resultStr += "there were %d passes and %d fails" % (len(passes), len(fails))
    print(resultStr)

    msgs = []
    for email, player in zip(emails, players):
        msgs.append(Message("Mission Outcome %s" % missionId,
                            email, resultStr))
    sendEmails(msgs)
                            

    
        



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
