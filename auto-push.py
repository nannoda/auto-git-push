import asyncio
import os
import sys
LOGGING = True


def log(msg)->None:
    if LOGGING:
        print(msg)

this_path = os.path.dirname(os.path.abspath(__file__))

async def update_repo(path:str = "."):
    """
    Updates the repo by pulling, adding, commiting, and pushing
    """
    # change directory to the path
    os.chdir(path)
    log("Changing directory...")
    log(f"Current directory: {os.getcwd()}")
    
    log("Pulling...")
    proc = await asyncio.create_subprocess_exec(
        "git", "pull",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        log(f"[stdout] {stdout.decode()}")
    if stderr:
        log(f"[stderr] {stderr.decode()}")

    log(f"Adding {path}...")
    proc = await asyncio.create_subprocess_exec(
        "git", "add", path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        log(f"[stdout] {stdout.decode()}")
    if stderr:
        log(f"[stderr] {stderr.decode()}")


    log("Commiting...")
    proc = await asyncio.create_subprocess_exec(
        "git", "commit", "-m", "auto-push",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        log(f"[stdout] {stdout.decode()}")
    if stderr:
        log(f"[stderr] {stderr.decode()}")
    log("Pushing...")
    proc = await asyncio.create_subprocess_exec(
        "git", "push",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        log(f"[stdout] {stdout.decode()}")
    if stderr:
        log(f"[stderr] {stderr.decode()}")
    log("Done")

async def main():
    # getting args using argparse
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", "-l", 
                        help="log the output",
                        type=bool,
                        default=True)
    parser.add_argument("--interval", "-i", 
                        help="interval in seconds", 
                        type=int,
                        default=60)
    parser.add_argument("--path-file", "-p",
                        help="a file that contains the path to all repos",
                        type=str,
                        default="path.txt")
    
    args = parser.parse_args()
    global LOGGING
    LOGGING = args.log
    log(f"Interval: {args.interval} seconds")

    log("Starting...")
    while True:
        # update the repo
        try:
            os.chdir(this_path)
            with open(args.path_file, "r") as f:
                paths = f.readlines()
            for path in paths:
                path = path.strip()
                if path.startswith("#"):
                    continue
                log(f"Updating path: \"{path}\"")
                await update_repo(path)
        except Exception as e:
            log(e)
        log("Waiting...")
        await asyncio.sleep(args.interval)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())