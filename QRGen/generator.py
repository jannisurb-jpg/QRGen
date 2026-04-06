import reedsolo
from PIL import Image, ImageDraw
import sys

data = sys.argv[1]
output_path = sys.argv[2]

color = "black"

error_correction = "L"  # L--> 7%, M --> 15%, Q --> 25%, H --> 30%

error_correction_bits = ""

if error_correction == "L":
    error_correction_bits = "01" #1
elif error_correction == "M":
    error_correction_bits = "00" #0
elif error_correction == "Q":
    error_correction_bits = "11" #3
elif error_correction == "H":
    error_correction_bits = "10" #2

qr_byte_capacity_L = [
    17, 32, 53, 78, 106, 134, 154, 192, 230, 271,
    321, 367, 425, 458, 520, 586, 644, 718, 792, 858,
    929, 1003, 1091, 1171, 1273, 1367, 1465, 1528, 1628, 1732,
    1840, 1952, 2068, 2188, 2303, 2431, 2563, 2699, 2809, 2953
]
qr_byte_capacity_M = [
    14, 26, 42, 62, 84, 106, 122, 152, 180, 213,
    251, 287, 331, 362, 412, 450, 504, 560, 624, 666,
    711, 779, 857, 911, 997, 1059, 1125, 1190, 1264, 1370,
    1452, 1538, 1628, 1722, 1809, 1911, 1989, 2099, 2213, 2331
]
qr_byte_capacity_Q = [
    11, 20, 32, 46, 60, 74, 86, 108, 130, 151,
    177, 203, 241, 258, 292, 322, 364, 394, 442, 482,
    509, 565, 611, 661, 715, 751, 805, 868, 908, 982,
    1030, 1112, 1168, 1228, 1283, 1351, 1423, 1499, 1579, 1663
]
qr_byte_capacity_H = [
    7, 14, 24, 34, 44, 58, 64, 84, 98, 119,
    137, 155, 177, 194, 220, 250, 280, 310, 338, 382,
    403, 439, 461, 511, 535, 593, 625, 658, 698, 742,
    790, 842, 898, 958, 983, 1051, 1093, 1139, 1219, 1273
]

qr_ec_data_codewords = {
    'L': [
        19, 34, 55, 80, 108, 136, 156, 194, 232, 274,
        324, 370, 428, 461, 523, 589, 647, 721, 795, 861,
        932, 1006, 1094, 1174, 1276, 1370, 1468, 1531, 1631, 1735,
        1843, 1955, 2071, 2191, 2306, 2434, 2566, 2702, 2812, 2956
    ],
    'M': [
        16, 28, 44, 64, 86, 108, 124, 154, 182, 216,
        254, 290, 334, 365, 415, 453, 507, 563, 627, 669,
        714, 782, 860, 914, 1000, 1062, 1128, 1193, 1267, 1373,
        1455, 1541, 1631, 1725, 1812, 1914, 1992, 2102, 2216, 2334
    ],
    'Q': [
        13, 22, 34, 48, 62, 76, 88, 110, 132, 154,
        180, 206, 244, 261, 295, 325, 367, 397, 445, 485,
        512, 568, 614, 664, 718, 754, 808, 871, 911, 985,
        1033, 1115, 1171, 1231, 1286, 1354, 1426, 1502, 1582, 1666
    ],
    'H': [
        9, 16, 26, 36, 46, 60, 66, 86, 100, 122,
        140, 158, 180, 197, 223, 253, 283, 313, 341, 385,
        406, 442, 464, 514, 538, 596, 628, 661, 701, 745,
        793, 845, 901, 961, 986, 1054, 1096, 1142, 1222, 1276
    ]
}

