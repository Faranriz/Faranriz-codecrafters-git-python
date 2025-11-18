import sys
import os
import zlib
import hashlib

def main():
    # use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)
    
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == "cat-file" and sys.argv[2] == "-p":
        sha = sys.argv[3]
        filename = f".git/objects/{sha[0:2]}/{sha[2:]}"
        with open(filename, "rb") as f:
            compressed = f.read()
            data = zlib.decompress(compressed)
            null_index = data.index(b"\x00")
            content = data[null_index + 1:]
            print(content.decode("utf-8"), end="")
            
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
