#!/usr/bin/env sh

CYCLES=1
SILENT=false
USERID=17
TOR_PORT=9053
CONTENT_SIZE=10
DOMAIN="example.donotexist"
CONTENT_DIRECTORIES=("browser_ext" "discord" "sus_files" "wallet")

succ=0
fail=0
current_cycle=1

send_data() {
  curl -X POST "$DOMAIN/$1" \
    -H "userid: $USERID" \
    -H "Content-Type: application/json" \
    -d "$2"

  if [[ $? -eq 0 ]]; then
    echo "Successfully uploaded $filepath"
    succ=$((succ+1))  # Increment the success counter
  else
    echo "Failed to upload $filepath"
    fail=$((fail+1))  # Increment the failure counter
  fi
}

run_command() {
    if [ "$SILENT" = true ]; then
        "$@" > /dev/null 2>&1  # Suppress output
    else
        "$@"  # Show output
    fi
}

# Function to display help
function show_help {
    echo "Usage: unrat [OPTIONS]"
    echo
    echo "Options:"
    echo "  -h        Show this help message."
    echo "  -l        Only log files."
    echo "  -u USERID Set the user ID (default: 17)."
    echo "  -c CYCLES Set the number of cycles (default: 1)."
    echo "  -s CONTENT_SIZE Set the content size (default: 100)."
    echo "  -p TOR_PORT Set the Tor port (default: 9053)."
    echo "  -d DOMAIN Set the domain (default: example.donotexist)."
    exit 0
}

# Parse options
while getopts "hl:u:c:s:p:d:" opt; do
    case $opt in
        h)
            show_help
            ;;
        l)
            SILENT=true
            ;;
        u)
            USERID=$OPTARG
            ;;
        c)
            CYCLES=$OPTARG
            ;;
        p)
            TOR_PORT=$OPTARG
            ;;
        d)
            DOMAIN=$OPTARG
            ;;
        *)
            show_help
            ;;
    esac
done

if [[ -z "$CYCLES" || "$CYCLES" -le 0 ]]; then
    echo "CYCLES is not set or invalid. Set to 1."
    CYCLES=1
fi

if [[ -z "$CONTENT_SIZE" || "$CONTENT_SIZE" -le 0 ]]; then
    echo "CONTENT_SIZE is not set or invalid. Set to 10."
    CONTENT_SIZE=10
fi

while [[ $current_cycle -le $CYCLES ]] ; do
  echo "Killing tor"
  pkill -x "tor"
  echo "Starting tor with port $TOR_PORT"
  tor --SocksPort $TOR_PORT &
  export "ALL_PROXY=socks5://127.0.0.1:$TOR_PORT"
  echo "Exported ALL_PROXY variable to $ALL_PROXY"

  echo "Creating tmp folder"
  tempfolder="tmp$((RANDOM % CONTENT_SIZE + 1))"
  mkdir $tempfolder
  cd  $tempfolder
 
  # Running python gen scripts
  run_command python ../gen_browsers_ext.py $((RANDOM % CONTENT_SIZE + 1))
  run_command python ../gen_cookies.py $((RANDOM % CONTENT_SIZE + 1))
  run_command python ../gen_discord.py $((RANDOM % CONTENT_SIZE + 1))
  run_command python ../gen_usernames_passwds.py $((RANDOM % CONTENT_SIZE + 1))
  run_command python ../gen_wallets.py $((RANDOM % CONTENT_SIZE + 1))
  run_command python ../gen_sus.py $((RANDOM % CONTENT_SIZE + 1))

#    Single files
#    .
#    ├── cookies
#    │   └── cookies.json
#    ├── discord
#    │   └── discord-tokens.txt
#    └── passwords
#        └── passwords.json

  # Check if tor is running
  if pgrep -x "tor" > /dev/null; then
      echo "SUCCESS: Tor is running"
  else
      echo "Tor failed to start, exiting..."
      exit 1
  fi

  # Send false cookies
  echo "Sending false cookies"
  send_data "webdata" "$(cat cookies/cookies.json)"

  # Send false passwords
  echo "Sending false passwords"
  send_data "pw" "$(cat cookies/cookies.json)"

  for folder in "${CONTENT_DIRECTORIES[@]}"; do
      # Find all files in the folder recursively
      for filepath in "$folder"/*; do
          if [[ -f "$filepath" ]]; then  # Make sure it's a file
              echo "Uploading $filepath"
  
              # Use curl to send the file with POST request
              curl -X POST "$DOMAIN/delivery" \
                  -H "userid: $USERID" \
                  -F "file=@$filepath"
  
              if [[ $? -eq 0 ]]; then
                  echo "Successfully uploaded $filepath"
                  succ=$((succ+1))  # Increment the success counter
              else
                  echo "Failed to upload $filepath"
                  fail=$((fail+1))  # Increment the failure counter
              fi
          fi
      done
  done

  echo "Succesfully sent: $succ"
  echo "Failed: $fail"
  cd ../
  echo "Removing tempfolder"
  rm -r $tempfolder

  sleep 0.5
  echo "Cycle: $current_cycle"
  ((current_cycle++))
done
