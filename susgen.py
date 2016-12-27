## author: ecooper

## Generate semantically-unpredictable sentences (SUS)
## for intelligibility tests of the standard form:
## det adj noun verb det adj noun.
## as in the NIT Blizzard Challenge evaluation sentences:
## http://research.nii.ac.jp/src/en/NITECH-EN.html

## Dependencies: NLTK including the Brown corpus.
## Usage: python susgen.py n
## where n = the number of sentences you want to generate.

import nltk
from random import choice
import sys

def get_sus():
# Setup: collect the relevant parts of speech
    JJs = []
    NNs = []
    NNSs = []
    VBDs = []
    VBZs = []
    VBs = []
    for w in nltk.corpus.brown.tagged_words():
        if w[1] == 'JJ':
            JJs.append(w[0])
        if w[1] == 'NN':
            NNs.append(w[0])
        if w[1] == 'NNS':
            NNSs.append(w[0])
        if w[1] == 'VBD':
            VBDs.append(w[0])
        if w[1] == 'VBZ':
            VBZs.append(w[0])
        if w[1] == 'VB':
            VBs.append(w[0])

    # Round 1: randomly decide which parts of speech and articles we want.
    # 1) roll the dice for first a/the (weighted towards 'the')
    the_sub = choice([True, True, False])

    # 2) roll the dice for singular or plural subject
    # except if our article is not 'the,' then disallow plural.
    if not the_sub:
        sing_sub = True
    else:
        sing_sub = choice([True, False])

    # 3) roll the dice for present or past tense
    present = choice([True, False])

    # 4) roll the dice for second a/the
    the_obj = choice([True, True, False])

    # 5) roll the dice for singular or plural object
    # again disallowing plural if the article is 'the'
    if not the_obj:
        sing_obj = True
    else:
        sing_obj = choice([True, False])
        
    # Round 2: randomly pick words, constrained by our previously chosen POSes.
    # 1) roll the dice for first adjective
    adj_sub = choice(JJs)

    # 2) if first article is 'a', choose 'a' or 'an' as appropriate
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    if not the_sub:
        if adj_sub[0] in vowels:
            article_sub = 'an'
        else:
            article_sub = 'a'
    else:
        article_sub = 'the'

    # 3) roll the dice for first noun, constrained by sing/plural
    if sing_sub:
        sub = choice(NNs)
    else:
        sub = choice(NNSs)

    # 4) roll the dice for verb, past or present
    if present:
        if sing_sub:
            verb = choice(VBZs)
        else:
            verb = choice(VBs)
    else:
        verb = choice(VBDs)
    
    # 5) roll the dice for second adjective
    adj_obj = choice(JJs)

    # 6) 'a' or 'an' as appropriate
    if not the_obj:
        if adj_obj[0] in vowels:
            article_obj = 'an'
        else:
            article_obj = 'a'
    else:
        article_obj = 'the'

    # 7) roll the dice for the last noun, sing or plur as chosen earlier
    if sing_obj:
        obj = choice(NNs)
    else:
        obj = choice(NNSs)

    # put together the sentence
    sus = article_sub + ' ' + adj_sub + ' ' + sub + ' ' + verb + ' '
    sus += article_obj + ' ' + adj_obj + ' ' + obj + '.'
    return sus

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python susgen.py n"
        exit()
    n = int(sys.argv[1])
    for i in range(0,n):
        print get_sus()
