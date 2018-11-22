import sys, random

def split(a, n):
    k, m = len(a) / n, len(a) % n
    result = (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))
    return list(result)


def doit_exp(k, exp):
    # print k, exp
    (num_i,num_l) = exp
    items = [1] * num_i + [0] * num_l
    # print x
    random.shuffle(items)
    # print items
    clusters = split(items, k)
    # print clusters

    total = 0
    correct = 0
    for c in clusters:
        total = total + len(c)
        if c.count(0) > c.count(1):
            correct = correct + c.count(0)
        else:
            correct = correct + c.count(1)
    assert total == num_i + num_l
    assert correct <= total
    acc = correct / float(total)
    # print acc
    return acc


def doit(n, data):
    final_acc_cum = 0
    num_runs = 100
    for i in range(num_runs):
        acc_cum_i = 0
        for exp in data:
            acc_cum_i = acc_cum_i + doit_exp(n, exp)
        acc_i = acc_cum_i / float(len(data))
        # print len(data)
        # print n, acc_i
        final_acc_cum = final_acc_cum + acc_i
    final_acc = final_acc_cum / float(num_runs)
    print n, final_acc



random.seed(5)

fname = sys.argv[1]
data = [[int(y) for y in x.split()] for x in  open(fname).readlines()]
    
for k in range(1,6):
    doit(k, data)

