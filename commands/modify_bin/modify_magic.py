import json
import os

from os import path as p

import bin_utils as b

pyscripts_path = p.dirname(p.dirname(p.dirname(p.realpath(__file__))))
git_free_path = p.join(pyscripts_path, "git-free")

def save_to_json(data, filename):
    """Save processed data to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def analyze_binary(image_path, json_path):
    contents = b.open_binary(image_path)
    output_data = b.process_image(contents)
    save_to_json(output_data, json_path)


def modify_magic_binary(image_path, new_image_path, new_magic):
    # Read the original binary contents
    contents = b.open_binary(image_path)

    # Unpack the image header to extract the fields
    magic, load_addr, hdr_size, img_size, flags, \
        ver_major, ver_minor, ver_revision, ver_build_num = b.unpack_image_header(contents)

    # Pack the modified image header with the new magic number
    modified_image_header = b.ImageHeader.pack(new_magic, load_addr, hdr_size, img_size, flags,
                                             ver_major, ver_minor, ver_revision, ver_build_num)

    # Combine the modified header with the rest of the binary contents
    modified_contents = modified_image_header + contents[b.ImageHeader.size:]

    # Write the modified contents to a new binary file
    with open(new_image_path, 'wb') as f:
        f.write(modified_contents)

    print(f"\n\nModified image file created: {new_image_path}\n")


main_path = p.join(git_free_path, "file")

if p.isdir(main_path):

    img_path = os.path.join(main_path, "zephyr.signed.bin")
    original_save_path = os.path.join(main_path, "signed_out.json")

    modified_img = os.path.join(main_path, "zephyr.modified.bin")
    modified_save_path = os.path.join(main_path, "modified_out.json")

    new_magic_value = 0xabcdef12

    analyze_binary(img_path, original_save_path)
    modify_magic_binary(img_path, modified_img, new_magic_value)
    analyze_binary(modified_img, modified_save_path)

else:
    print(f"{main_path} is not recognized")
