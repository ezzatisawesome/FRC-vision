""" usage: partition_dataset.py [-h] [-i IMAGEDIR] [-o OUTPUTDIR] [-r RATIO] [-t]

Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTDIR, --inputDir INPUTDIR
                        Path to the folder where the json and image datasets are stored. If not specified, the CWD will be used.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output folder where the .record output will be writte/created. 
"""

import os
import io
import re
import json
import numpy as np
import argparse
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'Power_Cell':
        return 1
    else:
        None


def iterate_dir(source, dest):
    writer = tf.io.TFRecordWriter(dest)

    images = [f for f in os.listdir(source)
                if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.json)$', f)]

    for filename in images:
        tf_example = create_tf_example(os.path.join(source, filename))
        writer.write(tf_example.SerializeToString())

    writer.close()

    output_path = os.path.join(os.getcwd(), dest)
    print('Successfully created the TFRecords: {}'.format(output_path))


def create_tf_example(source):
    
    image_source = source.split('.')[0]+".jpeg"
    #print(image_source)
    encoded_jpg = open(image_source, 'rb').read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)

    split_url = source.split('.')

    json_url = split_url[0] + '.json'
    json_file = open(os.path.join(json_url))
    data = json.load(json_file)

    filename = source.encode('utf8')
    filetype = '{}'.format(split_url[1])
    image_format = b'jpeg'

    height = data['size']['height']
    width = data['size']['width']

    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []
    
    objects = data['objects']
    for obj in objects:
        
        xmin = obj['points']['exterior'][0][0] / width
        xmax = obj['points']['exterior'][1][0] / width
        ymin = obj['points']['exterior'][0][1] / width
        ymax = obj['points']['exterior'][1][1] / width
        if xmin < 0.0:
            xmin = 0.0
        elif xmin > 1.0:
            xmin = 1.0

        if xmax < 0.0:
            xmax = 0.0
        elif xmax > 1.0:
            xmax = 1.0

        if ymin < 0.0:
            ymin = 0.0
        elif ymin > 1.0:
            ymin = 1.0

        if ymax < 0.0:
            ymax = 0.0
        elif ymax > 1.0:
            ymax = 1.0
        
        xmins.append(xmin)
        xmaxs.append(xmax)
        ymins.append(ymin)
        ymaxs.append(ymax)
    
        classes_text.append(obj['classTitle'].encode('utf8'))
        classes.append(class_text_to_int(obj['classTitle']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes)
    }))

    return tf_example


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Partition dataset of images into training and testing sets",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--inputDir',
        help='Path to the folder where the json and image datasets are stored. If not specified, the CWD will be used.',
        type=str,
        default=os.getcwd()
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the .record output will be writte/created. ',
        type=str,
        default=None
    )
    args = parser.parse_args()

    # Now we are ready to start the iteration
    iterate_dir(args.inputDir, args.outputDir)


if __name__ == '__main__':
    main()