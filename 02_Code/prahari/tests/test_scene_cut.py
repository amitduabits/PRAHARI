from app.services.capture import detect_scene_cut


def test_loop_rewind_is_scene_cut():
    hits = []
    seq = [0, 40, 80, 40]
    prev = None
    for pts in seq:
        if detect_scene_cut(prev, pts):
            hits.append(pts)
        prev = pts
    assert hits == [40]


def test_gap_is_scene_cut():
    hits = []
    seq = [0, 40, 8000]
    prev = None
    for pts in seq:
        if detect_scene_cut(prev, pts):
            hits.append(pts)
        prev = pts
    assert hits == [8000]
