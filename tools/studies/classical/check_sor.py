import lyparse as L
from fractions import Fraction as Fr
M = '/home/claude/mutopiaproject/mutopiaproject/ftp/'
T = {'I': 'SorF/O6/sorf-op6n08/sorf-op6n08.ly', 'II': 'SorF/O35/sorf_op35_no13/sorf_op35_no13.ly', 'III': 'SorF/O6/sorf-op6n02/sorf-op6n02.ly',
     'IV': 'SorF/O6/sorf-op6n01/sorf-op6n01.ly', 'V': 'SorF/O35/sorf_op35_no22/sorf_op35_no22.ly', 'VI': 'SorF/O35/sorf_op35_no17/sorf_op35_no17.ly',
     'XI': 'SorF/O6/sorf-op6n03/sorf-op6n03.ly', 'XII': 'SorF/O6/sorf-op6n06/sorf-op6n06.ly', 'XIII': 'SorF/O6/sorf-op6n09/sorf-op6n09.ly',
     'XIV': 'SorF/O6/sorf-op6n12/sorf-op6n12.ly', 'XV': 'SorF/O35/sorf_op35_no16/sorf_op35_no16.ly', 'XVII': 'SorF/O6/sorf-op6n11/sorf-op6n11.ly',
     'XIX': 'SorF/O29/o29-13/o29-13.ly'}
if __name__ == '__main__':
    import sys
    for k, f in T.items():
        try:
            P = L.parse(M + f); n, d = P['time']; bl = Fr(n, d)
            vl = {kk: round(float(max(t + du for t, du, m, ti in ev) / bl), 2) for kk, ev in P['voices'].items() if ev and ':' not in kk}
            ms = [m for t, du, m, v in P['notes']]
            print(f'{k:5s} {f.split("/")[-1]:24s} {P["time"]} partial {P["partial"]} voices {vl} played {float((P["length"] - P["partial"]) / bl):.2f} bad {len(P["bad"])} range {min(ms)}-{max(ms)} graces {len(P["graces"])}')
            for b in P['bad'][:int(sys.argv[1]) if len(sys.argv) > 1 else 0]: print('     ', b)
        except Exception as e:
            import traceback; print(k, 'ERR', e)
