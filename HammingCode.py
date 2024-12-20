with open('input.txt', 'r') as input_file:
    input_data = input_file.readline().strip()

data_list = [int(digit) for digit in input_data]

index = 0
while 2**index <= len(data_list):
    data_list.insert(2**index - 1, 0)
    index += 1

for control_bit in range(1, index + 1):
    parity_bits = []
    for group_start in range(0, len(data_list), 2**control_bit):
        for bit_index in range(group_start, group_start + 2**(control_bit - 1)):
            try:
                parity_bits.append(data_list[bit_index + 2**(control_bit - 1) - 1])
            except IndexError:
                pass
    data_list[2**(control_bit - 1) - 1] = 1 if sum(parity_bits) % 2 else 0

encoded_message = ''.join(map(str, data_list))
print('Encoded message:', encoded_message)

with open('output.txt', 'w') as output_file:
    output_file.write('Message encoded with Hamming code:\n' + encoded_message)

with open('recieved.txt', 'r') as received_file:
    received_data = received_file.readline().strip()

received_list = [int(digit) for digit in received_data]

index = 0
while 2**index <= len(received_list):
    received_list[2**index - 1] = 0
    index += 1

for control_bit in range(1, index + 1):
    parity_bits = []
    for group_start in range(0, len(received_list), 2**control_bit):
        for bit_index in range(group_start, group_start + 2**(control_bit - 1)):
            try:
                parity_bits.append(received_list[bit_index + 2**(control_bit - 1) - 1])
            except IndexError:
                pass
    received_list[2**(control_bit - 1) - 1] = 1 if sum(parity_bits) % 2 else 0

error_positions = []
for degree in range(index):
    if received_list[2**degree - 1] != data_list[2**degree - 1]:
        error_positions.append(2**degree)

if not error_positions:
    print('\nNo errors in received message.')
    for idx in range(index):
        if 2**idx <= len(received_list):
            received_list[2**idx - 1] = 'x'
    decoded_message = ''.join(map(str, received_list)).replace('x', '')
    print('\nDecoded message:', decoded_message)
else:
    error_position = sum(error_positions)
    print('\nError found at position:', error_position)
    received_list[error_position - 1] ^= 1

    for idx in range(index):
        if 2**idx <= len(received_list):
            received_list[2**idx - 1] = 'x'
    corrected_message = ''.join(map(str, received_list)).replace('x', '')
    print('\nCorrected message:', corrected_message)