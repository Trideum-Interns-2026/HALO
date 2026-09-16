# PX4 SITL + Gazebo dev container
# PX4-Autopilot is cloned directly into a persistent named volume on first
# run (see entrypoint.sh + docker-compose.yml) — no local source folder or
# host path needed. Build artifacts then persist in that volume across
# `docker compose run --rm` instead of rebuilding from scratch each time.

FROM px4io/px4-dev-ros2-foxy

# Default vehicle model to build/launch (override via PX4_TARGET env var
# or by passing a target name to `docker compose run`)
ARG PX4_TARGET=gazebo-classic_typhoon_h480

# Make sure git is available (usually already in base image, safe no-op if so)
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# UDP port QGroundControl connects on
EXPOSE 14540/udp

WORKDIR /PX4-Autopilot

# Copy in the entrypoint that auto-runs `make px4_sitl <target>` on start.
# The sed calls strip a BOM / CRLF line endings if they ever creep in from
# a Windows editor, since either one breaks the shebang line on Linux.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i '1s/^\xEF\xBB\xBF//' /usr/local/bin/entrypoint.sh \
    && sed -i 's/\r$//' /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh

ENV PX4_TARGET=${PX4_TARGET}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# Default arg = launch with $PX4_TARGET. Override with "bash" for a shell,
# or another target name (e.g. gazebo_iris) to launch a different model.
CMD []s