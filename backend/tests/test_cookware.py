"""Tests for the check_cookware tool."""

from tools.cookware import check_cookware


def test_check_cookware_user_has_all():
    # Subset of USER_COOKWARE
    result = check_cookware.invoke({"required_equipment": "Frying Pan, Knife, Spoon"})
    assert "all required equipment" in result
    assert "missing" not in result.lower()


def test_check_cookware_user_has_all_comma_separated():
    result = check_cookware.invoke({"required_equipment": "Spatula, Stovetop, Whisk"})
    assert "all required equipment" in result


def test_check_cookware_missing_items():
    result = check_cookware.invoke({"required_equipment": "Frying Pan, Oven, Knife"})
    assert "missing" in result.lower()
    assert "Oven" in result
    assert "Frying Pan" in result or "Knife" in result  # they have these


def test_check_cookware_all_missing():
    result = check_cookware.invoke({"required_equipment": "Oven, Blender"})
    assert "missing" in result.lower()
    assert "Oven" in result
    assert "Blender" in result
