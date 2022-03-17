from libnum import invmod, n2s
from gmpy2 import next_prime

p = 74318463376311964657848870236469351222861371046000989980725143814597652972079
g = 10135979321704650132001133858909900216529170765388975908180263641843583056994
N = 46560744052031492000075598084262814175984839629218579003339825251165084535288738001196294968344403225296587992393409186512832442084313772062189640462381680977493272839744503195012137744652370256066011590369737294828406013950810998314546935103160880000499234316605414326064476117367727072344004644766745175963
c = 29564821569830699556212453454017718111058831300186556031247189290688822358690794181849755724708332331076603480330197679576704296745927605411596199406151384464410673003828317449576528702268825429862415693161675568796639942990788691799887406882528537855409648064568566289462225279575505434737651736766525709858
e = 0x10001

def chaos_maker(p, g, x):
    res = 0
    global rsf
    for i in range(256):
        x = rsf[x]
        if x < (p-1) // 2:
            res -= (1 << i) - 1
        elif x > (p-1) // 2:
            res += (1 << i) + 1
        else:
            res ^= (1 << i + 1)
        x = x % 28361
    return res if res > 0 else -res

rsf = [0] * 28361
rsf[0] = 1
for i in range(1, 28361):
    rsf[i] = (g * rsf[i-1]) % p
WOW = [0] * 28361
for i in range(0, 28361):
    WOW[i] = chaos_maker(p, g, i)
if 34921423738238217667426170081985242050986185851542392329360223748418245446709 in WOW:
    print(1)
WOW.sort()
ok = 0
for i in range(0, 28361):
    lef = i+1
    rig = 28360
    mid, best = 0, 0
    while lef <= rig:
        mid = (lef + rig) // 2
        if (WOW[i]*WOW[i] + WOW[mid] * WOW[mid]) * 2 * WOW[i] * WOW[mid] >= N:
            best = mid
            rig = mid -1
        else:
            lef = mid + 1
    if best == 0:
        continue
    for j in range(best-1, min(best+30, 28361)):
        u = WOW[i] * WOW[i] + WOW[j] * WOW[j]
        v = 2 * WOW[i] * WOW[j]
        if u * v <= N and N <= (u+1000) * (v+1000):
            u = next_prime(u)
            v = next_prime(v)
            if u * v == N:
                ok = True
                break
    if ok:
        break

# u = 13207168490744652956999406596846767472614127517045010655090178723910296606220559473477009696618646553552917605315941229263316963221556883007951846286507319
# v = 13206540315287197799978983146788490475082830408392129019383447128092673850363700139125558344894148410716241976023782262109119063597770109472702331423302981
print(u)
print(v)
phi = (u-1)*(v-1)
d = invmod(e, phi)
flag = pow(c,d,N)
print(n2s(int(flag)))