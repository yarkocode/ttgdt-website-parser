import pytest

from ttgdtparser.helpers import is_time


class TestIsTimeHelper:
    @pytest.mark.parametrize('time_repr,expected', [
        ('08:00', True),
        ('08.00', False),
        ('8:00', True),
        ('8,00', False),
        ('08,00', False),
        ('14:00', True),
        ('12:54', True),
        ('1,2,3,4', False),
        ('1,10', False),
        ('1,10', False),
        ('1.2.3.4.5', False),
        ('1:2:3:4:5', False)
    ])
    def test_time_checking(self, time_repr: str, expected: bool):
        print(time_repr)
        assert is_time(time_repr) is expected, 'Time was not correctly parsed. May be not time?'
