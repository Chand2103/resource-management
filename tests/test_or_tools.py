import pytest
from src.or_tools import check_availabiliy

def test_check_availability_no_conflicts():
    starts = ["09:00:00", "11:00:00"]
    ends = ["10:00:00", "12:00:00"]
    new_start = "10:30:00"
    new_end = "11:30:00"
    
    result = check_availabiliy(starts, ends, new_start, new_end)
    assert result is False  # Should be False because it overlaps with the second booking

def test_check_availability_with_conflicts():
    starts = ["09:00:00", "11:00:00"]
    ends = ["10:00:00", "12:00:00"]
    new_start = "08:00:00"
    new_end = "08:30:00"
    
    result = check_availabiliy(starts, ends, new_start, new_end)
    assert result is True  # Should be True because it doesn't overlap with any booking

def test_check_availability_empty_slots():
    starts = []
    ends = []
    new_start = "09:00:00"
    new_end = "10:00:00"
    
    result = check_availabiliy(starts, ends, new_start, new_end)
    assert result is True  # Should be True because there are no existing bookings

def test_check_availability_edge_cases():
    starts = ["09:00:00"]
    ends = ["10:00:00"]
    new_start = "10:00:00"
    new_end = "11:00:00"
    
    result = check_availabiliy(starts, ends, new_start, new_end)
    assert result is True  # Should be True because it starts exactly when the previous booking ends 