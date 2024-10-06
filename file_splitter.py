"""
Made for infinite cloud storage on discord.
Splits files into 8 MB chunks of binary data, and vice versa
"""

import os
from shutil import rmtree

# Some important variables
main_dir: str = os.path.dirname(os.path.abspath(__file__))
main_dir = main_dir.replace(os.sep, "/")
binary_out: str = main_dir + "/BIN_OUT"
file_out: str = main_dir + "/FILE_OUT"

# Converts files into 8 MB chunks, and stores their file type in their name.
# Creates a directory containing every chunk. The directory name follows this format: (file_name)_(file_type)
# Chunk names follow this format: (id)_(file_name)_(file_type).bin
def file_to_bin(path: str) -> None:
    name_prefix, file_type = os.path.splitext(os.path.basename(path))
    name_prefix += f"_{file_type[1:]}"
    # Convert the original file to binary
    with open(path, "rb") as file:
        bin_data: bytes = file.read()

    chunks = [] # Not using list comprehension for readability
    # NOTE: because im kinda slow, 8 MB = 8 000 KB = 8 000 000 bytes = 64 000 000 bits
    for c in range(len(bin_data) // 8_000_000):
        chunks.append(bin_data[8_000_000 * c: 8_000_000 * (c+1)])
    chunks.append(bin_data[(len(chunks)-1) * 8_000_000:])

    # Create files for all of the chunks and put it in its own directory
    os.mkdir(binary_out + f"/{name_prefix}")
    for i, chunk in enumerate(chunks):
        with open(binary_out + f"/{name_prefix}/{i}_{name_prefix}.bin", "wb") as file:
            file.write(chunk)

def bin_to_file(dir: str) -> None:
    chunks_gen = os.walk(dir)
    chunks_gen = chunks_gen.__next__()[2]
    chunks = []
    for c in chunks_gen:
        with open(dir + f"/{c}", "rb") as file:
            chunks.append(file.read())
    
    combined_data = b"".join(chunks)

    # Spliting the directory into the file name and type
    split_index = -1
    while os.path.basename(dir)[split_index] != "_":
        split_index -= 1
    file_name, file_type = os.path.basename(dir)[:split_index], os.path.basename(dir)[split_index+1:]
    
    newPath = file_out + f"/{file_name}.{file_type}"
    with open(newPath, "wb") as file:
        file.write(combined_data)
    
def clear_directory(path: str) -> None:
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__" and True:
    os.system("cls")

    # Initialize folders
    if os.path.exists(binary_out):
        pass
    else:
        print("BIN_OUT initialized.")
        os.makedirs(binary_out)

    if os.path.exists(file_out):
        pass
    else:
        print("FILE_OUT initialized.")
        os.makedirs(file_out)
    
    # Get inputs
    print("""1 => Convert file to binary
2 => Convert binary back into original file
3 => Clear BIN_OUT and FILE_OUT directories""")
    operation = int(input("Conversion Type: "))
    os.system("cls")
    
    path_to_convert = input("Enter the file/directory path: ")
    path_to_convert = path_to_convert.replace(os.sep, "/")
    os.system("cls")

    match (operation):
        case 1:
            file_to_bin(path_to_convert)
        
        case 2:
            bin_to_file(path_to_convert)

        case 3:
            clear_directory(binary_out)
            clear_directory(file_out)

        case _:
            pass
