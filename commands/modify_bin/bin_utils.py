# Mainly from Marti Bolivar (GithubGist : @mbolivar)
# https://gist.github.com/mbolivar/285309cca792f746d6c698f56941041a

import struct

# Constants and Formats
IMG_HDR_MAGIC = 0x96f3b83d
TLV_INFO_MAGIC = 0x6907
IMAGE_F_RAM_LOAD = 0x00000020

IMG_HDR_FMT = '<IIHxxIIbbhIxxxx'
TLV_INFO_FMT = '<HH'
TLV_HDR_FMT = '<bxH'

TLV_HDR_TYPES = {
    0x01: 'IMAGE_TLV_KEYHASH',
    0x10: 'IMAGE_TLV_SHA256',
    0x20: 'IMAGE_TLV_RSA2048_PSS',
    0x21: 'IMAGE_TLV_ECDSA224',
    0x22: 'IMAGE_TLV_ECDSA256'
}

# Named tuples for structures
ImageHeader = struct.Struct(IMG_HDR_FMT)
TLVInfo = struct.Struct(TLV_INFO_FMT)
TLVHeader = struct.Struct(TLV_HDR_FMT)


def verify_magic(magic_number, expected_magic):
    """Verify if the magic number matches the expected value."""
    return magic_number == expected_magic


def open_binary(image_path):
    """Read binary data from the specified image file."""
    try:
        with open(image_path, 'rb') as f:
            contents = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
    return contents


def unpack_image_header(contents):
    """Unpack the image header from binary contents."""
    return ImageHeader.unpack_from(contents)


def unpack_tlv_info(contents, offset):
    """Unpack TLV info from binary contents at the specified offset."""
    return TLVInfo.unpack_from(contents, offset)


def unpack_tlv_header(contents, offset):
    """Unpack TLV header from binary contents at the specified offset."""
    return TLVHeader.unpack_from(contents, offset)


def process_image(contents):
    """Process the image file and extract header, TLV info, and TLV headers."""

    # Unpack Image Header
    magic, load_addr, hdr_size, img_size, flags, \
        ver_major, ver_minor, ver_revision, ver_build_num = unpack_image_header(contents)

    # Verify Image Header Magic
    magic_hdr_check = verify_magic(magic, IMG_HDR_MAGIC)
    print(f"\nImage Header Magic Number Verification: {'OK' if magic_hdr_check else 'BAD'}\n")

    # Display Initial Image Bytes
    print('Initial Image Bytes:')
    start = hdr_size
    end = start + min(20, img_size)
    print('\t' + ' '.join(f'{b:02X}' for b in contents[start:end]))

    # Unpack TLV Info
    tlv_info_offset = hdr_size + img_size
    tlv_magic, tlv_size = unpack_tlv_info(contents, tlv_info_offset)

    # Verify TLV Info Magic
    magic_info_check = verify_magic(tlv_magic, TLV_INFO_MAGIC)
    print(f"TLV Info Magic Number Verification: {'OK' if magic_info_check else 'BAD'}\n")

    magic_hex = hex(magic)

    # Prepare Output Data Structure
    output_data = {
        "img_header": {
            "magic_dec": magic,
            "magic_hex": magic_hex,
            "img_size": img_size,
            "version": {
                "major": ver_major,
                "minor": ver_minor,
                "revision": ver_revision,
                "build": ver_build_num
            }
        },
        "tlv_info": {
            "magic": tlv_magic,
            "tlv_size": tlv_size
        },
        "tlv_headers": []
    }

    # Process TLV Headers
    tlv_end = tlv_info_offset + tlv_size
    tlv_off = tlv_info_offset + struct.calcsize(TLV_INFO_FMT)

    while tlv_off < tlv_end:
        tlv_type, tlv_len = unpack_tlv_header(contents, tlv_off)

        tlv_header = {
            "type": TLV_HDR_TYPES.get(tlv_type, f'Unknown (0x{tlv_type:02X})'),
            "len": tlv_len
        }
        output_data["tlv_headers"].append(tlv_header)

        if tlv_len <= 32:
            start = tlv_off + struct.calcsize(TLV_HDR_FMT)
            end = start + tlv_len
            tlv_bytes = ' '.join(f'{b:02X}' for b in contents[start:end])
            tlv_header["data"] = tlv_bytes
            print('\t' + tlv_bytes)

        tlv_off += struct.calcsize(TLV_HDR_FMT) + tlv_len

    return output_data