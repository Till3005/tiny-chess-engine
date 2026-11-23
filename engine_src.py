import os, json, random, urllib.request as ur
from time import time

vls = (0, 100, 320, 330, 500, 900, 20000)
N_OF = (-33, -31, -18, -14, 14, 18, 31, 33)
K_OF = (-17, -16, -15, -1, 1, 15, 16, 17); B_OF = (-17, -15, 15, 17)
R_OF = (-16, -1, 1, 16)
OF = {2: N_OF, 3: B_OF, 4: R_OF, 5: K_OF, 6: K_OF}
CST = {6: (7, 5), 2: (0, 3), 118: (119, 117), 114: (112, 115)}
CRT = {7: 'K', 0: 'Q', 119: 'k', 112: 'q'}
MATE, INF, BUD = 30000, 10 ** 9, 200000
TS = float(os.environ.get('ENG_SECONDS') or '4.0')
DELTA = 200
D = time() + TS
NODES = 0

class ABORT(Exception): pass

random.seed(5150)
ZP = {p: [random.getrandbits(64) for _ in range(128)]
      for p in list(range(1, 7)) + list(range(9, 15))}
ZS = random.getrandbits(64)
ZC = {c: random.getrandbits(64) for c in 'KQkq'}
ZE = [random.getrandbits(64) for _ in range(8)]
bd = [0] * 128; KX = [4, 116]
NMAT = [3200, 3200]; sm = 0
CR = {'K': 1, 'Q': 1, 'k': 1, 'q': 1}
EP, HM, FM, pk = -1, 0, 1, 0
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
def key_castling():
 global pk
 for ch in CR:
  if CR[ch]: pk ^= ZC[ch]

def fen(f):
 global sm, CR, EP, HM, FM
 a = f.split(); bd[:] = [0] * 128; r, c = 7, 0
 for ch in a[0]:
  if ch == '/': r -= 1; c = 0
  elif ch.isdigit(): c += int(ch)
  else:
   p = 'PNBRQK'.index(ch.upper()) + 1 | (8 if ch.islower() else 0)
   sq = r * 16 + c; bd[sq] = p
   if p == 6: KX[0] = sq
   elif p == 14: KX[1] = sq
   c += 1
 sm = 0 if a[1] == 'w' else 8
 CR = {ch: ch in a[2] for ch in 'KQkq'}
 EP = -1
 if len(a) > 3 and a[3] != '-': EP = (int(a[3][1]) - 1) * 16 + ord(a[3][0]) - 97
 HM, FM = int(a[4]), int(a[5])
 NMAT[:] = [0, 0]; pk = 0
 for sq in range(128):
  if sq & 136 or not bd[sq]: continue
  p = bd[sq]; pk ^= ZP[p][sq]
  if p & 7 > 1: NMAT[p >> 3] += vls[p & 7]
 if sm: pk ^= ZS
 key_castling()
 if EP >= 0: pk ^= ZE[EP & 7]
 HS[:] = []; REP.clear(); REP[pk] = 1; PS.clear()
def make(m):
 global sm, CR, EP, HM, FM, pk
 f, t, l, pr = m
 p, c = bd[f], bd[t]
 k0, e0, h0, c0 = pk, EP, HM, dict(CR)
 pk ^= ZP[p][f]
 if c:
  pk ^= ZP[c][t]
  if c & 7 > 1: NMAT[c >> 3] -= vls[c & 7]
 bd[f] = 0; bd[t] = pr if pr else p
 pk ^= ZP[bd[t]][t]
 if p & 7 == 6: KX[p >> 3] = t
 if EP >= 0: pk ^= ZE[EP & 7]
 EP = -1
 if p & 7 == 1:
  if l == 1: EP = (f + t) >> 1; pk ^= ZE[EP & 7]
  elif l == 2:
   cs = t - 16 if sm == 0 else t + 16
   pk ^= ZP[bd[cs]][cs]; bd[cs] = 0
  elif pr: NMAT[sm >> 3] += vls[pr & 7]
 elif l == 3:
  rf, rt = CST[t]
  rk = bd[rf]
  bd[rf] = 0; bd[rt] = rk
  pk ^= ZP[rk][rf] ^ ZP[rk][rt]
 key_castling()
 if p & 7 == 6: CR['K' if p == 6 else 'k'] = CR['Q' if p == 6 else 'q'] = False
 for s in CRT:
  if f == s or t == s: CR[CRT[s]] = False
 key_castling()
 HM = 0 if (c or p & 7 == 1) else HM + 1
 FM += sm == 8
 sm ^= 8; pk ^= ZS
 REP[pk] = REP.get(pk, 0) + 1
 HS.append((m, c, c0, e0, k0, h0, pk))
