from pathlib import Path
import shutil

DOWNLOADS = Path(r"C:\Users\student\Downloads")
TARGET_FOLDERS = {
    "images": {"jpg", "jpeg"},
    "data": {"csv", "xlsx"},
    "docs": {"txt", "doc", "pdf"},
    "archive": {"zip"},
    "binary": {"exe", "msi"},
}


def ensure_folder(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def unique_target_path(target_path: Path) -> Path:
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1
    while True:
        candidate = target_path.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def move_files():
    if not DOWNLOADS.exists() or not DOWNLOADS.is_dir():
        raise FileNotFoundError(f"Downloads 폴더를 찾을 수 없습니다: {DOWNLOADS}")

    for folder_name, extensions in TARGET_FOLDERS.items():
        ensure_folder(DOWNLOADS / folder_name)

    for item in DOWNLOADS.iterdir():
        if not item.is_file():
            continue

        ext = item.suffix.lower().lstrip('.')
        if not ext:
            continue

        for folder_name, extensions in TARGET_FOLDERS.items():
            if ext in extensions:
                dest_folder = DOWNLOADS / folder_name
                dest_path = unique_target_path(dest_folder / item.name)
                shutil.move(str(item), str(dest_path))
                print(f"Moved: {item.name} -> {dest_folder.name}")
                break


if __name__ == "__main__":
    move_files()
