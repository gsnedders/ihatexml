try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree

import re

spaces = re.compile("[\x20\x09\x0A\x0D]+")

def strip_element(parent, element):
    tail = element.tail
    idx = list(parent).index(element)
    if tail is not None:
        if idx == 0:
            if parent.text is not None:
                parent.text += tail
            else:
                parent.text = tail
        else:
            previous = parent[idx - 1]
            if previous.text is not None:
                previous.text += tail
            else:
                previous.text = tail
    parent.remove(element)

def get_prod(prod):
    lhs = prod.find("./lhs")
    rhses = prod.findall("./rhs")
    for rhs in rhses:
        for com in rhs.findall("./com"):
            strip_element(rhs, com)
    lhs_str = etree.tostring(lhs, "unicode", "text")
    rhses_str = map(lambda x: etree.tostring(x, "unicode", "text"), rhses)
    return "%s ::= %s" % (lhs_str.strip(), spaces.sub(" ", "".join(rhses_str)).strip())

def get_all_prods(doc):
    prods = doc.findall(".//prod")
    return map(get_prod, prods)

def main(fp):
    doc = etree.parse(fp)
    prods = get_all_prods(doc)
    print("\n".join(prods))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Extract EBNF from XML spec")
    parser.add_argument("file", help="file to parse")
    args = parser.parse_args()
    with open(args.file, "rb") as fp:
        main(fp)
