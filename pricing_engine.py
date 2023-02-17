import logging
from copy import deepcopy
from http import HTTPStatus

from flask import Flask, request
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from instruments import INSTRUMENT_MAP, create_instrument
from pricing_exceptions import (
    PricingEngineException,
    PricingEngineRFQValidationFailure,
    PricingEngineInstrumentError
)

logger = logging.Logger(__name__)
server = Flask(__name__)

rfq_schema = {
    "type": "object",
    "properties": {
        "commodity": {"type": "string", "enum": ["BRN", "HH"]},
        "putcall": {"type": "string", "enum": ["CALL", "PUT"]},
        "strike": {"type": "number"},
        "delivery": {"type": "string"},
        "type": {"type": "string", "enum": list(INSTRUMENT_MAP.keys())},
    }
}


def validate_rfq(rfq: dict) -> None:
    """ Validate given RFQ against the schema """
    try:
        validate(rfq, schema=rfq_schema)
    except ValidationError as ex:
        logger.error("RFQ - %s - %s", rfq, ex)
        raise PricingEngineRFQValidationFailure(ex.message) from ex


@server.route("/price", methods=["POST"])
def price():
    """
    Entry point to option pricing server.
    Accepts a post request with json payload. Payload consisting of option contract
    requesting for quote.

    The contract must strictly follow the json structure bellow

    {
        "commodity": "HH",
        "putcall": "PUT",
        "strike": 2.5,
        "delivery": "FEB-24",
        "type": "VANILLA"
    }

    On a successful response the quote for the contract will be return within the results
    section in the json response. Shown bellow

    {
        "Results": {
            "PV": 32.30087
        },
        "commodity": "HH",
        "delivery": "FEB-24",
        "putcall": "PUT",
        "strike": 2.5,
        "type": "VANILLA"
    }
    """

    try:
        rfq = request.get_json(force=True)

        # Validate ingress RFQ
        validate_rfq(rfq)

        # Create the instrument
        instrument = create_instrument(rfq)

        quote = deepcopy(rfq)

        # Calculate the PV
        quote["Results"] = {"PV": instrument.price()}

        error_code = HTTPStatus.OK
        content = quote

    except PricingEngineRFQValidationFailure as ex:
        content = {"Error": str(ex)}
        error_code = HTTPStatus.BAD_REQUEST

    except PricingEngineInstrumentError as ex:
        logger.error("Instrument Error", exc_info=True)
        content = {"Error": str(ex)}
        error_code = HTTPStatus.BAD_REQUEST

    except PricingEngineException as ex:
        logger.error("Pricing Engine failed", exc_info=True)
        error_code = HTTPStatus.INTERNAL_SERVER_ERROR
        content = {"Error": f"Pricing Engine error! - {ex}"}

    return content, error_code


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
