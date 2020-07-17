from drill import Drill
import xml.etree.ElementTree as ET
import sys
import argparse
import os


def saveToFile(filecontent, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(filecontent)


def main(args):
    drl = Drill()
    drl.import_from_xml(args.input_file_brd)
    drl_text = drl.get_excellon_format('INCH', 'INCH')
    saveToFile(drl_text, args.output_file_drill)
    if os.path.isfile(args.output_file_drill):
        print('Total holes found: {}'.format(drl.count_all_holes()))
        print('File saved as: {}'.format(args.output_file_drill))
    else:
        print('ERROR. File not saved ({})'.format(args.output_file_drill))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Export full precision drill excellon file from BRD project file (Eagle XML format)')
    parser.add_argument(
        'input_file_brd',
        help='filename input BRD (Eagle XML format)')
    parser.add_argument(
        'output_file_drill',
        help='filename output excellon drill format')
    parser.add_argument(
        '--header',
        default='INCH',
        nargs='?',
        choices=('INCH', 'MM'),
        help='units in header [INCH/MM]')
    parser.add_argument(
        '--body',
        nargs='?',
        default='INCH',
        choices=('INCH', 'MM'),
        help='units in body [INCH/MM]')
    args = parser.parse_args()

    if os.path.isfile(args.input_file_brd):
        if os.path.isfile(args.output_file_drill):
            answer = input(
                'Output file already exists. Do you realy want to overwrite? [y/n]')
            if answer.upper() != 'Y':
                sys.exit('OK, exiting process.')
    else:
        sys.exit('Not found import file: {}'
                 .format(args.input_file_brd))

    main(args)