def unmake():
 global sm, CR, EP, HM, FM, pk
 m, c, cr, ep, k, hm, kp = HS.pop()
 f, t, l, pr = m
 sm ^= 8
 if l == 2:
  bd[f] = 1 | sm; bd[t] = 0
  bd[t - 16 if sm == 0 else t + 16] = 9 if sm == 0 else 1
 else:
  bd[f] = (1 | sm) if pr else bd[t]; bd[t] = c
 if l == 3:
  rf, rt = CST[t]
  bd[rf] = bd[rt]; bd[rt] = 0
 if bd[f] & 7 == 6: KX[bd[f] >> 3] = f
 if pr: NMAT[sm >> 3] -= vls[pr & 7]
 if c and c & 7 > 1: NMAT[c >> 3] += vls[c & 7]
 CR, EP, HM, pk = cr, ep, hm, k
 FM -= sm == 8
 REP[kp] -= 1

def attacked_by(sq, s):
 for os_, v in ((N_OF, 2), (K_OF, 6), ((-15, -17) if s == 0 else (15, 17), 1)):
  for q in os_:
   if not (sq + q) & 136 and bd[sq + q] == v | s: return True
 for o in R_OF + B_OF:
  q = sq + o
  while not q & 136:
   x = bd[q]
   if x:
    if x & 8 == s and x & 7 in ((4, 5) if o in R_OF else (3, 5)): return True
    break
   q += o
 return False

in_check_now = lambda: attacked_by(KX[sm >> 3], sm ^ 8)
king_is_safe = lambda: not attacked_by(KX[(sm ^ 8) >> 3], sm)
def pm(sq, L):
 ap = L.append
 d = 16 if sm == 0 else -16
 for dd in (d, d - 1, d + 1):
  q = sq + dd
  if q & 136 or (bd[q] and dd == d): continue
  if dd != d and (not bd[q] or bd[q] & 8 == sm):
   if q == EP and not bd[q]: ap((sq, q, 2, 0))
   continue
  if q >> 4 in (0, 7):
   for pc in (5, 4, 3, 2): ap((sq, q, 0, pc | sm))
  else:
   ap((sq, q, 0, 0))
   if dd == d and sq >> 4 == (1 if sm == 0 else 6) and not bd[sq + 2 * d]:
    ap((sq, sq + 2 * d, 1, 0))

def sl(sq, L):
 pt = bd[sq] & 7
 for of in OF[pt]:
  q = sq + of
  while not q & 136:
   x = bd[q]
   if not x or x & 8 != sm: L.append((sq, q, 0, 0))
   if x or pt in (2, 6): break
   q += of

def cm(L):
 k = KX[sm > 0]
 for lo, hi, rf, rp, kd, en, r in ((5, 6, 7, 4, 5, 8, 'K'), (1, 3, 0, 4, 3, 8, 'Q'),
   (117, 118, 119, 12, 117, 0, 'k'), (113, 115, 112, 12, 115, 0, 'q')):
  if en == (sm ^ 8) and CR[r] and bd[rf] == rp \
    and not any(bd[x] for x in range(lo, hi + 1)) \
    and not attacked_by(k, en) and not attacked_by(kd, en):
   L.append((k, kd + 1 if r in 'Kk' else kd - 1, 3, 0))

def gen():
 L = []
 for sq in range(128):
  if sq & 136: continue
  p = bd[sq]
  if not p or p & 8 != sm: continue
  (pm if p & 7 == 1 else sl)(sq, L)
 cm(L)
 return L

def lgl():
 out = []
 for m in gen():
  make(m)
  if king_is_safe(): out.append(m)
  unmake()
 return out

