import os
import re

root = r"C:\Users\Michael\Desktop\coding\python\panda_ops"

exts = [
    '.js',
    '.ts',
    '.tsx',
    '.py',
    '.css'
]

exclude_dirs = [
    'node_modules', 
    'resources_old',
    'resources',
    'public',
    'venv',
    '__pycache__',
    '.git'
]

output_checked_files = True


def get_line_count(filepath):
    if output_checked_files:
        print(filepath)
    line_count = 0
    blank_count = 0
    with open(filepath, mode='r') as f:
        for line in f.readlines():
            if bool(re.search(r'\S', line)):
                line_count += 1
            else:
                blank_count += 1
    return line_count, blank_count


def print_stats(d):
    total_loc = 0
    total_blank = 0
    for ext in d.keys():
        print(ext)
        print("  loc: " + str(d[ext]['line_count']))
        print("  blank: " + str(d[ext]['blank_count']))
        print('')
        total_loc += d[ext]['line_count']
        total_blank += d[ext]['blank_count']
    print("total loc: " + str(total_loc))
    print("total blank: " + str(total_blank))


def main():
    os.chdir(root)

    d = {}

    for (dirpath, dirnames, filenames) in os.walk(root, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        filenames = [f for f in filenames if any([f.endswith(ext) for ext in exts])]

        if filenames == []:
            continue
        
        for filename in filenames:
            file_to_count = os.path.join(dirpath, filename)
            if not os.path.isfile(file_to_count):
                continue

            ext = filename.split('.')[-1]
            counts = get_line_count(file_to_count)
            if ext not in d.keys():
                d[ext] = {
                    "line_count": 0,
                    "blank_count": 0
                }
            d[ext]['line_count'] += counts[0]
            d[ext]['blank_count'] += counts[1]
    
    print_stats(d)


if __name__ == "__main__":
    main()
