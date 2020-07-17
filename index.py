from xml2drill import Drill
import xml.etree.ElementTree as ET


def saveToFile(filecontent, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(filecontent)


def get_some_info_from_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root.iter('via'):
        print(child.tag, child.attrib)
    for child in root.iter('hole'):
        print(child.tag, child.attrib)


def main():
    drl = Drill()
    drl.import_from_xml('__.brd')
    drl_text = drl.get_excellon_format('INCH','INCH')
    saveToFile(drl_text,'new_drill.txt')

if __name__ == "__main__":
    main()
