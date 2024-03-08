import gzip
import os

def compress_file(file_path):
    compressed_file_path = './test_gzip.gz'
    with open(file_path, 'rb') as file:
        with gzip.open(compressed_file_path, 'wb') as compressed_file:
            compressed_file.writelines(file)
    compressed_size = os.path.getsize(compressed_file_path)
    return round(compressed_size * 8 / 1.5)

# svg_dir = "../svgs/"
# dirs = [f for f in os.listdir(svg_dir) if not f.startswith('.')]
# for dir in dirs:
#     os.makedirs('./test_result/' + dir, exist_ok=True)
#     with open("./test_result/" + dir + '/gzipped_bytes.csv', 'w') as file:
#         for filename in os.listdir(os.path.join(svg_dir, dir)):
#             if filename.endswith(".svg"):
#                 file.write(filename + ',')
#                 # print(os.path.join(svg_dir, dir, filename))
#                 file_path = os.path.join(svg_dir, dir, filename)
#                 file.write(str(compress_file(file_path)) + '\n')
print(compress_file('./test.svg'))
