import pytest

from app.core.host.credentials import Credentials


def test_credentials_with_enable():
    """
    GIVEN username, password, enable
    WHEN Credentials are initilized
    THEN the attributes tested are present
    """
    creds = Credentials(username="user", password="password", enable="enable")

    assert creds.username == "user"
    assert creds.password == "password"
    assert creds.enable == "enable"


def test_credentials_no_enable():
    """
    GIVEN username, password
    WHEN Credentials are initilized
    THEN the attributes tested are present
    """
    creds = Credentials(username="user", password="password")

    assert creds.username == "user"
    assert creds.password == "password"
    assert creds.enable == "password"


def test_credentials_no_user():
    """
    GIVEN password
    WHEN Credentials are initilized
    THEN TypeError is raised
    """
    with pytest.raises(TypeError):
        creds = Credentials(password="password")
