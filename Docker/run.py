#!/usr/bin/env python3
"""
One-shot launcher for the PX4 SITL Docker setup.

Builds the image if needed, then starts PX4 SITL with the Typhoon H480
model in Gazebo Classic (or a different target if you pass one).

Usage:
    python run.py                # build (if needed) + launch typhoon_h480
    python run.py <other_target> # launch a different vehicle model
    python run.py bash           # skip launching, just get a shell

Run this from inside the folder containing Dockerfile, docker-compose.yml,
and entrypoint.sh.

Before running: make sure Docker Desktop and VcXsrv are both up.
"""

import subprocess
import sys


def run(cmd):
    """Run a command, streaming output live, and exit on failure."""
    print(f">> {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"!! Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def docker_available():
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "gazebo-classic_typhoon_h480"

    print(">> Checking Docker is available...")
    if not docker_available():
        print("!! Docker doesn't seem to be running (or isn't installed).")
        print("!! Start Docker Desktop and try again.")
        sys.exit(1)

    print(">> Building image (skips layers that haven't changed)...")
    run(["docker", "compose", "build"])

    print(f">> Starting PX4 SITL container (target: {target})...")
    run(["docker", "compose", "run", "--rm", "px4-sitl", target])


if __name__ == "__main__":
    main()
