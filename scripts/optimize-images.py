#!/usr/bin/env python3

from pathlib import Path
import shutil
import subprocess
import sys


MEDIA_DIR = Path("media")
CONTENT_DIR = Path("_days")

MAX_DIMENSION = 1600
WEBP_QUALITY = 78

SOURCE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def find_imagemagick() -> str:
    """Find ImageMagick 7 or ImageMagick 6 executable."""
    for command in ("magick", "convert"):
        executable = shutil.which(command)

        if executable:
            return executable

    raise SystemExit(
        "ImageMagick nebyl nalezen. "
        "Nainstaluj jej přes brew nebo apt."
    )


def replace_content_references(
    replacements: dict[str, str],
) -> int:
    """Replace old image paths in Markdown frontmatter."""
    changed_files = 0

    if not CONTENT_DIR.exists():
        return changed_files

    for path in CONTENT_DIR.rglob("*.md"):
        original = path.read_text(encoding="utf-8")
        updated = original

        for old_path, new_path in replacements.items():
            old_public = f"/{old_path}"
            new_public = f"/{new_path}"

            updated = updated.replace(old_public, new_public)
            updated = updated.replace(old_path, new_path)

        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1

    return changed_files


def main() -> None:
    if not MEDIA_DIR.exists():
        print("Složka media neexistuje, není co optimalizovat.")
        return

    imagemagick = find_imagemagick()

    source_files = sorted(
        path
        for path in MEDIA_DIR.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SOURCE_EXTENSIONS
    )

    if not source_files:
        print("Žádné nové JPG nebo PNG fotografie.")
        return

    replacements: dict[str, str] = {}
    original_size = 0
    optimized_size = 0

    for source in source_files:
        target = source.with_suffix(".webp")

        if target.exists() and target != source:
            raise SystemExit(
                f"Nelze převést {source}: "
                f"cílový soubor {target} už existuje."
            )

        temporary = target.with_name(
            f".{target.stem}.temporary.webp"
        )

        original_size += source.stat().st_size

        command = [
            imagemagick,
            str(source),
            "-auto-orient",
            "-resize",
            f"{MAX_DIMENSION}x{MAX_DIMENSION}>",
            "-strip",
            "-define",
            "webp:method=4",
            "-quality",
            str(WEBP_QUALITY),
            str(temporary),
        ]

        subprocess.run(command, check=True)

        if not temporary.exists() or temporary.stat().st_size == 0:
            raise SystemExit(
                f"Optimalizace {source} nevytvořila platný soubor."
            )

        temporary.replace(target)
        optimized_size += target.stat().st_size

        old_relative = source.as_posix()
        new_relative = target.as_posix()

        replacements[old_relative] = new_relative
        source.unlink()

        print(
            f"{old_relative} -> {new_relative} "
            f"({target.stat().st_size / 1024:.0f} kB)"
        )

    changed_documents = replace_content_references(
        replacements
    )

    saving = original_size - optimized_size
    saving_percent = (
        saving / original_size * 100
        if original_size
        else 0
    )

    print()
    print(f"Převedeno fotografií: {len(source_files)}")
    print(f"Upraveno zápisků: {changed_documents}")
    print(
        f"Velikost před: {original_size / 1024 / 1024:.2f} MB"
    )
    print(
        f"Velikost po:   {optimized_size / 1024 / 1024:.2f} MB"
    )
    print(f"Úspora:        {saving_percent:.1f} %")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(
            f"ImageMagick skončil s chybou: {error}",
            file=sys.stderr,
        )
        raise SystemExit(error.returncode)
