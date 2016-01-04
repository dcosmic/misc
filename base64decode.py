import sys
import os
import csv
import base64


def get_encodes(encode_file_path):
    encoded_set = set()
    with open(encode_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for eachline in reader:
            encoded_set.add(eachline[0])
    return(encoded_set)


def decoding_base64(data_set):
    decoded_set = set()
    for s in data_set:
        if len(s) % 4 != 0:
            cut = len(s) - len(s) % 4
            s = s[:cut]
        decoded_text = base64.b64decode(s)
        print(decoded_text)
        decoded_set.add(decoded_text)
    return decoded_set


def write_decoded(decoded_set, decode_file_path):
    with open(decode_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in decoded_set:
            print(i.decode())
            writer.writerow([i.decode()])


if __name__ == '__main__':

    # print sys.argv
    if len(sys.argv) <= 1:
        print('No argument!  please input the dot dir!')

    else:
        s_dir = sys.argv[1]

        encode_file_path = s_dir + '\\encode.csv'
        decode_file_path = s_dir + '\\decode.csv'
        if os.path.exists(s_dir):
            e_set = get_encodes(encode_file_path)
            d_set = decoding_base64(e_set)
            write_decoded(d_set, decode_file_path)
