def modify_bin_file(input_file, output_file):
    # Step 1: Read the first 15 bytes from the input .bin file
    with open(input_file, 'rb') as f:
        original_data = bytearray(f.read(15))

    # Step 2: Modify the 10th byte (index 9 in zero-based index)
    if len(original_data) >= 10:
        original_data[9] = 0xFF  # Modify the 10th byte to 0xFF (example modification)

    # Step 3: Save the modified data to a new .bin file
    with open(output_file, 'wb') as f:
        f.write(original_data)

    # Step 4: Read the first 15 bytes from the modified .bin file
    with open(output_file, 'rb') as f:
        modified_data = f.read(15)

    return modified_data


# Specify input and output file paths
input_file_path = r"../../git-free/file/zephyr.signed.bin"
output_file_path = r"../../git-free/file/zephyr.signed.output.bin"

# Modify the .bin file and retrieve the modified data
modified_first_15_bytes = modify_bin_file(input_file_path, output_file_path)

# Print the modified first 15 bytes (in hexadecimal format)
print("Modified 15 bytes:", modified_first_15_bytes.hex())
