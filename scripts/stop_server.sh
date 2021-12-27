#!/bin/bash
isExistApp = `pgrep python3.8`
if [[ -n  $isExistApp ]]; then
    kill $isExistApp
fi