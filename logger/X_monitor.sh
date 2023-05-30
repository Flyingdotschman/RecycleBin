#!/bin/bash

while true; do
	# Get CPU Load
	cpu_load = $(uptime | awk -F 'load average:'  '{(print $2}' | awk -F, '{print $1}' )

	# Get memory usage
	mem_usage = $(free -m | awk 'NR=2{printf "%.2f%%", $3*100/$2}')

	# Get CPU temperature