qr_ec_codewords_count = {
    'L': [7,10,15,20,26,18,20,24,30,18,20,24,26,30,22,24,28,30,28,28,28,28,30,30,26,28,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
    'M': [10,16,26,18,24,16,18,22,22,26,30,22,22,26,26,26,26,26,26,26,26,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28],
    'Q': [13,22,18,26,18,24,18,22,20,24,28,26,24,20,30,24,28,28,28,28,28,30,30,30,30,28,30,30,30,30,30,30,30,30,30,30,30,30,30,30],
    'H': [17,28,22,16,22,28,26,26,24,28,24,28,22,24,24,30,28,28,26,28,30,24,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30,30]
}

# Block structure: (num_blocks_type1, data_cw_per_block_type1, num_blocks_type2, data_cw_per_block_type2)
# Type2 blocks have one extra data codeword compared to type1
qr_block_info = {
    'L': [
        (1,19,0,0),(1,34,0,0),(1,55,0,0),(1,80,0,0),(1,108,0,0),
        (2,68,0,0),(2,78,0,0),(2,97,0,0),(2,116,0,0),(2,68,2,69),
        (4,81,0,0),(2,92,2,93),(4,107,0,0),(3,115,1,116),(5,87,1,88),
        (5,98,1,99),(1,107,5,108),(5,120,1,121),(3,113,4,114),(3,107,5,108),
        (4,116,4,117),(2,111,7,112),(4,121,5,122),(6,117,4,118),(8,106,4,107),
        (10,114,2,115),(8,122,4,123),(3,117,10,118),(7,116,7,117),(5,115,10,116),
        (13,115,3,116),(17,115,0,0),(17,115,1,116),(13,115,6,116),(12,121,7,122),
        (6,121,14,122),(17,122,4,123),(4,122,18,123),(20,117,4,118),(19,118,6,119),
    ],
    'M': [
        (1,16,0,0),(1,28,0,0),(1,44,0,0),(2,32,0,0),(2,43,0,0),
        (4,27,0,0),(4,31,0,0),(2,38,2,39),(3,36,2,37),(4,43,1,44),
        (1,50,4,51),(6,36,2,37),(8,37,1,38),(4,40,5,41),(5,41,5,42),
        (7,45,3,46),(10,46,1,47),(9,43,4,44),(3,44,11,45),(3,41,13,42),
        (17,42,0,0),(17,46,0,0),(4,47,14,48),(6,45,14,46),(8,47,13,48),
        (19,46,4,47),(22,45,3,46),(3,45,23,46),(21,45,7,46),(19,45,10,46),
        (2,45,29,46),(10,45,23,46),(14,45,21,46),(14,45,23,46),(12,45,26,46),
        (6,45,34,46),(29,45,14,46),(13,45,32,46),(40,45,7,46),(18,45,31,46),
    ],
    'Q': [
        (1,13,0,0),(1,22,0,0),(2,17,0,0),(2,24,0,0),(2,15,2,16),
        (4,19,0,0),(2,14,4,15),(4,18,2,19),(4,16,4,17),(6,19,2,20),
        (4,22,4,23),(4,20,6,21),(8,20,4,21),(11,16,5,17),(5,24,7,25),
        (15,19,2,20),(1,22,15,23),(17,22,1,23),(17,21,4,22),(15,24,5,25),
        (17,22,6,23),(7,24,16,25),(11,24,14,25),(11,22,16,23),(17,22,14,23),
        (11,24,14,25),(22,23,13,24),(18,24,13,25),(26,21,17,22),(11,23,22,24),
        (19,23,21,24),(11,24,31,25),(32,23,21,24),(31,24,21,25),(28,23,28,24),
        (16,24,34,25),(3,23,51,24),(14,23,46,24),(15,23,52,24),(17,23,52,24),
    ],
    'H': [
        (1,9,0,0),(1,16,0,0),(2,13,0,0),(4,9,0,0),(2,11,2,12),
        (4,15,0,0),(4,13,1,14),(4,14,2,15),(4,12,4,13),(6,15,2,16),
        (3,12,8,13),(7,14,4,15),(12,11,4,12),(11,12,5,13),(11,12,7,13),
        (3,15,13,16),(2,14,17,15),(2,14,19,15),(9,13,16,14),(15,11,10,12),
        (19,16,6,17),(34,13,0,0),(16,15,14,16),(30,16,2,17),(22,15,13,16),
        (33,16,4,17),(12,15,28,16),(11,15,31,16),(19,15,26,16),(23,15,25,16),
        (23,15,28,16),(19,15,35,16),(11,15,46,16),(59,16,1,17),(22,15,41,16),
        (2,15,64,16),(24,15,46,16),(42,15,32,16),(10,15,67,16),(20,15,61,16),
    ]
}

qr_required_remainder_bits = [
    0,                          # V1
    7,7,7,7,7,                  # V2-6
    0,0,0,0,0,0,0,              # V7-13
    3,3,3,3,3,3,3,              # V14-20
    4,4,4,4,4,4,4,              # V21-27
    3,3,3,3,3,3,3,              # V28-34
    0,0,0,0,0,0                 # V35-40
]

final_padding_byte_first = "11101100"
final_padding_byte_second = "00010001"
mode_indicator = "0100" # numeric mode --> 0001, alphanumeric mode --> 0010, byte mode --> 0100, kanji mode --> 1000, eci mode --> 0111 | Just byte mode is working properly


def determine_smallest_version(bytesVar):
    caps = {'L': qr_byte_capacity_L, 'M': qr_byte_capacity_M,
            'Q': qr_byte_capacity_Q, 'H': qr_byte_capacity_H}
    for version, capacity in enumerate(caps[error_correction], start=1):
        if bytesVar <= capacity:
            return version
    print("Wrong error correction mode!")


def determine_padded_length(binary_bytes):
    padded_length = ""
    if len(binary_bytes) < 16:
        missing_chars = 16 - len(binary_bytes)
        for i in range(missing_chars):
            padded_length += "0"
        padded_length += binary_bytes
        return padded_length


def get_encoded_data(inputString):
    encoded_data = ""
    for char in inputString:
        encoded_data += format(ord(char), '08b')
    return encoded_data


def determine_required_bit_length(version, ec):
    total_codewords = qr_ec_data_codewords[ec][version - 1]
    return int(total_codewords) * 8


def add_terminator(bit_string, required_bit_length):
    difference = required_bit_length - len(bit_string)
    for i in range(difference):
        if i < 4:
            bit_string += "0"
    return bit_string


def make_bit_string_multiple_of_eight(bit_string):
    remainder = len(bit_string) % 8
    zeros_to_be_added = 8 - remainder
    for i in range(zeros_to_be_added):
        bit_string += "0"
    return bit_string


def fill_up_to_max_cap(bit_string, required_bit_length):
    difference = required_bit_length - len(bit_string)
    difference //= 8
    for i in range(int(difference)):
        if i % 2 == 0:
            bit_string += final_padding_byte_first
        else:
            bit_string += final_padding_byte_second
    return bit_string


def bytes_from_bitstring(bit_string):
    return [int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8)]


