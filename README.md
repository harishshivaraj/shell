# SHELL Interview Quest

## Introduction

### Option Pricing Engine using Black Scholes model

The project consists of a simple rest API to price options contracts using the Black Scholes model. The pricing model
was built with certain assumption. Including constant market data, rates and volatility.

- Works only for European options
- With no dividend pay off
- With no markups charges included
- With each contract of 100 units
- With a constant interest rate
- With a constant volatility

The system was developed using python version 3.10 and tested on Kubuntu 22.10

### Requirements

- Docker 
- Make

### Running the script

`cd shell`

`make run`

```
curl --location 'http://localhost:8008/price' --header 'Content-Type: application/json'
      --data '{
        "commodity": "HH",
        "putcall": "PUT",
        "strike": 2.5,
        "delivery": "FEB-24",
        "type": "VANILLA"
      }'
```

### Running the tests

`cd shell`

`make run-dev`

Now from the container shell

`make test`