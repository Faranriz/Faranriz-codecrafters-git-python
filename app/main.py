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

    # reading a blob object
    elif command == "cat-file":
        if not sys.argv[2] == "-p":
            raise RuntimeError(f"Unknown flag #{sys.argv[2]}")
        
        sha = sys.argv[3]
        filename = f".git/objects/{sha[0:2]}/{sha[2:]}"
        with open(filename, "rb") as f:
            compressed = f.read()
        data = zlib.decompress(compressed)
        null_index = data.index(b"\x00")
        content = data[null_index + 1:]
        print(content.decode("utf-8"), end="")

    # creating a blob object
    elif command == "hash-object":
        if not sys.argv[2] == "-w":
            raise RuntimeError(f"Unknown flag #{sys.argv[2]}")
        
        with open(sys.argv[3], "rb") as f:
            content = f.read()

        # build git object via 'blob <size>\0<content>'
        object = b"blob %d\x00%s" % (len(content), content)

        sha = hashlib.sha1(object).hexdigest()
        print(sha)

        # store in .git/objects/
        dir_name = f".git/objects/{sha[:2]}"
        filename = f"{dir_name}/{sha[2:]}"

        #make directory if not already existing
        os.makedirs(dir_name, exist_ok=True)
        with open(filename, "wb") as f:
            f.write(zlib.compress(object))




    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
