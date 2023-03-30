import asyncio

async def commit(path:str = "."):
    print(f"Adding {path}...")
    proc = await asyncio.create_subprocess_exec(
        "git", "add", path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f"[stdout] {stdout.decode()}")
    print(f"[stderr] {stderr.decode()}")
    print("Commiting...")
    proc = await asyncio.create_subprocess_exec(
        "git", "commit", "-m", "auto-push",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f"[stdout] {stdout.decode()}")
    print(f"[stderr] {stderr.decode()}")
    print("Pushing...")
    proc = await asyncio.create_subprocess_exec(
        "git", "push",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f"[stdout] {stdout.decode()}")
    print(f"[stderr] {stderr.decode()}")
    print("Done")




async def main():
    print("Starting...")
    await commit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())