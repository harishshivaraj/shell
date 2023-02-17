import json

import pytest

from pricing_engine import server


@pytest.fixture
def client() -> "FlaskClient":
    return server.test_client()


@pytest.mark.parametrize(
    "rfq, pv", [
        ({"commodity": "BRN", "putcall": "CALL", "strike": 90, "delivery": "FEB-24", "type": "VANILLA"}, 1702.95664),
        ({"commodity": "BRN", "putcall": "PUT", "strike": 80, "delivery": "FEB-24", "type": "VANILLA"}, 928.8332),
        ({"commodity": "HH", "putcall": "PUT", "strike": 1.5, "delivery": "FEB-24", "type": "VANILLA"}, 3.57784),
        ({"commodity": "HH", "putcall": "CALL", "strike": 3.0, "delivery": "FEB-24", "type": "VANILLA"}, 40.233),
    ]
)
def test_rfq_request(client, rfq, pv):
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype
    }
    response = client.post('/price', data=json.dumps(rfq), headers=headers)
    quote = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert quote['Results']['PV'] == pv


@pytest.mark.parametrize(
    "rfq, error_code", [
        ({"commodity": "B1", "putcall": "CALL", "strike": 200, "delivery": "FEB-24", "type": "VANILLA"}, 400),
        ({"commodity": "BRN", "putcall": "PUT1", "strike": 200, "delivery": "FEB-24", "type": "VANILLA"}, 400),
        ({"commodity": "HH", "putcall": "PUT", "strike": "edr", "delivery": "FEB-24", "type": "VANILLA"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": 200, "delivery": "FEB-24", "type": "VANILLA1"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": 200, "delivery": "MAR-22", "type": "VANILLA1"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": -200, "delivery": "MAR-22", "type": "VANILLA1"}, 400),
        ({"commodity": "HH", "putcall": "CALL", "strike": -200, "delivery": "MAR-22"}, 400),
    ]
)
def test_validation(client, rfq, error_code):
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype
    }
    response = client.post('/price', data=json.dumps(rfq), headers=headers)
    assert response.status_code == error_code
