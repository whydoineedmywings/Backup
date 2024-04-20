from os import path
from sched import scheduler
from shutil import copytree
from time import time, sleep
from datetime import datetime
from argparse import ArgumentParser, Namespace

def backup(src_dir: str, dst_dir: str) -> None:
    backup_folder: str = path.join(
        dst_dir,
        datetime.now().strftime("%Y.%m.%d/%H.%M.%S")
    )

    try:
        copytree(src_dir, backup_folder)
        print(f"Backup complited successfully! Backup directory: {backup_folder}")
    except Exception as ex:
        print(f"Backup was complited with an exception: {ex}")

def schedule_backup(timeout: int, sc: scheduler, src_dir: str, dst_dir: str) -> None:
    backup(src_dir, dst_dir)
    sc.enter(timeout, 1, schedule_backup, (timeout, sc, src_dir, dst_dir))

def main() -> None:
    parser: ArgumentParser = ArgumentParser(
        prog="Backup", 
        description="Create a copy of files",
        epilog="Created by whydoineedmywings?"
    )

    parser.add_argument(
        "--time", 
        type=int, 
        help="Time in seconds after which a copy of the files will be created",
        required=True,
    )

    parser.add_argument(
        "--src",
        type=str,
        help="The directory from which the copy will be made",
        required=True
    )

    parser.add_argument(
        "--dst",
        type=str,
        help="The directory to which the copy will be made",
        required=True
    )

    argv: Namespace = parser.parse_args()
    print(f"Time: {argv.time}, src: {argv.src}, dst: {argv.dst}")

    event: scheduler = scheduler(time, sleep)
    event.enter(0, 1, schedule_backup, (argv.time, event, argv.src, argv.dst))
    event.run()


if __name__ == "__main__":
    main()
