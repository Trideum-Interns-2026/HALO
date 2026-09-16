# PX4 SITL Setup — NVIDIA DGX Spark

This folder is a platform-agnostic PX4 SITL + Gazebo Classic + ROS 2 Docker
setup. The same files also work on Windows (via `docker-compose.windows.yml`)
— `run.py` auto-detects which platform you're on and picks the right one.

## What's in this folder

| File | Purpose |
|---|---|
| `Dockerfile` | Shared image definition (Ubuntu 22.04 + ROS 2 Humble + PX4 deps). Works on both amd64 and arm64 — no changes needed per platform. |
| `entrypoint.sh` | Clones PX4-Autopilot, installs deps, builds, and launches — all automatic. |
| `docker-compose.yml` | Shared base config (volume, build settings). |
| `docker-compose.spark.yml` | Spark-specific overrides: GPU passthrough, native X11 display. |
| `docker-compose.windows.yml` | Windows-specific overrides (not used on the Spark, kept for parity). |
| `run.py` | One-command launcher — detects the platform and runs the right compose files. |

You do **not** need to download PX4-Autopilot separately — it's cloned
automatically into a persistent Docker volume the first time you run this.

---

## One-time setup on the Spark

### 1. Confirm GPU + Container Toolkit
```
nvidia-smi
dpkg -l | grep nvidia-container-toolkit
```
If the toolkit is missing:
```
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```
Confirm it works:
```
docker run --rm --gpus all ubuntu nvidia-smi
```

### 2. Install QGroundControl (runs natively on the Spark, not in Docker)
Download the AppImage from qgroundcontrol.com, then:
```
chmod +x QGroundControl.AppImage
./QGroundControl.AppImage
```

### 3. Allow Docker to use the display
```
xhost +local:docker
```
This needs to be re-run after every reboot (or add it to your `~/.bashrc`).

---

## Running it

From inside this folder:
```
python3 run.py
```
This auto-detects Linux/ARM64 and uses `docker-compose.spark.yml` automatically.

First run will take a while — it installs ROS 2, PX4 build dependencies,
clones PX4-Autopilot, and does a full build from scratch. Every run after
that reuses the same Docker volume, so it's much faster.

Other useful commands:
```
python3 run.py bash                          # get a shell instead of launching
python3 run.py gazebo-classic_iris           # launch a different vehicle model
python3 run.py --platform spark              # force the Spark override explicitly
```

---

## What should happen

- Gazebo opens directly on the Spark's own display, GPU-accelerated (no
  VcXsrv, no remote X forwarding — much better frame rate than the Windows
  setup).
- QGroundControl (running natively, opened separately) shows **Ready** in
  the top-right, connected automatically over UDP — no port-mapping or
  "disconnected banner" issues like on Windows, since there's no WSL2/NAT
  networking layer in the way.

---

## Troubleshooting

Most of the build/runtime issues we hit while developing this setup
(stale build state, `ninja: unknown target` errors, missing shebang lines,
etc.) and their fixes are documented in `PX4-SITL-Docker-Troubleshooting.md`
— worth checking there first if something looks familiar. The
Windows-specific sections (VcXsrv, `host.docker.internal`, port mapping)
don't apply here, but everything about PX4's build system itself still does.
