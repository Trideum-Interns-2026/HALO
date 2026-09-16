# PX4 SITL Setup — Windows

This folder is a platform-agnostic PX4 SITL + Gazebo Classic + ROS 2 Docker
setup. The same files also work on the NVIDIA DGX Spark (via
`docker-compose.spark.yml`) — `run.py` auto-detects which platform you're
on and picks the right one.

## What's in this folder

| File | Purpose |
|---|---|
| `Dockerfile` | Shared image definition (Ubuntu 22.04 + ROS 2 Humble + PX4 deps). Works on both amd64 and arm64 — no changes needed per platform. |
| `entrypoint.sh` | Clones PX4-Autopilot, installs deps, builds, and launches — all automatic. |
| `docker-compose.yml` | Shared base config (volume, build settings). |
| `docker-compose.windows.yml` | Windows-specific overrides: VcXsrv display forwarding, port mapping. |
| `docker-compose.spark.yml` | Spark-specific overrides (not used on Windows, kept for parity). |
| `run.py` | One-command launcher — detects the platform and runs the right compose files. |

You do **not** need to download PX4-Autopilot separately — it's cloned
automatically into a persistent Docker volume the first time you run this.

---

## One-time setup on Windows

### 1. Install Docker Desktop
Download from docker.com, install, and make sure the **WSL 2 backend** is
enabled (Settings → General → "Use the WSL 2 based engine").

### 2. Install an X server (for Gazebo's GUI)
Download **VcXsrv**: https://sourceforge.net/projects/vcxsrv/
Launch it with:
- Multiple windows
- Display number: `0`
- Disable access control (checked)

Leave it running in the background whenever you want to run the sim.

### 3. Install QGroundControl
Download from qgroundcontrol.com and install/run it normally — it runs
directly on Windows, not inside Docker.

### 4. Install Python (for `run.py`)
If you don't already have it, install Python 3 from python.org (or the
Microsoft Store), and make sure `python` is available from PowerShell.

---

## Running it

From inside this folder, in PowerShell:
```
python run.py
```
This auto-detects Windows and uses `docker-compose.windows.yml` automatically.

First run will take a while — it installs ROS 2, PX4 build dependencies,
clones PX4-Autopilot, and does a full build from scratch. Every run after
that reuses the same Docker volume, so it's much faster.

Other useful commands:
```
python run.py bash                          # get a shell instead of launching
python run.py gazebo-classic_iris           # launch a different vehicle model
python run.py --platform windows            # force the Windows override explicitly
```

Make sure **Docker Desktop** and **VcXsrv** are both running before you launch.

---

## What should happen

- A Gazebo window appears on your Windows desktop via VcXsrv, showing the
  vehicle model.
- QGroundControl (opened separately) shows **Ready** in the top-right,
  connected automatically over UDP.

### A known limitation on Windows
Gazebo's rendering goes through VcXsrv over X11, which typically can't do
full hardware-accelerated GPU rendering the way native Linux can — so frame
rates are noticeably lower than on the Spark (we saw ~7fps in testing).
This is a limitation of the Windows/WSL2/VcXsrv rendering path itself, not
a bug in this setup. If smooth frame rates matter more than Windows
convenience, the Spark (or any native Linux machine) will perform much better.

---

## Troubleshooting

Every build/runtime issue we hit while developing this setup — stale build
state, `ninja: unknown target` errors, missing shebang lines, the
QGroundControl "disconnected banner" fix, stuck volumes/networks, and more
— is documented with its fix in `PX4-SITL-Docker-Troubleshooting.md`. Check
there first if something looks familiar.
