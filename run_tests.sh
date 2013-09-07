#!/bin/bash

NOSETEST_OPTIONS="-s -d"

if [ -n "$NOSE_PROCESSES" ]; then
    NOCOLOR=1
    unset COVERAGE
else
    NOSETEST_OPTIONS="$NOSETEST_OPTIONS --failed"
fi

if [ -n "$VERBOSE" ]; then
    NOSETEST_OPTIONS="$NOSETEST_OPTIONS --verbose"
fi

if [ -n "$STOPFIRST" ]; then
    NOSETEST_OPTIONS="$NOSETEST_OPTIONS --stop"
fi

NOSETEST_OPTIONS="$NOSETEST_OPTIONS $TESTS"

rm test.log
nosetests $NOSETEST_OPTIONS 2>&1 | tee -a test.log

exit ${PIPESTATUS[0]}