def split_into_blocks(data_bytes, version, ec_level):
    """
    Splits data bytes into blocks according to QR spec.
    Returns list of blocks, each block is a list of bytes.
    """
    n1_blocks, n1_cw, n2_blocks, n2_cw = qr_block_info[ec_level][version - 1]

    blocks = []
    idx = 0

    # Type 1 blocks
    for _ in range(n1_blocks):
        blocks.append(data_bytes[idx:idx + n1_cw])
        idx += n1_cw

    # Type 2 blocks (one extra codeword each)
    for _ in range(n2_blocks):
        blocks.append(data_bytes[idx:idx + n2_cw])
        idx += n2_cw

    return blocks


def generate_ec_for_blocks(blocks, version, ec_level):
    """
    Generates EC codewords for each block separately.
    Returns list of EC blocks.
    """
    num_ec = qr_ec_codewords_count[ec_level][version - 1]
    ec_blocks = []

    for block in blocks:
        rsc = reedsolo.RSCodec(num_ec)
        full = rsc.encode(bytes(block))
        ec_block = list(full[-num_ec:])
        ec_blocks.append(ec_block)

    return ec_blocks


def interleave(data_blocks, ec_blocks):
    """
    Interleaves data blocks and EC blocks per QR spec:
    First all data codewords interleaved, then all EC codewords interleaved.
    """
    interleaved = []

    # Interleave data blocks: take one byte from each block in turn
    max_data_len = max(len(b) for b in data_blocks)
    for i in range(max_data_len):
        for block in data_blocks:
            if i < len(block):
                interleaved.append(block[i])

    # Interleave EC blocks: take one byte from each EC block in turn
    max_ec_len = max(len(b) for b in ec_blocks)
    for i in range(max_ec_len):
        for block in ec_blocks:
            if i < len(block):
                interleaved.append(block[i])

    return interleaved


def bytes_to_bitstring(byte_list):
    return ''.join(format(b, '08b') for b in byte_list)


# ---- Main ----

input_string = data
how_many_bytes = len(input_string)
how_many_bytes_binary = format(how_many_bytes, '08b')

print(f"You need {how_many_bytes} Bytes")

version = determine_smallest_version(how_many_bytes)
print(f"Version: {version}")

# Build bit string
if version > 9:
    padded_length = str(determine_padded_length(how_many_bytes_binary))
    bit_string = mode_indicator + padded_length
else:
    bit_string = mode_indicator + str(how_many_bytes_binary)

bit_string += get_encoded_data(input_string)

required_bit_length = determine_required_bit_length(version, error_correction)

if required_bit_length - len(bit_string) > 0:
    bit_string = add_terminator(bit_string, required_bit_length)
