
import os, hashlib ,sys

def check_file(fobj, size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(size)
        if not chunk:
            return
        yield chunk

def check_for_duplicates(paths, hash=hashlib.sha1):
    hashes = {}
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                hashobj = hash()
                for chunk in check_file(open(full_path, 'rb')):
                    hashobj.update(chunk)
                file_id = (hashobj.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                if duplicate:
                    print "Duplicate found: %s and %s" % (full_path, duplicate)
                    #print full_path , type(full_path)
                    #print duplicate , type(duplicate)
                    if full_path:
                        os.remove(full_path)
                else:
                    hashes[file_id] = full_path

if sys.argv[1:]:
    check_for_duplicates(sys.argv[1:])
else:
    print "Please pass the paths to check as parameters to the script"