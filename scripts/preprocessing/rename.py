""" usage: partition_dataset.py [-h] [-i INPUTDIR] [-o OUTPUTDIR]

Rename json files in a folder in an ordered way

optional arguments:
    -h, --help            show this help message and exit
    -i INPUTDIR, --inputDIR INPUTDIR
                            Path to the folder where the json file is stored. If not specified, the CWD will be used.

    -o OUTPUTDIR, --outputDir OUTPUTDIR
                            Path to the new dirs should be created. Defaults to the same directory as IMAGEDIR.
"""

import os
import re
import argparse

def iterate_dir(source, dest):
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')

    if not os.path.exists(dest):
        os.makedirs(dest)
        
    images = [f for f in os.listdir(source)
              if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.json)$', f)]

    for filename in images:
        splitted = filename.split(".")
        new_filename = splitted[0] + ".json"
        os.rename(os.path.join(source, filename), os.path.join(dest, new_filename))

def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Rename Json Files",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--inputDir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to where the new directory should be created. '
             'Defaults to the same directory as OUTPUTDIR.',
        type=str,
        default=None
    )

    args = parser.parse_args()

    if args.outputDir is None:
        args.outputDir = args.imageDir

    # Now we are ready to start the iteration
    iterate_dir(args.inputDir, args.outputDir)


if __name__ == '__main__':
    main()