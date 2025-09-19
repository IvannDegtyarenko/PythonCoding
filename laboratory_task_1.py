import argparse
parser = argparse.ArgumentParser(description="Document to program")
parser.add_argument("filepath", type=argparse.FileType("r"))
args = parser.parse_args()

with args.filepath as file:
    print(file.read())