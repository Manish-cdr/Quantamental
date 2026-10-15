#!/bin/bash

cd src || exit 1

if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
fi

cargo run -- --token "$db8er11r01qs1m4crf90db8er11r01qs1m4crf9g" --symbols "BINANCE:BTCUSDT"