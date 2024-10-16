from tartigrade.hello_tartigrade import what_is_a_tartigrade


def test_what_is_a_tartigrade_is_string() -> None:
    assert isinstance(what_is_a_tartigrade(), str)
