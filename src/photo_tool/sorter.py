"""Sorting logic for photos (by date, location, etc.)."""


def sort_photos(photos, key=None):
    return sorted(photos, key=key)
