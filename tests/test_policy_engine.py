from policy_engine import get_risk_level

import pytest

from policy_engine import get_risk_level


@pytest.mark.parametrize(
    "license_name, expected",
    [
        ("MIT", "Low Risk"),
        ("Apache", "Low Risk"),
        ("LGPL", "Medium Risk"),
        ("GPL", "High Risk"),
        ("AGPL", "Very High Risk"),
    ]
)
def test_risk_levels(
    license_name,
    expected
):
    assert (
        get_risk_level(license_name)
        == expected
    )