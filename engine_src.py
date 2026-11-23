import os, json, random, urllib.request as ur
from time import time, sleep

VAL = (0, 100, 320, 330, 500, 900, 20000)
N_OF = (-33, -31, -18, -14, 14, 18, 31, 33)
K_OF = (-17, -16, -15, -1, 1, 15, 16, 17); B_OF = (-17, -15, 15, 17)
R_OF = (-16, -1, 1, 16)
OF = {2: N_OF, 3: B_OF, 4: R_OF, 5: K_OF, 6: K_OF}
CST = {6: (7, 5), 2: (0, 3), 118: (119, 117), 114: (112, 115)}
CRT = {7: 'K', 0: 'Q', 119: 'k', 112: 'q'}
MATE, INF, BUD = 30000, 10 ** 9, 340000
TS = float(os.environ.get('ENG_SECONDS') or '6.5')
D = time() + TS
NODES = 0

class ABORT(Exception): pass

random.seed(5150)
ZP = {p: [random.getrandbits(64) for _ in range(128)]
      for p in list(range(1, 7)) + list(range(9, 15))}
ZS = random.getrandbits(64)
ZC = {c: random.getrandbits(64) for c in 'KQkq'}
ZE = [random.getrandbits(64) for _ in range(8)]
BR = [0] * 128; KX = [4, 116]
NMAT = [3200, 3200]; STM = 0
CR = {'K': 1, 'Q': 1, 'k': 1, 'q': 1}
EP, HM, FM, KEY = -1, 0, 1, 0
HS = []; REP = {}; TT = {}
KIL = {}; HIS = {}; PS = {}
tb = lambda fn: tuple(fn(i >> 3, i & 7) for i in range(64))
cf = lambda r, f: min(f, 7 - f, r, 7 - r)
PST = {
 1: (tb(lambda r, f: 0 if r in (0, 7) else 60 if r == 1 else 10 + 3 * (7 - r) + 2 * min(f, 7 - f)),
     tb(lambda r, f: 0 if r in (0, 7) else 90 if r == 1 else 14 * (7 - r))),
 2: (tb(lambda r, f: -30 + 6 * cf(r, f)),) * 2,
 3: (tb(lambda r, f: -14 + 8 * cf(r, f)),) * 2,
 4: (tb(lambda r, f: -5 + 5 * cf(r, f) + (10 if r == 1 else 0)),) * 2,
 5: (tb(lambda r, f: -10 + 3 * cf(r, f)),) * 2,
 6: (tb(lambda r, f: -30 - 8 * cf(r, f)), tb(lambda r, f: 15 * cf(r, f) - 20))}
PP = (0, 8, 14, 26, 50, 84, 130, 0)
def kcr():
 global KEY
 for ch in CR:
  if CR[ch]: KEY ^= ZC[ch]

def fen(f):
 global STM, CR, EP, HM, FM
 a = f.split(); BR[:] = [0] * 128; r, c = 7, 0
 for ch in a[0]:
  if ch == '/': r -= 1; c = 0
  elif ch.isdigit(): c += int(ch)
  else:
   p = 'PNBRQK'.index(ch.upper()) + 1 | (8 if ch.islower() else 0)
   sq = r * 16 + c; BR[sq] = p
   if p == 6: KX[0] = sq
   elif p == 14: KX[1] = sq
   c += 1
 STM = 0 if a[1] == 'w' else 8
 CR = {ch: ch in a[2] for ch in 'KQkq'}
 EP = -1
 if len(a) > 3 and a[3] != '-': EP = (int(a[3][1]) - 1) * 16 + ord(a[3][0]) - 97
 HM, FM = int(a[4]), int(a[5])
 NMAT[:] = [0, 0]; KEY = 0
 for sq in range(128):
  if sq & 136 or not BR[sq]: continue
  p = BR[sq]; KEY ^= ZP[p][sq]
  if p & 7 > 1: NMAT[p >> 3] += VAL[p & 7]
 if STM: KEY ^= ZS
 kcr()
 if EP >= 0: KEY ^= ZE[EP & 7]
 HS[:] = []; REP.clear(); REP[KEY] = 1; PS.clear()
def make(m):
 global STM, CR, EP, HM, FM, KEY
 f, t, l, pr = m
 p, c = BR[f], BR[t]
 k0, e0, h0, c0 = KEY, EP, HM, dict(CR)
 KEY ^= ZP[p][f]
 if c:
  KEY ^= ZP[c][t]
  if c & 7 > 1: NMAT[c >> 3] -= VAL[c & 7]
 BR[f] = 0; BR[t] = pr if pr else p
 KEY ^= ZP[BR[t]][t]
 if p & 7 == 6: KX[p >> 3] = t
 if EP >= 0: KEY ^= ZE[EP & 7]
 EP = -1
 if p & 7 == 1:
  if l == 1: EP = (f + t) >> 1; KEY ^= ZE[EP & 7]
  elif l == 2:
   cs = t - 16 if STM == 0 else t + 16
   KEY ^= ZP[BR[cs]][cs]; BR[cs] = 0
  elif pr: NMAT[STM >> 3] += VAL[pr & 7]
 elif l == 3:
  rf, rt = CST[t]
  rk = BR[rf]
  BR[rf] = 0; BR[rt] = rk
  KEY ^= ZP[rk][rf] ^ ZP[rk][rt]
 kcr()
 if p & 7 == 6: CR['K' if p == 6 else 'k'] = CR['Q' if p == 6 else 'q'] = False
 for s in CRT:
  if f == s or t == s: CR[CRT[s]] = False
 kcr()
 HM = 0 if (c or p & 7 == 1) else HM + 1
 FM += STM == 8
 STM ^= 8; KEY ^= ZS
 REP[KEY] = REP.get(KEY, 0) + 1
 HS.append((m, c, c0, e0, k0, h0, KEY))
