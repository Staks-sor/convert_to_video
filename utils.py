import os
import re
from collections import defaultdict


def collect_image_sequences(directory):
    sequences = defaultdict(list)
    pattern = re.compile(r'^(.*?)(\d+)?\.jpg$')

    # Сбор изображений по каталогам
    for root, dirs, files in os.walk(directory):
        for filename in files:
            match = pattern.match(filename)
            if match:
                sequence_name = match.group(1).strip()
                sequences[sequence_name].append(os.path.join(root, filename))

    return sequences
