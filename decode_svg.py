import decode_tag
import xml.etree.ElementTree as ET


# root = ET.Element('data')
# country = ET.SubElement(root,'country', {'name':'Liechtenstein'})  # root 增加 country 节点
# rank = ET.SubElement(country,'rank')  # country 增加 rank 节点
# rank.text = '1'
# year = ET.SubElement(country,'year')  # country 增加 year节点
# year.text = '2008'
# # ET.dump(root)


def get_allDNA(seq: str):
    allDNA = []
    for i in seq:
        allDNA.append(decode_tag.DNAseq2tag(i))
    return allDNA




# 直接写/用elementTree


def generate_circle(circle):
    # <circle class="st0" cx="32" cy="29.6" r="4.4"/>
    line = '<circle '
    if circle[-2] != None:
        line += 'id = \"{}\" '.format(circle[-2])
    if circle[-1] != None:
        line += 'class = \"{}\" '.format(circle[-1])
    line += 'cx = \"{}\" cy = \"{}\" r = \"{}\"/>'.format(
        circle[4], circle[5], circle[6])
    return line

# 关系有关！！！


def generate_g(g):
    line = '<g '
    if g[-2] != None:
        line += 'id = \"{}\" '.format(g[-2])
    if g[-1] != None:
        line += 'class = \"{}\" '.format(g[-1])
    line += '></g>'
    return line


def generate_path(path):
    line = '<path '
    if path[-2] != None:
        line += 'id = \"{}\" '.format(path[-2])
    if path[-1] != None:
        line += 'class = \"{}\" '.format(path[-1])
    line += 'd=\"{}\"'.format(path[4])
    line += '/>'
    return line


def generate_polygon(polygon):
    line = '<polygon '
    if polygon[-2] != None:
        line += 'id = \"{}\" '.format(polygon[-2])
    if polygon[-1] != None:
        line += 'class = \"{}\" '.format(polygon[-1])
    line += 'points = \"{}\"'.format(polygon[4])
    line += '/>'
    return line


def generate_rect(rect):
    line = '<rect '
    if rect[-2] != None:
        line += 'id = \"{}\" '.format(rect[-2])
    if rect[-1] != None:
        line += 'class = \"{}\" '.format(rect[-1])
    line += 'height=\"{}\" width=\"{}\" x=\"{}\" y=\"{}\"'.format(
        rect[7], rect[6], rect[4], rect[5])
    line += '/>'
    return line


def generate_style(style):
    line = '<style>'
    line += style[4]
    line += '</style>'
    return line


generate_tag_dict = {"circle": generate_circle, "g": generate_g, "path": generate_path,
                     "polygon": generate_polygon, "rect": generate_rect, "style": generate_style}


def func_None(seq):
    print('无对应函数')


def generate_tag(tag):
    name = tag[0]
    return generate_tag_dict.get(name, func_None)(tag)
# 将嵌套的标签写入


def add_child(root, child):
    line = '\n'.join([root[:-4], child])
    line += '\n'+root[-4:]
    return line
# 将并列的后一个标签写入


def add_bro(root, bro):
    line = '\n'.join([root, bro])
    return line



def dfs_add(allDNA, cur=0):
    # 将各个标签拼接
    first_child = allDNA[cur][2]
    bro = allDNA[cur][3]
    # ret = ''
    if first_child == None:
        if bro == None:
            return generate_tag(allDNA[cur])
        else:
            return add_bro(generate_tag(allDNA[cur]), dfs_add(allDNA, bro))
    else:
        return add_child(generate_tag(allDNA[cur]), dfs_add(allDNA, first_child))


def generate_svg(DNAseq):
    # 传入各个标签及参数的DNA序列list
    allDNA = get_allDNA(DNAseq) #将DNAseq转化成各个标签及参数
    allDNA = sorted(allDNA, key=lambda x: x[1])
    file = '<?xml version="1.0" ?>'
    root = '<svg width="64px" height="64px" viewBox="0 0 64 64" style="enable-background:new 0 0 64 64;" version="1.1" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n'
    file = root + dfs_add(allDNA) +'\n</svg>'
    return file


if __name__ == '__main__':
    seq = ['ATAATAAATTTATTA', 'ATAATTTATTAATCCGACGCTTGGTGCAAGAGAGTATTGGAGAAACGTTACTTCTATTGGTAAGTCATTGACTCTA', 'AAAATCTATTAATGCTAACAAAAAAAAAAAACTAATGCGAGAGAGAGTCTAAACAGAGAGAGAGTTGATGTGAGTGTAAGAA', 'TAAATGTATTAACTACTAAAGGAAAAAAAAAACTAACAGTAAAAAAAAACTAAACAGAGAGAGAGTCTAATAAGAGAGAGAGTTGATGTGAGTGTAAGAT', 'AGAACTATATTAACTTGAGTCGAGAGAGACACGAAGAGACGCAGTTACAAAGATAGTCACGCAGTCACGAAGATAGTCACGCAGAGACAAAGTAAGTGACGCAGTAACGAAGATAGTCACGCAGAGACAATGATGTGAGTGTAAGAT', 'ACAACTTTATTAACTCGTACTGCTAGTAGATAGACACGCAGATACGAAGACAGCAACGCAGTTTACAAGTGACGCAGTGTCAGACGTAGAAACGCAGTCACGAAGAAACGTAGATACGCAGATACGAAGAAACGCAGTTACGTAGATACGCAGATACGAAGATACGCAGATTGTCAGCAACGCAGCATCAGAGAAACGAAGAAACGCAGTCACGAAGAAACGCAGTTACGAAGATACGCAGATACGAAGATACGCAGATACGAAGATACGCAGATTCCAAGTAACGCAGTATCAGAGAAACGCAGTCACGAAGAAACGAAGATACGCAGATACGTAGAAACGCAGTTACGAAGATACGCAGATACGTAGATACGCAGATTGTCACGTAGCAACGCAGCAACAAACAAACAAACAAACAAACAATAAGAGATAGAGACGCAGACACGAAGACAGCAACGCAGCTACGAAGATAGACACGCAGTGACGAAGACAGCAACGCAGTTACGAAGATAGACACGCAGATACGAAGACAGCAACGCAGTTTGCCACAATAGTAGATAGATACGAAGAGAGTGACGCAGAGTACAAGCAACGCAGCATGTCACGTAGTCACGCAGTCTACAAGATAGATTTTCAGAGAGTGACGCAGAGTGCCTGATGTGAGTGTAAGAG', 'TTAACTCTATTTATTGTAGGTTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGAATGCGTCTCTCCTTCGATCGAAGCCACAGTATCTATCTATTTATTTAATAGCTAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGATTGCGTCTCTCCTTCGATCGAAGCCACAGTATAAGAGAGACAGTAAGAGAGTCAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGACTGCGTCTCTCCTTCGATCGAAGCCACAGAGCATATATATAAGATTATAAGAGAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGAGTGCGTCTCTCCTTCGATCGAAGCCACAGAGAGAGAGAGAATATAAGAAAGAAAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACAAACGCTGAGTGTAAGTATGCGTCTCTCCTTCGATCGAAGCCTCGCTCGGTCGCTCTTAGCGTGAGTGTATGACTCGGTCCGTCTTAGCCACAGAGAGAGAGAGAATATAAGAAAGAAAGCGTGAGTGTATGACTCGGTCCGTCTTACGTTCGATCCTTCGCTCTTTCAGTCATTGAAAGCCTGACTCGGTGTTTCGCTCTAAGCGTGAGTGTATGACTCGGTCCGTCTTACGTTCGATCCTTCGCTCTTTCCCTCGGTCCTTCGCAGCCTGACTCGGTGTTTCGCTCTAAGCGTGAGTGTATGACTCGGTCCGTCTTACGTTCGTTCCTTGTATCTTTGACTCGATCCTTCGTTCCTTGTAAGCCAGATAGAAAGCGTGGTAACCACAAACAAACAAACAAACAAACAAACAAACAAA']
    print(generate_svg(seq)) 