from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import math
import os

import tensorflow as tf

from medium_show_and_tell_caption_generator.caption_generator import CaptionGenerator
from medium_show_and_tell_caption_generator.model import ShowAndTellModel
from medium_show_and_tell_caption_generator.vocabulary import Vocabulary

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string("model_path", "", "Model graph def path")
tf.flags.DEFINE_string("vocab_file", "", "Text file containing the vocabulary.")
# tf.flags.DEFINE_string("input_files", "",
#                        "File pattern or comma-separated list of file patterns "
#                        "of image files.")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))

from flask import Flask
from flask import request
from flask import jsonify
from urllib.request import urlopen
import urllib
import string
import tempfile

app = Flask(__name__)
model = None
vocab = None
generator = None

@app.route("/", methods=['GET', 'POST'])
def main_index():
    url = None
    file = None
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
    else:
        url = request.args.get('url')
        url = urllib.parse.quote(url, safe=string.printable)
        logger.info('url: %s', url)
        with tempfile.NamedTemporaryFile(delete=True) as img_file:
            req = urllib.request.urlopen(url)
            img_file.write(req.read())
            img_file.flush()
            with tf.gfile.GFile(img_file.name, "rb") as f:
                file = f.read()
    if file:
        captions = generator.beam_search(file)
        results = []
        for i, caption in enumerate(captions):
            # Ignore begin and end tokens <S> and </S>.
            sentence = [vocab.id_to_token(w) for w in caption.sentence[1:-1]]
            sentence = " ".join(sentence)
            # print("  %d) %s (p=%f)" % (i, sentence, math.exp(caption.logprob)))
            results.append({ 
                'i' : i,
                'sentence' : sentence, 
                'logprob' : math.exp(caption.logprob)
            })
        return jsonify(results)

    else:
        return 'No file provided', 400

if __name__ == "__main__":
    model_path = os.path.join(current_dir, "../etc/show-and-tell.pb") #FLAGS.model_path
    vocab_file = os.path.join(current_dir, "../etc/word_counts.txt") #FLAGS.model_path
    model = ShowAndTellModel(model_path)
    vocab = Vocabulary(vocab_file)

    generator = CaptionGenerator(model, vocab)
    # tf.app.run()
    app.run(host='0.0.0.0')