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
        ({"commodity": "BRN", "putcall": "CALL", "strike": 90, "delivery": "FEB-24", "type": "VANILLA"}, 1702.95664),
        ({"commodity": "BRN", "putcall": "PUT", "strike": 80, "delivery": "FEB-24", "type": "VANILLA"}, 928.8332),
        ({"commodity": "HH", "putcall": "PUT", "strike": 1.5, "delivery": "FEB-24", "type": "VANILLA"}, 3.57784),
        ({"commodity": "HH", "putcall": "CALL", "strike": 3.0, "delivery": "FEB-24", "type": "VANILLA"}, 40.233),
    ]
)
def test_rfq_request(client: FlaskClient, rfq: dict, pv: float) -> None:
    quote, return_code = get_quote(client, rfq)
    assert return_code == 200
    assert quote['Results']['PV'] == pv


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


def test_call_price_boundary(client: FlaskClient) -> None:
    """ 90 call cannot be more expensive than 86 call """
    def rfq(strike: float) -> dict:
        return {"commodity": "BRN", "putcall": "CALL", "strike": strike, "delivery": "FEB-24", "type": "VANILLA"}

    quote1, _ = get_quote(client, rfq(strike=80))
    quote2, _ = get_quote(client, rfq(strike=90))

    assert quote2['Results']['PV'] < quote1['Results']['PV']
