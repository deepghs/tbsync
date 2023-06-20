import os.path


def get_testfile(seg, *segs):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'testfile', seg, *segs))
