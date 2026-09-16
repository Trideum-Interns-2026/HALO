# PX4 SITL + Gazebo Classic dev container — platform-agnostic (amd64/arm64)
#
# Uses a plain Ubuntu base + PX4's own official dependency setup script,
# instead of the amd64-only px4io/px4-dev-* images. This is what makes the
# exact same Dockerfile work unmodified on both a Windows/x86 machine and
# an ARM64 device like the NVIDIA DGX Spark — only docker-compose.yml
# (network/display/GPU wiring) differs per platform, via override files.

FROM ubuntu:22.04

ARG PX4_TARGET=gz_x500
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    sudo \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3-pip \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*

# ROS 2 Humble — matches Ubuntu 22.04, has proper arm64 packages (unlike
# Foxy, which the original amd64-only px4io image used). This replaces
# that image's ROS 2 tooling.
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
       > /etc/apt/sources.list.d/ros2.list \
    && apt-get update && apt-get install -y --no-install-recommends \
       ros-humble-ros-base \
       ros-dev-tools \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc

# Gazebo Harmonic — installed from OSRF's own apt repo, NOT Ubuntu's
# default archive. Ubuntu's own gz-harmonic package doesn't reliably
# provide the CMake config files (gz-transport_DIR, gz-sim_DIR, etc.)
# that PX4's gz_bridge module needs to find it at configure time.
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
       > /etc/apt/sources.list.d/gazebo-stable.list \
    && apt-get update && apt-get install -y --no-install-recommends \
       gz-harmonic \
       libprotobuf-dev \
       protobuf-compiler \
       libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

ENV GZ_VERSION=harmonic

WORKDIR /PX4-Autopilot

EXPOSE 14540/udp
EXPOSE 14550/udp

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN sed -i '1s/^\xEF\xBB\xBF//' /usr/local/bin/entrypoint.sh \
    && sed -i 's/\r$//' /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh

ENV PX4_TARGET=${PX4_TARGET}
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD []