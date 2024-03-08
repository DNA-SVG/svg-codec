import os, time
from codec.codec import Codec

svg_dir = "../svgs/"
dirs = [f for f in os.listdir(svg_dir) if not f.startswith('.')]
codec = Codec()
start = time.perf_counter()
for dir in dirs:
    os.makedirs('./test_result/' + dir, exist_ok=True)
    with open('./test_result/' + dir + '/default.csv', 'w') as file:
        for filename in os.listdir(os.path.join(svg_dir, dir)):
            if filename.endswith(".svg"):
                file.write(filename + ',')
                # print(os.path.join(svg_dir, dir, filename))
                codec.outputDNAseq(os.path.join(svg_dir, dir, filename), "test_out.txt")
                # codec.outputSVG('./test_out.txt', './text_result.svg')
                file.write(str(os.path.getsize("test_out.txt")) + '\n')
# os.remove('./text_result.svg')
end = time.perf_counter()
print("Time elapsed:", end - start)