def update_val_from_bits(bit_list):
    val = 0
    for i, state in enumerate(bit_list):
        if state:
            val |= (1 << i)
    return val

def update_bits_from_val(val):
    bits = []
    for i in range(32):
        bits.append(bool((val >> i) & 1))
    return bits