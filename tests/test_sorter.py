from photo_tool.sorter import sort_photos


def test_sorter():
    items = [3,1,2]
    assert sort_photos(items) == [1,2,3]
