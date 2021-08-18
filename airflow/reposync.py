import subprocess
from helpers import get_snapshot_folder, setup_rclone


if __name__ == "__main__":
    folder = get_snapshot_folder()
    setup_rclone()
    subprocess.run(
        f"rclone copy --progress sftp:snapshots/{folder}/lotus_datadir s3:sentinel-backfill/repo/mainnet/{folder}",
        shell=True,
        check=True,
    )