elif required_bit_length - len(bit_string) < 0:
    print("ERROR: Data too long!")

if len(bit_string) % 8 != 0:
    bit_string = make_bit_string_multiple_of_eight(bit_string)

if required_bit_length - len(bit_string) > 0:
    bit_string = fill_up_to_max_cap(bit_string, required_bit_length)
elif required_bit_length - len(bit_string) < 0:
    print("ERROR: Bit string too long!")

data_bytes = bytes_from_bitstring(bit_string)
print(f"Data codewords: {len(data_bytes)}")

# Split into blocks
data_blocks = split_into_blocks(data_bytes, version, error_correction)
print(f"Number of blocks: {len(data_blocks)}")
for i, block in enumerate(data_blocks):
    print(f"  Block {i+1}: {len(block)} data bytes -> {block}")

# Generate EC per block
ec_blocks = generate_ec_for_blocks(data_blocks, version, error_correction)
for i, ec in enumerate(ec_blocks):
    print(f"  EC Block {i+1}: {len(ec)} EC bytes -> {ec}")

# Interleave
final_bytes = interleave(data_blocks, ec_blocks)
final_bitstring = bytes_to_bitstring(final_bytes)

#add remainder bits
final_bitstring += "0" * qr_required_remainder_bits[version - 1]

print(f"\nBits before EC: {len(bit_string)}")
print(f"Bits after EC (interleaved): {len(final_bitstring)}")
print(f"\nFinal bitstring:\n{final_bitstring}")

image = Image.new("RGB", (21 + (4 * (version - 1)), (21 + (4 * (version - 1)))), "white")

draw = ImageDraw.Draw(image)

#Hard code finder patterns
grid_size = 21 + 4 * (version - 1)

for rows in range(grid_size):
    for columns in range(grid_size):
        if rows == 0 or rows == 6:
            if (columns < 7 or columns > grid_size - 8):
                draw.point((columns, rows), fill=color)
        elif rows > 0 and rows < 7:
            if columns == 0 or columns == 6 or columns == grid_size - 7 or columns == grid_size - 1:
                draw.point((columns, rows), fill=color)     
        if rows == 2 or rows == 3 or rows == 4:
            if (columns > 1 and columns < 5) or (columns > grid_size - 6 and columns < grid_size - 2):
                draw.point((columns, rows), fill=color)

        if rows == grid_size - 7 or rows == grid_size - 1:
            if (columns < 7):
                draw.point((columns, rows), fill=color)
        elif rows > grid_size - 7 and rows < grid_size:
            if columns == 0 or columns == 6:
                draw.point((columns, rows), fill=color) 
        if rows in (grid_size-5, grid_size-4, grid_size-3):
            if (columns > 1 and columns < 5):
                draw.point((columns, rows), fill=color)

# Alignment pattern center coordinates per version (Version 1 = keine)
alignment_pattern_coords = {
    1:  [],
    2:  [6, 18],
    3:  [6, 22],
    4:  [6, 26],
    5:  [6, 30],
    6:  [6, 34],
    7:  [6, 22, 38],
    8:  [6, 24, 42],
    9:  [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98,  122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170],
}

def is_near_finder(row, col, grid_size):
    """Prüft ob ein Alignment Pattern die Finder Patterns überlappen würde."""
    # Oben-links: Zeilen 0-8, Spalten 0-8
    if row <= 8 and col <= 8:
        return True
    # Oben-rechts: Zeilen 0-8, Spalten grid_size-8 bis grid_size-1
    if row <= 8 and col >= grid_size - 8:
        return True
    # Unten-links: Zeilen grid_size-8 bis grid_size-1, Spalten 0-8
    if row >= grid_size - 8 and col <= 8:
        return True
    return False

def draw_alignment_pattern(draw, center_row, center_col):
    """Zeichnet ein 5x5 Alignment Pattern mit zufälligen Farben."""
    for r in range(center_row - 2, center_row + 3):
        for c in range(center_col - 2, center_col + 3):
            # Äußerer Ring (dunkel)
            if r == center_row - 2 or r == center_row + 2 or \
               c == center_col - 2 or c == center_col + 2:
                draw.point((c, r), fill=color)
            # Innerer Ring (hell / weiß)
            elif r == center_row - 1 or r == center_row + 1 or \
                 c == center_col - 1 or c == center_col + 1:
                draw.point((c, r), fill="white")
            # Mittelpunkt (dunkel)
            else:
                draw.point((c, r), fill=color)

