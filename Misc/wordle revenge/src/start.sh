#!/bin/bash
socat tcp-listen:65100,fork exec:/root/main.py,reuseaddr