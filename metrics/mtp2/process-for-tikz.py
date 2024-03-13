import sys


def insert_line(file_path, line):
    with open(file_path, "r+") as file:
        content = file.read()
        file.seek(0, 0)
        file.write(line.rstrip("\r\n") + "\n" + content)


line_to_insert = "X\tY"


def sort_file(file_path):
    try:
        # Open the file for reading
        with open(file_path, "r") as file:
            lines = file.readlines()

            # Sort the lines based on 'a'
            sorted_lines = sorted(lines, key=lambda x: float(x.split("\t")[0]))

            # Write sorted lines back to the file
            with open(file_path, "w") as file:
                for line in sorted_lines:
                    file.write(line)

            print("File sorted successfully!")

    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        sort_file(file_path)
        insert_line(file_path, line_to_insert)
