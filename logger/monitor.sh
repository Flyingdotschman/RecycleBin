
#!/bin/bash


# Log file path
log_file="/home/rock/logger/monitor.log"
max_file_size=$((3 * 1024 * 1024 * 1024))  # 3GB in bytes

# Function to delete log file
delete_log_file() {
  rm "$log_file"
  echo "Deleted log file: $log_file"
}

# Start logging
while true; do
  # Check if log file exceeds the maximum size
  file_size=$(stat -c %s "$log_file")
  if [ "$file_size" -gt "$max_file_size" ]; then
    delete_log_file
  fi

  # Get system uptime
  uptimer=$(uptime -p)

  # Get CPU load
  cpu_load=$(mpstat 1 1 | awk '/Average:/ {print 100-$NF}' | awk '{printf "%.2f%%", $1}')

  # Get memory usage
  mem_usage=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')

  # Get CPU temperature
  cpu_temp=$(cat /sys/class/thermal/thermal_zone0/temp)
  cpu_temp=$(echo "scale=2; $cpu_temp / 1000" | bc)

  # Log the data
  log_data="Uptime: $uptimer | CPU Load: $cpu_load | Memory Usage: $mem_usage | CPU Temperature: $cpu_temp ° | Logsize:$file_size "
  echo "$log_data"
  echo "$log_data" >> "$log_file"

  # Wait for 30 seconds
  sleep 1
done
