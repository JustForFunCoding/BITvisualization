import sys
import time
import tb as traceback

test_utils_tests = [
        ("BIT 1D", [
          ("test_pu_rq_1d.py", "BIT PU RQ 1D", "1"),
          ("test_ru_pq_1d.py", "BIT RU PQ 1D", "1"),
          ("test_ru_rq_1d.py", "BIT RU RQ 1D", "2"),
        ]),
        ("BIT 2D", [
          ("test_pu_rq_2d.py", "BIT PU RQ 2D", "1"),
          ("test_ru_pq_2d.py", "BIT RU PQ 2D", "1"),
          ("test_ru_rq_2d.py", "BIT RU RQ 2D", "4"),
        ])
    ]
    
def discover_brython_test_modules():
    # TODO : Test discovery based on file system paths
    return test_utils_tests
    
def test_groups():
    ret = []
    for tg in test_utils_tests:
        ret.append(tg[0])

def populate_testmod_input(elem, selected=None):
    """Build a multiple selection control including test modules
    """
    from browser import html
    groups = discover_brython_test_modules()
    for label, options in groups:
        if selected and label not in selected:
            continue
        g = html.OPTGROUP(label=label)
        elem <= g
        for filenm, caption, canvas in options:
            if filenm == selected:
                o = html.OPTION(caption, value=(filenm,canvas), selected='')
            else:
                o = html.OPTION(caption, value=(filenm, canvas))
            g <= o

def run(src, file_path=None):
    t0 = time.perf_counter()
    msg = ''
    try:
        ns = {'__name__':'__main__'}
        if file_path is not None:
            ns['__file__'] = file_path
        exec(src, ns)
        state = 1
    except Exception as exc:
        msg = traceback.format_exc()
        print(msg, file=sys.stderr)
        state = 0
    t1 = time.perf_counter()
    return state, t0, t1, msg

def run_test_module(filename, base_path=''):
    if base_path and not base_path.endswith('/'):
        base_path += '/'
    file_path = base_path + filename
    src = open(file_path).read()
    return run(src, file_path)