def unmake():
 global STM, CR, EP, HM, FM, KEY
 m, c, cr, ep, k, hm, kp = HS.pop()
 f, t, l, pr = m
 STM ^= 8
 if l == 2:
  BR[f] = 1 | STM; BR[t] = 0
  BR[t - 16 if STM == 0 else t + 16] = 9 if STM == 0 else 1
 else:
  BR[f] = (1 | STM) if pr else BR[t]; BR[t] = c
 if l == 3:
  rf, rt = CST[t]
  BR[rf] = BR[rt]; BR[rt] = 0
 if BR[f] & 7 == 6: KX[BR[f] >> 3] = f
 if pr: NMAT[STM >> 3] -= VAL[pr & 7]
 if c and c & 7 > 1: NMAT[c >> 3] += VAL[c & 7]
 CR, EP, HM, KEY = cr, ep, hm, k
 FM -= STM == 8
 REP[kp] -= 1

def atk(sq, s):
 for os_, v in ((N_OF, 2), (K_OF, 6), ((-15, -17) if s == 0 else (15, 17), 1)):
  for q in os_:
   if not (sq + q) & 136 and BR[sq + q] == v | s: return True
 for o in R_OF + B_OF:
  q = sq + o
  while not q & 136:
   x = BR[q]
   if x:
    if x & 8 == s and x & 7 in ((4, 5) if o in R_OF else (3, 5)): return True
    break
   q += o
 return False

inch = lambda: atk(KX[STM >> 3], STM ^ 8)
safe = lambda: not atk(KX[(STM ^ 8) >> 3], STM)
def gen():
 L = []; ap = L.append
 for r in range(8):
  for f in range(8):
   sq = r * 16 + f; p = BR[sq]
   if not p or p & 8 != STM: continue
   t = p & 7
   if t == 1:
    d = 16 if STM == 0 else -16
    for dd in (d, d - 1, d + 1):
     q = sq + dd
     if q & 136 or (BR[q] and dd == d): continue
     if dd != d and (not BR[q] or BR[q] & 8 == STM):
      if q == EP and not BR[q]: ap((sq, q, 2, 0))
      continue
     if q >> 4 in (0, 7):
      for pc in (5, 4, 3, 2): ap((sq, q, 0, pc | STM))
     else:
      ap((sq, q, 0, 0))
      if dd == d and r == (1 if STM == 0 else 6) and not BR[sq + 2 * d]:
       ap((sq, sq + 2 * d, 1, 0))
    continue
   for o in OF[t]:
    q = sq + o
    while not q & 136:
     if BR[q]:
      if BR[q] & 8 != STM: ap((sq, q, 0, 0))
      break
     ap((sq, q, 0, 0))
     if t == 2 or t == 6: break
     q += o
 for e1, e2, rs, rp, ms, en, R in ((5, 6, 7, 4, 5, 8, 'K'), (1, 3, 0, 4, 3, 8, 'Q'),
   (117, 118, 119, 12, 117, 0, 'k'), (113, 115, 112, 12, 115, 0, 'q')):
  if en == (STM ^ 8) and CR[R] and BR[rs] == rp \
    and not any(BR[x] for x in range(e1, e2 + 1)) \
    and not atk(KX[STM >> 3], en) and not atk(ms, en):
   ap((KX[STM >> 3], ms + 1 if R in 'Kk' else ms - 1, 3, 0))
 return L

def lgl():
 out = []
 for m in gen():
  make(m)
  if safe(): out.append(m)
  unmake()
 return out

