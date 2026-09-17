#!/bin/bash
set -e

TARGET="${1:-${PX4_TARGET:-gazebo-classic_typhoon_h480}}"

# /PX4-Autopilot is a persistent named volume (see docker-compose.yml), so
# it starts empty. Clone straight into it on first run only — after that,
# the volume keeps the source, build artifacts, and any changes between
# runs, so no re-clone or full rebuild is needed each time.
if [ ! -f "/PX4-Autopilot/Makefile" ]; then
    echo ">> Persistent volume is empty — cloning PX4-Autopilot into it (one-time)..."
    git clone --recurse-submodules https://github.com/PX4/PX4-Autopilot.git /PX4-Autopilot
fi

cd /PX4-Autopilot

if [ "$TARGET" = "bash" ] || [ "$TARGET" = "shell" ]; then
    exec /bin/bash
fi

echo ">> Launching PX4 SITL with target: $TARGET"
echo ">> QGroundControl should auto-connect on UDP 14550"
echo ">> Gazebo should appear via VcXsrv on the Windows host"
echo

# A truly fresh build needs px4_sitl_default built first to properly
# configure/generate the ninja build files — going straight for a model
# target (e.g. gazebo-classic_typhoon_h480) on a brand new build directory
# can fail with "unknown target '/bin/sh'" otherwise. This is a no-op
# (fast) on subsequent runs once already built.
if [ ! -f "/PX4-Autopilot/build/px4_sitl_default/bin/px4" ]; then
    echo ">> First build — configuring px4_sitl_default first..."
    make px4_sitl_default
fi

exec make px4_sitl "$TARGET"