# --- In deiner Haupt-Schleife, nach den Finder Patterns einfügen: ---

coords = alignment_pattern_coords.get(version, [])

# Alle möglichen (row, col) Kombinationen aus den Koordinaten
from itertools import product

for row, col in product(coords, repeat=2):
    if not is_near_finder(row, col, grid_size):
        draw_alignment_pattern(draw, row, col)

# Timing patterns - Zeile 6 und Spalte 6, zwischen den Finder Patterns
# Starten bei Index 8 und enden bei grid_size - 9 (nach den Separatoren)

for i in range(8, grid_size - 8):
    # Horizontales Timing Pattern (Zeile 6)
    if i % 2 == 0:
        draw.point((i, 6), fill=color)
    else:
        draw.point((i, 6), fill="white")
    
    # Vertikales Timing Pattern (Spalte 6)
    if i % 2 == 0:
        draw.point((6, i), fill=color)
    else:
        draw.point((6, i), fill="white")

# Dark Module - immer bei (8, 4*version + 9)
draw.point((8, 4 * version + 9), fill=color)
        
# Alle Funktionsmodule markieren - diese werden übersprungen
function_modules = set()

# Finder Patterns + Separatoren (8x8 pro Ecke)
for r in range(8):
    for c in range(8):
        function_modules.add((r, c))              # oben-links
        function_modules.add((r, grid_size-1-c))  # oben-rechts
        function_modules.add((grid_size-1-r, c))  # unten-links

# Timing Patterns
for i in range(8, grid_size - 8):
    function_modules.add((6, i))
    function_modules.add((i, 6))

# Dark Module
function_modules.add((8, 4 * version + 9))

# Format Info Bereiche
for i in range(9):
    function_modules.add((8, i))
    function_modules.add((i, 8))
for i in range(8):
    function_modules.add((8, grid_size - 1 - i))
    function_modules.add((grid_size - 1 - i, 8))

# Alignment Patterns
for row, col in product(coords, repeat=2):
    if not is_near_finder(row, col, grid_size):
        for r in range(row - 2, row + 3):
            for c in range(col - 2, col + 3):
                function_modules.add((r, c))

# Bits platzieren im Zick-Zack
bit_index = 0
going_up = True
col = grid_size - 1

while col >= 0:
    if col == 6:  # Timing Pattern Spalte überspringen
        col -= 1

    for i in range(grid_size):
        row = (grid_size - 1 - i) if going_up else i

        # Rechte Spalte des Paares
        if (row, col) not in function_modules:
            if bit_index < len(final_bitstring):
                bit = int(final_bitstring[bit_index])
                bit_index += 1
            else:
                bit = 0
            bit_color = color if bit == 1 else (255, 255, 255)
            draw.point((col, row), fill=bit_color)

        # Linke Spalte des Paares
        if col - 1 >= 0 and (row, col - 1) not in function_modules:
            if bit_index < len(final_bitstring):
                bit = int(final_bitstring[bit_index])
                bit_index += 1
            else:
                bit = 0
            bit_color = color if bit == 1 else (255, 255, 255)
            draw.point((col - 1, row), fill=bit_color)

    going_up = not going_up
    col -= 2

