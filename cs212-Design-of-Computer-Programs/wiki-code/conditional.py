import itertools
import fractions

def conditional_prob():
    print(two_kids)
    # ['BB', 'BG', 'GB', 'GG']
    print(condP(two_boys, one_boy))
    # 1/3

def product(*variables):
    "The cartesian product (as a str) of the possibilities for each variable."
    return map(''.join, itertools.product(*variables))

def condP(predicate, event):
    """Conditional probability: P(predicate(s) | s in event).
    The proportion of states in event for which predicate is true."""
    pred = [s for s in event if predicate(s)]
    return fractions.Fraction(len(pred), len(event))

def tuesday():
    """Out of all families with two kids with at least one boy born on a
    Tuesday, what is the probability of two boys?
    """
    print(two_kids_bday)
    print(condP(two_boys, boy_tuesday))
    # 13/27

sex = 'BG'
two_kids = product(sex, sex)
one_boy = [s for s in two_kids if 'B' in s]
def two_boys(s): return s.count('B') == 2
day = 'SMTWtFs'
two_kids_bday = product(sex, day, sex, day)
boy_tuesday = [s for s in two_kids_bday if 'BT' in s]
boy_anyday = [s for s in two_kids_bday if 'B' in s]
month = 'JFMAmjLaSOND'
two_kids_bmonth = product(sex, month, sex, month)
boy_december = [s for s in two_kids_bmonth if 'BD' in s]

def report(verbose = False, predicate = two_boys, predname = '2 boys',
           cases = [('2 kids', two_kids), ('2 kids born any day', two_kids_bday),
                    ('at least 1 boy', one_boy),
                    ('at least 1 boy born any day', boy_anyday),
                    ('at least 1 boy born on Tuesday', boy_tuesday),
                    ('at least 1 boy born in December', boy_december)]):
    import textwrap
    for (name, event) in cases:
        print('P(%s | %s) = %s' % (predname, name, condP(predicate, event)))
        if verbose:
            print('Reason:\n"%s" has %d elements:\n%s' %(
                name, len(event), textwrap.fill(' '.join(event), 85)))
            good = [s for s in event if predicate(s)]
            print('of those, %d are %s:\n%s\n\n' % (
                len(good), predname, textwrap.fill(' '.join(good), 85)))