uci = lambda m: 'abcdefgh'[m[0] & 7] + str((m[0] >> 4) + 1) + 'abcdefgh'[m[1] & 7] + str((m[1] >> 4) + 1) + ('pnbrqk'[(m[3] & 7) - 1] if m[3] else '')
def evalp():
 if KEY in PS: return PS[KEY]
 ph = min(24, (NMAT[0] + NMAT[1]) // 260)
 sc = 0
 for r in range(8):
  for f in range(8):
   sq = r * 16 + f; p = BR[sq]
   if not p: continue
   s, t = p >> 3, p & 7
   i = (7 - r) * 8 + f if s == 0 else r * 8 + f
   mg, eg = PST[t]
   v = VAL[t] + (mg[i] * ph + eg[i] * (24 - ph)) // 24
   if 2 <= t <= 5:
    n = 0
    for o in OF[t]:
     q = sq + o
     while not q & 136:
      n += 1
      if BR[q] or t == 2: break
      q += o
    v += 4 * n
   sc += v if s == 0 else -v
 PS[KEY] = sc
 return sc

cv = lambda m: (1000 - VAL[BR[m[0]] & 7]) if m[2] == 2 else (10 * VAL[BR[m[1]] & 7] - VAL[BR[m[0]] & 7] if BR[m[1]] else (VAL[m[3] & 7] if m[3] else 0))
def search(d, a, b, k):
 global NODES, STM, EP, KEY, HM
 NODES += 1
 if NODES > BUD or time() > D: raise ABORT()
 if HM >= 100 or REP.get(KEY, 0) >= 2: return -50
 inc = inch()
 n = 0; a0 = a; bw = None
 if d <= 0:
  if inc:
   L = lgl()
   if not L: return -MATE + k
   best = -INF
  else:
   best = st = evalp() * (1 - (STM >> 2))
   if st >= b: return st
   a = max(a, st)
   L = [m for m in gen() if BR[m[1]] or m[2] == 2 or m[3]]
  L.sort(key=cv, reverse=True)
 else:
  e = TT.get(KEY)
  ttm = e[2] if e else None
  if e and e[0] >= d and abs(e[3]) <= MATE - 1000 and (e[1] == 0 or
    (e[1] == 1 and e[3] >= b) or (e[1] == 2 and e[3] <= a)): return e[3]
  if not inc and d >= 3 and NMAT[STM >> 3] > 400:
   sep, skey, shm = EP, KEY, HM
   if EP >= 0: KEY ^= ZE[EP & 7]
   EP = -1
   STM ^= 8; KEY ^= ZS
   try: sc = -search(d - 3, -b, 1 - b, k + 1)
   finally:
    STM ^= 8
    EP, KEY, HM = sep, skey, shm
   if sc >= b: return sc
  L = gen()
  kill = KIL.get(k, ())
  L.sort(key=lambda m: (1 << 30) * (m == ttm) + (1 << 19) * (m in kill)
   + ((1 << 21) + VAL[m[3] & 7]) * (m[3] != 0) + (1 << 20) * (BR[m[1]] != 0)
   + cv(m) * (BR[m[1]] != 0 or m[2] == 2) + HIS.get((BR[m[0]], m[1]), 0), reverse=True)
  a0, best, bw, n = a, -INF, None, 0
 for m in L:
  c = BR[m[1]]
  make(m)
  if not safe():
   unmake(); continue
  n += d > 0
  if d <= 1 or n == 1: sc = -search(d - 1, -b, -a, k + 1)
  elif d > 0:
   red = 2 if d > 2 and n > 4 and not inc and not c \
    and m[2] != 2 and not m[3] else 0
   sc = -search(d - 1 - red, -a - 1, -a, k + 1)
   if sc > a and red: sc = -search(d - 1, -a - 1, -a, k + 1)
   if a < sc < b: sc = -search(d - 1, -b, -a, k + 1)
  else:
   sc = -search(d - 1, -b, -a, k + 1)
  unmake()
  if sc > best:
   best = sc; bw = m if d > 0 else bw
   if sc > a:
    a = sc
    if a >= b:
     if d > 0 and not c and not m[3]:
      ks = KIL.setdefault(k, [])
      ks[:] = [m] + [x for x in ks if x != m][:1]
      HIS[(BR[m[0]], m[1])] = HIS.get((BR[m[0]], m[1]), 0) + d * d
     break
 if d > 0 and not n: return -MATE + k if inc else -50
 if d > 0: TT[KEY] = (d, 1 if best >= b else 0 if best > a0 else 2, bw, best)
 return best
def root():
 global NODES
 NODES = 0
 b0 = len(HS)
 L = lgl()
 if not L: return None
 best = L[0]
 for d in range(1, 65):
  a, cu = -INF, None
  try:
   for m in L:
    make(m)
    try: sc = -search(d - 1, -INF, -a, 1)
    finally: unmake()
    if sc > a:
     a = sc; cu = m
  except ABORT:
   while len(HS) > b0: unmake()
   break
  best = cu or best
 return best
def post(url, obj):
 return json.loads(ur.urlopen(ur.Request(url, data=json.dumps(obj).encode(),
  headers={'Content-Type': 'application/json'}), timeout=45).read())
def play():
 url = os.environ.get('MAKEFUN_ENV_URL', '')
 if not url: return
 global D
 try:
  while True:
   g = post(url + '/game', {})
   if g.get('status') == 'done': return
   if g.get('status') == 'your_move':
    TT.clear(); KIL.clear(); HIS.clear(); PS.clear(); D = time() + TS
    if 'start_fen' in g:
     fen(g['start_fen'])
     todo = g.get('moves', [])
    else:
     todo = [g['last_move']] if g.get('last_move') else []
    for u in todo:
     m = next((x for x in lgl() if uci(x) == u), None)
     if m: make(m)
    m = root()
    if m: post(url + '/move', {'game': g['game'], 'move': uci(m)})
 except Exception:
  pass

fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
if __name__ == '__main__': play()
