#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

import imageio_ffmpeg


ROOT = Path(__file__).resolve().parent.parent
SCENES_DIR = ROOT / "assets" / "movie-scenes"


def clean_file(path: Path, dry_run: bool) -> bool:
    temp_path = path.with_name(f".{path.stem}.metadata-clean.mp4")
    title = path.name
    command = [
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-y",
        "-i",
        str(path),
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-map_metadata",
        "-1",
        "-map_chapters",
        "-1",
        "-c",
        "copy",
        "-metadata",
        f"title={title}",
        "-movflags",
        "+faststart",
        str(temp_path),
    ]

    if dry_run:
        print(path.name)
        return False

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        temp_path.replace(path)
    except subprocess.CalledProcessError as error:
        if temp_path.exists():
            temp_path.unlink()
        print(f"Failed: {path.name}\n{error.stderr}")
        return False

    print(f"Cleaned: {path.name}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove inherited MP4 metadata and set the title to the file name.")
    parser.add_argument("--dry-run", action="store_true", help="Only list files that would be processed.")
    args = parser.parse_args()

    files = sorted(SCENES_DIR.glob("*.mp4"))
    cleaned = sum(clean_file(path, args.dry_run) for path in files)

    if args.dry_run:
        print(f"{len(files)} files would be processed.")
    else:
        print(f"{cleaned} files cleaned.")


if __name__ == "__main__":
    main()
