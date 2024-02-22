from pytest_httpx import HTTPXMock
from st2dl.auth import get_access_token


def test_get_access_token(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        json={
            "access_token": "eyJhbGciOiJSUzI1NiI",
            "expires_in": 600,
            "refresh_expires_in": 3600,
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgO",
            "token_type": "Bearer",
            "not-before-policy": 0,
            "session_state": "644926fd-33df-49c5-92c5-de29a9bfca33",
            "scope": "AUDIENCE_PUBLIC openid email profile user-context",
        }
    )
    tokens = get_access_token("user", "pass")
    assert tokens.access_token == "eyJhbGciOiJSUzI1NiI"
