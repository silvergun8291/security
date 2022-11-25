#!/bin/bash
docker build -t simple_overflow .
docker run -d -p 4147:4147 simple_overflow