def get_mask_bit(mask, row, col):
    if mask == 0: return (row + col) % 2 == 0
    if mask == 1: return row % 2 == 0
    if mask == 2: return col % 3 == 0
    if mask == 3: return (row + col) % 3 == 0
    if mask == 4: return (row // 2 + col // 3) % 2 == 0
    if mask == 5: return (row * col) % 2 + (row * col) % 3 == 0
    if mask == 6: return ((row * col) % 2 + (row * col) % 3) % 2 == 0
    if mask == 7: return ((row + col) % 2 + (row * col) % 3) % 2 == 0

def penalty_score(pixels, grid_size):
    p = 0

    # Regel 1: 5+ gleiche Module in einer Reihe/Spalte
    for r in range(grid_size):
        run = 1
        for c in range(1, grid_size):
            if pixels[r][c] == pixels[r][c-1]:
                run += 1
            else:
                if run >= 5: p += 3 + (run - 5)
                run = 1
        if run >= 5: p += 3 + (run - 5)

    for c in range(grid_size):
        run = 1
        for r in range(1, grid_size):
            if pixels[r][c] == pixels[r-1][c]:
                run += 1
            else:
                if run >= 5: p += 3 + (run - 5)
                run = 1
        if run >= 5: p += 3 + (run - 5)

    # Regel 2: 2x2 Blöcke gleicher Farbe
    for r in range(grid_size - 1):
        for c in range(grid_size - 1):
            v = pixels[r][c]
            if v == pixels[r+1][c] == pixels[r][c+1] == pixels[r+1][c+1]:
                p += 3

    # Regel 3: Finder-ähnliche Muster
    pattern1 = [1,0,1,1,1,0,1,0,0,0,0]
    pattern2 = [0,0,0,0,1,0,1,1,1,0,1]
    for r in range(grid_size):
        for c in range(grid_size - 10):
            row_slice = [pixels[r][c+i] for i in range(11)]
            if row_slice == pattern1 or row_slice == pattern2:
                p += 40
    for c in range(grid_size):
        for r in range(grid_size - 10):
            col_slice = [pixels[r+i][c] for i in range(11)]
            if col_slice == pattern1 or col_slice == pattern2:
                p += 40

    # Regel 4: Verhältnis dunkler zu heller Module
    total = grid_size * grid_size
    dark = sum(pixels[r][c] for r in range(grid_size) for c in range(grid_size))
    percent = dark / total * 100
    prev_multiple = (int(percent) // 5) * 5
    next_multiple = prev_multiple + 5
    p += min(abs(prev_multiple - 50), abs(next_multiple - 50)) * 2 * 10

    return p

# Alle 8 Masken ausprobieren, beste wählen
best_mask = 0
best_penalty = float('inf')
best_pixels = None

# Aktuellen Zustand der Pixel auslesen
current_pixels = [[0] * grid_size for _ in range(grid_size)]
for r in range(grid_size):
    for c in range(grid_size):
        px = image.getpixel((c, r))
        current_pixels[r][c] = 0 if px == (255, 255, 255) else 1

for mask_num in range(8):
    # Kopie der aktuellen Pixel
    masked = [row[:] for row in current_pixels]

    # Maske nur auf Datenmodule anwenden
    for r in range(grid_size):
        for c in range(grid_size):
            if (r, c) not in function_modules:
                if get_mask_bit(mask_num, r, c):
                    masked[r][c] ^= 1  # Bit flippen

    pen = penalty_score(masked, grid_size)
    if pen < best_penalty:
        best_penalty = pen
        best_mask = mask_num
        best_pixels = masked

# Beste Maske auf das Bild anwenden
for r in range(grid_size):
    for c in range(grid_size):
        if best_pixels[r][c] == 1:
            draw.point((c, r), fill=color)
        else:
            draw.point((c, r), fill="white")

print(f"Beste Maske: {best_mask}, Penalty: {best_penalty}")

#add format string
format_string = error_correction_bits
format_string += format(best_mask, '03b')

original_format_string = format_string

generator_polynomial = "10100110111"

difference = 15 - len(format_string)

for i in range(difference):
    format_string += "0"


format_string = format_string.lstrip('0')

def format_string_creation(format_string, generator_polynomial):
    while len(generator_polynomial) != len(format_string):
        generator_polynomial += "0"

    result = str(format(int(generator_polynomial, 2) ^ int(format_string, 2), 'b'))

    result = result.lstrip('0')  # führende Nullen entfernen

    print("Result: ", result)

    return result

result = format_string_creation(format_string, generator_polynomial)

while len(result) > 10:
    result = format_string_creation(result, generator_polynomial)

if len(result) < 10:
    result = result.zfill(10)

print(result, len(result))

combined_string = original_format_string + result

final_format_string =  final_format_string = format(int(combined_string, 2) ^ int("101010000010010", 2), '015b')
print(final_format_string)

for i, char in enumerate(final_format_string):
    fill = color if char == "1" else (255, 255, 255)

    # Kopie 1 - oben links
    if i <= 5:
        draw.point((i, 8), fill=fill)
    elif i == 6:
        draw.point((7, 8), fill=fill)
    elif i == 7:
        draw.point((8, 8), fill=fill)
    elif i == 8:
        draw.point((8, 7), fill=fill)
    else:
        draw.point((8, 14 - i), fill=fill)

    # Kopie 2 - oben rechts und unten links
    if i <= 6:
        draw.point((8, grid_size - 7 + i), fill=fill)   # unten links, von unten nach oben
    else:
        draw.point((grid_size - 15 + i, 8), fill=fill)  # oben rechts, von links nach rechts

scale_factor = 10
img_resized = image.resize((grid_size*scale_factor, grid_size*scale_factor), Image.NEAREST)

img_resized.save(output_path)