#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def check_shelby():
    return subprocess.run(["shelby", "--version"], capture_output=True).returncode == 0


def upload_file(filepath, blob_name=None, expiry_days=30):
    if not Path(filepath).exists():
        return {"success": False, "error": f"File not found: {filepath}"}
    blob_name = blob_name or Path(filepath).name
    cmd = ["shelby", "upload", "--file", filepath,
           "--name", blob_name, "--expiry", str(expiry_days * 86400 * 1000)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {"success": result.returncode == 0, "blob_name": blob_name,
            "error": result.stderr.strip()}


def upload_directory(dirpath, prefix="", expiry_days=30):
    results = []
    for fp in Path(dirpath).rglob("*"):
        if fp.is_file():
            rel = fp.relative_to(dirpath)
            name = f"{prefix}/{rel}".lstrip("/") if prefix else str(rel)
            r = upload_file(str(fp), name, expiry_days)
            print(f"{'✅' if r['success'] else '❌'} {name}")
            results.append(r)
    return results


def main():
    p = argparse.ArgumentParser(description="Upload files to Shelby Protocol")
    sub = p.add_subparsers(dest="cmd")
    fp = sub.add_parser("file")
    fp.add_argument("filepath")
    fp.add_argument("--name")
    fp.add_argument("--expiry", type=int, default=30)
    dp = sub.add_parser("dir")
    dp.add_argument("dirpath")
    dp.add_argument("--prefix", default="")
    dp.add_argument("--expiry", type=int, default=30)
    args = p.parse_args()
    if not args.cmd:
        p.print_help(); sys.exit(1)
    if not check_shelby():
        print("❌ Shelby CLI not found: npm install -g @shelby-protocol/cli"); sys.exit(1)
    if args.cmd == "file":
        r = upload_file(args.filepath, args.name, args.expiry)
        print(f"{'✅' if r['success'] else '❌ ' + r.get('error', '')} {r.get('blob_name','')}")
    elif args.cmd == "dir":
        results = upload_directory(args.dirpath, args.prefix, args.expiry)
        ok = sum(1 for r in results if r["success"])
        print(f"\n📊 {ok} uploaded, {len(results)-ok} failed")


if __name__ == "__main__":
    main()
