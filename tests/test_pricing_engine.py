import json

import pytest

from pricing_engine import server

FlaskClient = "FlaskClient"


@pytest.fixture
def client() -> FlaskClient:
    return server.test_client()


def get_quote(client: FlaskClient, rfq: dict) -> tuple[dict, int]:
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype
    }
    response = client.post('/price', data=json.dumps(rfq), headers=headers)
    quote = json.loads(response.data.decode('utf-8'))
    return quote, response.status_code


@pytest.mark.parametrize(
    "rfq, pv", [
        ({"commodity": "BRN", "putcall": "CALL", "strike": 90, "delivery": "FEB-24", "type": "VANILLA"}, 1696),
        ({"commodity": "BRN", "putcall": "PUT", "strike": 80, "delivery": "FEB-24", "type": "VANILLA"}, 926),
        ({"commodity": "HH", "putcall": "PUT", "strike": 1.5, "delivery": "FEB-24", "type": "VANILLA"}, 3),
        ({"commodity": "HH", "putcall": "CALL", "strike": 3.0, "delivery": "FEB-24", "type": "VANILLA"}, 40),
    ]
)
def test_rfq_request(client: FlaskClient, rfq: dict, pv: float) -> None:
    quote, return_code = get_quote(client, rfq)
    assert return_code == 200
    assert pv-1 <= quote['Results']['PV'] <= pv+1


@pytest.mark.parametrize(
    "rfq, error_code", [
        ({"commodity": "B1", "putcall": "CALL", "strike": 200, "delivery": "FEB-24", "type": "VANILLA"}, 400),
        ({"commodity": "BRN", "putcall": "PUT1", "strike": 200, "delivery": "FEB-24", "type": "VANILLA"}, 400),
        ({"commodity": "HH", "putcall": "PUT", "strike": "edr", "delivery": "FEB-24", "type": "VANILLA"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": 200, "delivery": "FEB-24", "type": "VANILLA1"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": 200, "delivery": "MAR-22", "type": "VANILLA"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": -200, "delivery": "MAR-24", "type": "VANILLA"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": 200, "delivery": "MAR-24"}, 400),
    ]
)
def test_validation(client: FlaskClient, rfq: dict, error_code: int) -> None:
    quote, return_code = get_quote(client, rfq)
    assert return_code == error_code


@pytest.mark.parametrize(
    "rfq, expiry_date", [
        ({"commodity": "BRN", "putcall": "CALL", "strike": 200, "delivery": "FEB-24", "type": "VANILLA"}, "Dec-23"),
        ({"commodity": "BRN", "putcall": "PUT", "strike": 200, "delivery": "SEP-24", "type": "VANILLA"}, "Jul-24"),
    ]
)
def test_expiry_dates(client: FlaskClient, rfq: dict, expiry_date: str) -> None:
    quote, return_code = get_quote(client, rfq)
    assert return_code == 200
    assert quote['expiry'] == expiry_date


def test_call_price_boundary(client: FlaskClient) -> None:
    """ 90 call cannot be more expensive than 86 call """
    def rfq(strike: float) -> dict:
        return {"commodity": "BRN", "putcall": "CALL", "strike": strike, "delivery": "FEB-24", "type": "VANILLA"}

    quote1, _ = get_quote(client, rfq(strike=80))
    quote2, _ = get_quote(client, rfq(strike=90))

    assert quote2['Results']['PV'] < quote1['Results']['PV']