uci = lambda m: 'abcdefgh'[m[0] & 7] + str((m[0] >> 4) + 1) + 'abcdefgh'[m[1] & 7] + str((m[1] >> 4) + 1) + ('pnbrqk'[(m[3] & 7) - 1] if m[3] else '')
def evaluate_side():
 if pk in PS: return PS[pk]
 ph = min(24, (NMAT[0] + NMAT[1]) // 260)
 sc = 0
 for r in range(8):
  for f in range(8):
   sq = r * 16 + f; p = bd[sq]
   if not p: continue
   s, t = p >> 3, p & 7
   i = (7 - r) * 8 + f if s == 0 else r * 8 + f
   mg, eg = PST[t]
   v = vls[t] + (mg[i] * ph + eg[i] * (24 - ph)) // 24
   if 2 <= t <= 5:
    n = 0
    for o in OF[t]:
     q = sq + o
     while not q & 136:
      n += 1
      if bd[q] or t == 2: break
      q += o
    v += 4 * n
   sc += v if s == 0 else -v
 PS[pk] = sc
 return sc

order_score = lambda m: (1000 - vls[bd[m[0]] & 7]) if m[2] == 2 else (10 * vls[bd[m[1]] & 7] - vls[bd[m[0]] & 7] if bd[m[1]] else (vls[m[3] & 7] if m[3] else 0))
def search(d, a, b, k):
 global NODES, sm, EP, pk, HM
 NODES += 1
 if NODES > BUD or time() > D: raise ABORT()
 if HM >= 100 or REP.get(pk, 0) >= 2: return -50
 chk = in_check_now()
 nn = 0; a00 = a; bm = None
 if d <= 0:
  if chk:
   ml = lgl()
   if not ml: return -MATE + k
   bs = -INF
  else:
   bs = sp = evaluate_side() * (1 - (sm >> 2))
   if sp >= b: return sp
   a = max(a, sp)
   ml = [m for m in gen() if (bd[m[1]] or m[2] == 2 or m[3]) and sp + (vls[bd[m[1]] & 7] if bd[m[1]] else 0) + 900 * (m[3] != 0) + DELTA >= a]
  ml.sort(key=order_score, reverse=True)
 else:
  te = TT.get(pk)
  tm = te[2] if te else None
  if te and te[0] >= d and abs(te[3]) <= MATE - 1000 and (te[1] == 0 or
    (te[1] == 1 and te[3] >= b) or (te[1] == 2 and te[3] <= a)): return te[3]
  if not chk and d >= 3 and NMAT[sm >> 3] > 400:
   se, sk, sh = EP, pk, HM
   if EP >= 0: pk ^= ZE[EP & 7]
   EP = -1
   sm ^= 8; pk ^= ZS
   try: s2 = -search(d - 3, -b, 1 - b, k + 1)
   finally:
    sm ^= 8
    EP, pk, HM = se, sk, sh
   if s2 >= b: return s2
  ml = gen()
  kl = KIL.get(k, ())
  ml.sort(key=lambda m: (1 << 30) * (m == tm) + (1 << 19) * (m in kl)
   + ((1 << 21) + vls[m[3] & 7]) * (m[3] != 0) + (1 << 20) * (bd[m[1]] != 0)
   + order_score(m) * (bd[m[1]] != 0 or m[2] == 2) + HIS.get((bd[m[0]], m[1]), 0), reverse=True)
  a00, bs, bm, nn = a, -INF, None, 0
 for m in ml:
  c = bd[m[1]]
  make(m)
  if not king_is_safe():
   unmake(); continue
  nn += d > 0
  if d <= 1 or nn == 1: s2 = -search(d - 1, -b, -a, k + 1)
  elif d > 0:
   rd = 2 if d > 2 and nn > 4 and not chk and not c \
    and m[2] != 2 and not m[3] else 0
   s2 = -search(d - 1 - rd, -a - 1, -a, k + 1)
   if s2 > a and rd: s2 = -search(d - 1, -a - 1, -a, k + 1)
   if a < s2 < b: s2 = -search(d - 1, -b, -a, k + 1)
  unmake()
  if s2 > bs:
   bs = s2; bm = m if d > 0 else bm
   if s2 > a:
    a = s2
    if a >= b:
     if d > 0 and not c and not m[3]:
      ks = KIL.setdefault(k, [])
      ks[:] = [m] + [x for x in ks if x != m][:1]
      h = (bd[m[0]], m[1]); HIS[h] = HIS.get(h, 0) + d * d
     break
 if d > 0 and not nn: return -MATE + k if chk else -50
 if d > 0: TT[pk] = (d, 1 if bs >= b else 0 if bs > a00 else 2, bm, bs)
 return bs
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
