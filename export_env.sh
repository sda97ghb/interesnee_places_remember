#!/usr/bin/env bash
while read p; do export $p; done < .env
