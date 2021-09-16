from lol_runes import get_champion_name, get_line


class MockMessage:
    content = None


def test_champion_name_space():
    msg = MockMessage()
    msg.content = "!runa aurelion sol mid"
    assert get_champion_name(msg) == "aurelion sol"


def test_get_valid_line():
    msg = MockMessage()
    msg.conten = "!runa maplphite top"
    assert get_line(msg) == "top"
