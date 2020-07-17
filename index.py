from xml2drill import Drill
import xml.etree.ElementTree as ET


def saveToFile(filecontent, filename):
    with open(filename, 'w', unicode='utf-8') as f:
        f.write(filecontent)


def main():
    drl = Drill()
    drl.import_from_xml('something_in_xml_not_working_yet')
    print('Output:')
    print(drl.get_excellon_format())
    print(drl.holes_mm)
    print(drl.get_tools_table())
    print(drl.get_tools_text('MM'))
    print(drl.get_tools_text('INCH'))
    print(drl.get_body_text('INCH'))

if __name__ == "__main__":
    main()