if __name__ == '__main__':
    conditional_prob()
    tuesday()
    report()
    '''
    P(2 boys | 2 kids) = 1/4
    P(2 boys | 2 kids born any day) = 1/4
    P(2 boys | at least 1 boy) = 1/3
    P(2 boys | at least 1 boy born any day) = 1/3
    P(2 boys | at least 1 boy born on Tuesday) = 13/27
    P(2 boys | at least 1 boy born in December) = 23/47
    '''

    report(verbose = True)
    '''
    P(2 boys | 2 kids) = 1/4
    Reason:
    "2 kids" has 4 elements:
    BB BG GB GG
    of those, 1 are 2 boys:
    BB


    P(2 boys | 2 kids born any day) = 1/4
    Reason:
    "2 kids born any day" has 196 elements:
    BSBS BSBM BSBT BSBW BSBt BSBF BSBs BSGS BSGM BSGT BSGW BSGt BSGF BSGs BMBS BMBM BMBT
    BMBW BMBt BMBF BMBs BMGS BMGM BMGT BMGW BMGt BMGF BMGs BTBS BTBM BTBT BTBW BTBt BTBF
    BTBs BTGS BTGM BTGT BTGW BTGt BTGF BTGs BWBS BWBM BWBT BWBW BWBt BWBF BWBs BWGS BWGM
    BWGT BWGW BWGt BWGF BWGs BtBS BtBM BtBT BtBW BtBt BtBF BtBs BtGS BtGM BtGT BtGW BtGt
    BtGF BtGs BFBS BFBM BFBT BFBW BFBt BFBF BFBs BFGS BFGM BFGT BFGW BFGt BFGF BFGs BsBS
    BsBM BsBT BsBW BsBt BsBF BsBs BsGS BsGM BsGT BsGW BsGt BsGF BsGs GSBS GSBM GSBT GSBW
    GSBt GSBF GSBs GSGS GSGM GSGT GSGW GSGt GSGF GSGs GMBS GMBM GMBT GMBW GMBt GMBF GMBs
    GMGS GMGM GMGT GMGW GMGt GMGF GMGs GTBS GTBM GTBT GTBW GTBt GTBF GTBs GTGS GTGM GTGT
    GTGW GTGt GTGF GTGs GWBS GWBM GWBT GWBW GWBt GWBF GWBs GWGS GWGM GWGT GWGW GWGt GWGF
    GWGs GtBS GtBM GtBT GtBW GtBt GtBF GtBs GtGS GtGM GtGT GtGW GtGt GtGF GtGs GFBS GFBM
    GFBT GFBW GFBt GFBF GFBs GFGS GFGM GFGT GFGW GFGt GFGF GFGs GsBS GsBM GsBT GsBW GsBt
    GsBF GsBs GsGS GsGM GsGT GsGW GsGt GsGF GsGs
    of those, 49 are 2 boys:
    BSBS BSBM BSBT BSBW BSBt BSBF BSBs BMBS BMBM BMBT BMBW BMBt BMBF BMBs BTBS BTBM BTBT
    BTBW BTBt BTBF BTBs BWBS BWBM BWBT BWBW BWBt BWBF BWBs BtBS BtBM BtBT BtBW BtBt BtBF
    BtBs BFBS BFBM BFBT BFBW BFBt BFBF BFBs BsBS BsBM BsBT BsBW BsBt BsBF BsBs


    P(2 boys | at least 1 boy) = 1/3
    Reason:
    "at least 1 boy" has 3 elements:
    BB BG GB
    of those, 1 are 2 boys:
    BB


    P(2 boys | at least 1 boy born any day) = 1/3
    Reason:
    "at least 1 boy born any day" has 147 elements:
    BSBS BSBM BSBT BSBW BSBt BSBF BSBs BSGS BSGM BSGT BSGW BSGt BSGF BSGs BMBS BMBM BMBT
    BMBW BMBt BMBF BMBs BMGS BMGM BMGT BMGW BMGt BMGF BMGs BTBS BTBM BTBT BTBW BTBt BTBF
    BTBs BTGS BTGM BTGT BTGW BTGt BTGF BTGs BWBS BWBM BWBT BWBW BWBt BWBF BWBs BWGS BWGM
    BWGT BWGW BWGt BWGF BWGs BtBS BtBM BtBT BtBW BtBt BtBF BtBs BtGS BtGM BtGT BtGW BtGt
    BtGF BtGs BFBS BFBM BFBT BFBW BFBt BFBF BFBs BFGS BFGM BFGT BFGW BFGt BFGF BFGs BsBS
    BsBM BsBT BsBW BsBt BsBF BsBs BsGS BsGM BsGT BsGW BsGt BsGF BsGs GSBS GSBM GSBT GSBW
    GSBt GSBF GSBs GMBS GMBM GMBT GMBW GMBt GMBF GMBs GTBS GTBM GTBT GTBW GTBt GTBF GTBs
    GWBS GWBM GWBT GWBW GWBt GWBF GWBs GtBS GtBM GtBT GtBW GtBt GtBF GtBs GFBS GFBM GFBT
    GFBW GFBt GFBF GFBs GsBS GsBM GsBT GsBW GsBt GsBF GsBs
    of those, 49 are 2 boys:
    BSBS BSBM BSBT BSBW BSBt BSBF BSBs BMBS BMBM BMBT BMBW BMBt BMBF BMBs BTBS BTBM BTBT
    BTBW BTBt BTBF BTBs BWBS BWBM BWBT BWBW BWBt BWBF BWBs BtBS BtBM BtBT BtBW BtBt BtBF
    BtBs BFBS BFBM BFBT BFBW BFBt BFBF BFBs BsBS BsBM BsBT BsBW BsBt BsBF BsBs


    P(2 boys | at least 1 boy born on Tuesday) = 13/27
    Reason:
    "at least 1 boy born on Tuesday" has 27 elements:
    BSBT BMBT BTBS BTBM BTBT BTBW BTBt BTBF BTBs BTGS BTGM BTGT BTGW BTGt BTGF BTGs BWBT
    BtBT BFBT BsBT GSBT GMBT GTBT GWBT GtBT GFBT GsBT
    of those, 13 are 2 boys:
    BSBT BMBT BTBS BTBM BTBT BTBW BTBt BTBF BTBs BWBT BtBT BFBT BsBT


    P(2 boys | at least 1 boy born in December) = 23/47
    Reason:
    "at least 1 boy born in December" has 47 elements:
    BJBD BFBD BMBD BABD BmBD BjBD BLBD BaBD BSBD BOBD BNBD BDBJ BDBF BDBM BDBA BDBm BDBj
    BDBL BDBa BDBS BDBO BDBN BDBD BDGJ BDGF BDGM BDGA BDGm BDGj BDGL BDGa BDGS BDGO BDGN
    BDGD GJBD GFBD GMBD GABD GmBD GjBD GLBD GaBD GSBD GOBD GNBD GDBD
    of those, 23 are 2 boys:
    BJBD BFBD BMBD BABD BmBD BjBD BLBD BaBD BSBD BOBD BNBD BDBJ BDBF BDBM BDBA BDBm BDBj
    BDBL BDBa BDBS BDBO BDBN BDBD
    '''

