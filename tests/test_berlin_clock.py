import hypothesis.strategies as st
import pytest
from hypothesis import assume, given

import berlin_clock.berlin_clock as bc

colors = st.sampled_from([bc.Color.YELLOW, bc.Color.RED])
lights = st.builds(bc.Light, colors, st.booleans())


@given(st.lists(elements=lights, max_size=11), st.integers(min_value=0, max_value=11))
def test_set_row(light_row, num_lights):
    assume(num_lights <= len(light_row))
    bc.set_light_row(light_row, num_lights)
    assert bc.num_lights_on(light_row) == num_lights


def test_set_row_too_many():
    with pytest.raises(ValueError):
        bc.set_light_row([bc.Light()], 3)


def test_set_negative():
    with pytest.raises(ValueError):
        bc.set_light_row([bc.Light()], -1)


@given(st.datetimes())
def test_check_berlin_clock_set_time(time):
    clock = bc.BerlinClock()
    clock.set_time(time)
    assert clock.top_light.on == (time.second % 2 == 0)
    assert bc.num_lights_on(clock.first_row) == time.hour // 5
    assert bc.num_lights_on(clock.second_row) == time.hour % 5
    assert bc.num_lights_on(clock.third_row) == time.minute // 5
    assert bc.num_lights_on(clock.last_row) == time.minute % 5

    assert len(clock.first_row) == 4
    assert len(clock.second_row) == 4
    assert len(clock.third_row) == 11
    assert len(clock.last_row) == 4
