#!/usr/bin/env python3
"""Build and run one of the HALO MAVSDK programs."""

from pathlib import Path
import shutil
import subprocess
import sys


IMAGE_NAME = "halo-mavsdk"
REPO_DIR = Path(__file__).resolve().parent
DOCKERFILE = REPO_DIR / "Movement" / "Dockerfile.mavsdk"


def run(command: list[str]) -> None:
    print(f">> {' '.join(command)}", flush=True)
    subprocess.run(command, check=True)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python run_all.py <folder> <file.cpp>")
        print("Example: python run_all.py Movement test_takeoff.cpp")
        return 2

    folder = Path(sys.argv[1])
    file_name = Path(sys.argv[2]).name
    folder_path = REPO_DIR / folder
    matches = list(folder_path.rglob(file_name)) if folder_path.is_dir() else []
    if not matches or Path(file_name).suffix != ".cpp":
        print(f"C++ file not found: {folder / file_name}")
        return 2
    if len(matches) > 1:
        choices = "\n".join(f"  {path.relative_to(REPO_DIR)}" for path in matches)
        print(f"Multiple C++ files named '{file_name}' were found:\n{choices}")
        print("Use a folder that contains only one match.")
        return 2
    source_path = matches[0]
    program_path = f"/app/build/{source_path.stem}"

    if shutil.which("docker") is None:
        print("Docker was not found on PATH. Start Docker Desktop and try again.")
        return 1

    try:
        run([
            "docker", "build", "-f", str(DOCKERFILE), "-t", IMAGE_NAME,
            "--build-arg", "BUILD_JOBS=2", str(REPO_DIR),
        ])

        run([
            "docker", "run", "--rm", "--network", "host", IMAGE_NAME,
            program_path,
        ])
    except subprocess.CalledProcessError as error:
        print(f"Docker command failed with exit code {error.returncode}.")
        return error.returncode
    except KeyboardInterrupt:
        print("\nMission stopped.")
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())