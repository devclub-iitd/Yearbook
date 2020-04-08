import django
django.setup()

from myapp.models import *
from collections import defaultdict
import copy
# import logging

# logger = logging.getLogger(__name__)

depts = [
    "chemical",
    "civil",
    "cse",
    "ee",
    "maths",
    "mech",
    "physics",
    "textile",
    "dbeb",
]

for dept in depts:
    polls_dict = defaultdict(list)
    for p in Poll.objects.filter(department=dept):
        polls_dict[str(p.poll)].append(int(p.id))

    for p in polls_dict:
        polls_dict[p].sort()
    
    users = Student.objects.filter(department=dept)
    for u in users:
        votes_given = {}
        # logger.info('%s ------------ %s',u.name, u.VotesIHaveGiven,)
        for vote_id,enum in u.VotesIHaveGiven.items():
            if(len(enum.strip())>0 and enum.strip().lower()[:4]=='2016'):
                if(int(vote_id) > 180):
                    poll_text = Poll.objects.filter(id=int(vote_id))[0].poll
                    replace_vote_id = str(polls_dict[poll_text][0])
                    if replace_vote_id not in votes_given:
                        votes_given[replace_vote_id] = enum.strip()
                        replace_poll = Poll.objects.filter(id=int(replace_vote_id))[0]
                        if enum.strip() not in replace_poll.votes:
                            replace_poll.votes[enum.strip()] = 0
                        replace_poll.votes[enum.strip()] += 1
                        replace_poll.save()
                else:
                    votes_given[vote_id] = enum.strip()
        u.VotesIHaveGiven = votes_given
        # logger.info(u.VotesIHaveGiven)
        u.save()


for pid in range(540,179,-1):
    Poll.objects.filter(id=pid).delete()
