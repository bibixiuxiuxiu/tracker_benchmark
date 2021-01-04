from scripts import *
from config import *
from util import compare_name, calcu_speed, load_seq_result


loadSeqs = 'tb100'
evalType = 'OPE'
tracker = 'lgagf'
# replace your own path
txt_Results = r'E:\ImageCaptionCode\tracker_benchmark\tb100'

if SETUP_SEQ:
    print 'Setup sequences ...'
    """
    Doing in setup_seqs:
    1. check integrity of data, if not, download all
    2. write cfg.json and attrs.txt in each seq directory
    """
    butil.setup_seqs(loadSeqs)

# 'otb50', 'otb100' transform to corresponding seqs name list
seqNames = butil.get_seq_names(loadSeqs)
# load from saved cfg.json and return list contain Class Sequence instances
seqs = butil.load_seq_configs(seqNames)

resNames = os.listdir(txt_Results)
resNames.remove('times')
resNames = [res_name[:-4] for res_name in resNames]
print "=========================================================="

isSameName = compare_name(resNames, seqNames)

if isSameName:
    for s in seqs:

        seqResults = []
        res_type = 'rect'
        fps = round(calcu_speed(txt_Results, s.name), 3)
        boxes = load_seq_result(txt_Results, s.name)
        res = boxes.tolist()
        # for OPE
        r = Result(tracker, s.name, s.startFrame, s.endFrame,
                   res_type, evalType, res, fps, None)
        seqResults.append(r)
        print "Now write to results/{0}/{1}/{2}.json".format(evalType, tracker, s.name)
        if SAVE_RESULT:
            # 'results/evalType/Tracker/seqName.json'
            butil.save_seq_result(seqResults)

    print "Have written all seqs!"