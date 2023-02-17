# SHELL Interview Quest

## Introduction

### Option Pricing Engine using Black Scholes model

The project consists of a simple rest API to price options contracts using the Black Scholes model. The pricing model
was built with certain assumption. Including constant market data, rates and volatility.

The system was developed using python version 3.10 and tested on Kubuntu 22.10

### Requirements

1. Docker
2. Makefile

### Running the script

`cd shell`

`make run`

`curl --location 'http://localhost:8008/price' --header 'Content-Type: application/json'
      --data '{
        "commodity": "HH",
        "putcall": "PUT",
        "strike": 2.5,
        "delivery": "FEB-24",
        "type": "VANILLA"
      }'
`
