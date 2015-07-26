# Copyright 2006 Bryan O'Sullivan <bos@serpentine.com>.
#
# This software may be used and distributed according to the terms
# of the GNU General Public License, version 2 or later, which is
# incorporated herein by reference.
#from slope_one import *

#s = SlopeOne()
#s.update(dict(alice=dict(squid=1.0, cuttlefish=4.0),bob=dict(squid=1.0, octupus=3.0)))
#s.predict(dict(squid=1.0, cuttlefish=4.0))

#from imp import reload
#reload(slope_one)


class SlopeOne(object):
    def __init__(self):
        self.diffs = {}
        self.freqs = {}

    def predict(self, userprefs):
        preds, freqs = {}, {}
        for item, rating in userprefs.items():
            for diffitem, diffratings in self.diffs.items():
                try:
                    freq = self.freqs[diffitem][item]
                except KeyError:
                    continue
                preds.setdefault(diffitem, 0.0)
                freqs.setdefault(diffitem, 0)
                preds[diffitem] += freq * (diffratings[item] + rating)
                freqs[diffitem] += freq
        return dict([(item, value / freqs[item])
                     for item, value in preds.items()
                     if item not in userprefs and freqs[item] > 0])

    def update(self, userdata):
        for ratings in userdata.values():
            for item1, rating1 in ratings.items():
                self.freqs.setdefault(item1, {})
                self.diffs.setdefault(item1, {})
                for item2, rating2 in ratings.items():
                    self.freqs[item1].setdefault(item2, 0)
                    self.diffs[item1].setdefault(item2, 0.0)
                    self.freqs[item1][item2] += 1
                    self.diffs[item1][item2] += rating1 - rating2
        for item1, ratings in self.diffs.items():
            for item2 in ratings:
                ratings[item2] /= self.freqs[item1][item2]

if __name__=='slope_one':
    print('slope one is running')