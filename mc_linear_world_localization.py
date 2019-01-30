
n = 5
# uniform distribution
p = [ 1 /n] * n

world = ['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'green']
motions = [1, 1]
pHit = 0.6
pMiss = 0.2

pUndershoot = .1
pOvershoot = .1
pExact = .8
Phits = dict([('green' ,pMiss) ,('red' ,pHit)])

def sense(p, Z):
    q=[p[i] * pHit if Z == world[i] else p[i] * pMiss for i in range(len(p))]
    sumq = sum(q)
    return [qq/sumq for qq in q]


def move(p, U):
    q = [0] * len(p)
    for i in range(len(p)):
        q[(i + U - 1) % len(q)] += p[i] * pUndershoot
        q[(i + U) % len(q)] += p[i] * pExact
        q[(i + U + 1) % len(q)] += p[i] * pOvershoot
    return q


for meas,mot in zip(measurements,motions):
    p = sense(p,meas)
    p = move(p,mot)
print(p)



#Before motion, the robot believes it's in cell 1 with probability 1/9, cell 2 with probability 1/3, and so on.
# How would those probabilities change if the robot moved one cell to the right?