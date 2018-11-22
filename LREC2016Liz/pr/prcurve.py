import optparse, pylab, sys

parser = optparse.OptionParser()
parser.add_option('--noninterpolated', default=False, action='store_true')
parser.add_option('--outf', default=None)
parser.add_option('--top_n', default=None, type='int')
parser.add_option('--randomize_ranks', default=False, action='store_true')
parser.add_option('--labels', default=None)
parser.add_option('--baseline', default=False, action='store_true')
parser.add_option('--title', default=None, type='str')
parser.add_option('--legx', default=None, type=float)
parser.add_option('--legy', default=None, type=float)
parser.add_option('--legend_fontsize', default=36, type='int')
parser.add_option('--label_fontsize', default=32, type='int')
(options, args) = parser.parse_args()

pylab.rcParams.update({'legend.fontsize':options.legend_fontsize})
pylab.rcParams.update({'xtick.labelsize':options.label_fontsize})
pylab.rcParams.update({'ytick.labelsize':options.label_fontsize})
pylab.rcParams.update({'axes.labelsize':options.legend_fontsize})

pylab.rcParams.update({'figure.figsize':(15,10)})

targets = set([x.strip() for x in open(args[0])])

ranked_itemss = [[y.split()[0] for y in open(x)] for x in args[1:]]
# line_styles = ['-', '--', '-.', ':', '.-'] * 2
# line_styles = ['-', '--', '-.', ':'] * 2
# line_styles = ['-', '--', '-.', ':', '-+', '--+', '-.+', ':+']
line_styles = ['-k']


assert len(line_styles) >= len(ranked_itemss)
line_styles = line_styles[:len(ranked_itemss)]

if options.labels:
    ranked_items_labels = options.labels.split(',')
    # ranked_items_labels = options.labels.replace('-', u'\u2212').split(',')
else:    
    #ranked_items_labels = ['.'.join(x.split('.')[-2:]) for x in args[1:]]
    ranked_items_labels = args[1:]

if options.randomize_ranks:
    import random
    for r in ranked_itemss:
        random.shuffle(r)


def do_it(ranked_items, label, line_style):
    pr_s = []
    correct_so_far = 0
    for i,r in enumerate(ranked_items):
        if r in targets:
            correct_so_far += 1
        pr_s.append((correct_so_far / float(i+1),
                     correct_so_far / float(len(targets))))

    pr_s_sorted_by_r = sorted(pr_s, key=lambda x : x[1], reverse=True)

    for x in pr_s_sorted_by_r:
        print x

    pr_s_interp = []
    prevp = 0
    for p,r in pr_s_sorted_by_r:
        max_p = max(prevp,p)
        pr_s_interp.append((max_p, r))
        prevp = max_p

    if options.noninterpolated:
        pylab.plot([x[1] for x in pr_s], [x[0] for x in pr_s], 
                   line_style, label=label)
    else:
        pylab.plot([x[1] for x in pr_s_interp], [x[0] for x in pr_s_interp],
                   line_style, label=label)


# print ranked_itemss[0]
# print targets

for (ris,l,s) in zip(ranked_itemss, ranked_items_labels,line_styles):
    do_it(ris, l, s)
    if options.top_n:
        print l, sum([1 for r in ris[:options.top_n] if r in targets])


if options.baseline:
    baseline = [(len(targets) / float(len(ranked_itemss[0])),x/100.) for x in range(100)]
    pylab.plot([x[1] for x in baseline], [x[0] for x in baseline], 'b.',
               label='Baseline')

if options.title:
    pylab.title(options.title)
pylab.ylabel('Precision')
pylab.xlabel('Recall')
# if options.legx and options.legy:
#     pylab.legend(loc=(options.legx,options.legy))
# else:    
#     pylab.legend(loc='best')


pylab.ylim([0,1])
pylab.xlim([0,1])

if options.outf:
    pylab.savefig(options.outf)
else:
    pylab.show()

