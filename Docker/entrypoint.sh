#!/bin/bash
set -e

TARGET="${1:-${PX4_TARGET:-gazebo-classic_typhoon_h480}}"

# /PX4-Autopilot is a persistent named volume — starts empty on first run,
# on either platform.
if [ ! -f "/PX4-Autopilot/Makefile" ]; then
    echo ">> Persistent volume is empty — cloning PX4-Autopilot into it (one-time)..."
    git clone --recurse-submodules https://github.com/PX4/PX4-Autopilot.git /PX4-Autopilot
fi

cd /PX4-Autopilot

# Install PX4's own build dependencies once per volume. Using PX4's
# official script (rather than a prebaked image) is what makes this work
# unmodified on amd64 (Windows) and arm64 (Spark) alike.
if [ ! -f "/PX4-Autopilot/.deps_installed" ]; then
    echo ">> Installing PX4 build dependencies (one-time, several minutes)..."
    bash ./Tools/setup/ubuntu.sh --no-nuttx
    touch /PX4-Autopilot/.deps_installed
fi

# Always ensure Python deps are present, independent of the stamp file
# above — ubuntu.sh doesn't reliably install everything the build needs.
# kconfiglib specifically isn't always covered by requirements.txt, so
# install it explicitly rather than relying on that file alone.
echo ">> Ensuring Python build dependencies are present..."
pip3 install --no-cache-dir -r Tools/setup/requirements.txt --quiet
pip3 install --no-cache-dir kconfiglib --quiet
echo ">> Python dependencies OK"

if [ "$TARGET" = "bash" ] || [ "$TARGET" = "shell" ]; then
    exec /bin/bash
fi

echo ">> Launching PX4 SITL with target: $TARGET"
echo ">> QGroundControl should auto-connect on UDP 14550"
echo ">> Gazebo should appear on your display"
echo

if [ ! -f "/PX4-Autopilot/build/px4_sitl_default/bin/px4" ]; then
    echo ">> First build — configuring px4_sitl_default first..."
    make px4_sitl_default
fi

exec make px4_sitl "$TARGET"
