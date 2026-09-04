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


def test_scene_cut_resets_object_track_ids():
    from app.services import objects
    from app.services.capture import _reset_trackers

    objects._next_id["cam-x"] = 9
    objects._tracks["cam-x"] = [{"id": "cam-x-8", "bbox": [0, 0, 10, 10], "cls": "person"}]
    _reset_trackers("cam-x")
    assert "cam-x" not in objects._tracks
    assert "cam-x" not in objects._next_id


def test_gap_is_scene_cut():
    hits = []
    seq = [0, 40, 8000]
    prev = None
    for pts in seq:
        if detect_scene_cut(prev, pts):
            hits.append(pts)
        prev = pts
    assert hits == [8000]
