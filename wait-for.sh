
#!/bin/sh
# wait-for.sh: wait for a service to be available before executing a command.
# Usage: wait-for.sh host:port [-t timeout] [-- command args...]

set -e

TIMEOUT=15
QUIET=0
COMMAND="$@"

while [ $# -gt 0 ]; do
    case "$1" in
        *:* )
        HOST=$(printf "%s\n" "$1"| cut -d : -f 1)
        PORT=$(printf "%s\n" "$1"| cut -d : -f 2)
        shift 1
        ;;
        -q)
        QUIET=1
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [ "$TIMEOUT" = "" ]; then break; fi
        shift 2
        ;;
        --)
        shift
        COMMAND="$@"
        break
        ;;
        *)
        echo "Usage: $0 host:port [-t timeout] [-- command args...]"
        exit 1
        ;;
    esac
done

if [ "$HOST" = "" ] || [ "$PORT" = "" ]; then
    echo "Error: you need to provide a host and port to test."
    exit 1
fi

wait_for() {
    if [ "$QUIET" -eq 0 ]; then echo "Waiting for $HOST:$PORT..."; fi
    for i in `seq $TIMEOUT` ; do
        nc -z "$HOST" "$PORT" > /dev/null 2>&1
        result=$?
        if [ $result -eq 0 ] ; then
            if [ "$QUIET" -eq 0 ]; then echo "Service $HOST:$PORT is available."; fi
            if [ -n "$COMMAND" ] ; then
                exec $COMMAND
            fi
            exit 0
        fi
        sleep 1
    done
    echo "Operation timed out" >&2
    exit 1
}

wait_for