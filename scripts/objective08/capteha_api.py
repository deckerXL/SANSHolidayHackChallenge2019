#!/usr/bin/env python3
# Fridosleigh.com CAPTEHA API - Made by Krampus Hollyfeld / Modified by deckerXL
import requests
import json
import sys
import base64
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import numpy as np
from threading import Thread, enumerate
from datetime import datetime
import queue
import time

yourREALemailAddress = "*****************"

# Optimizations
NUM_PARALLEL_EXEC_UNITS = 6
config = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=NUM_PARALLEL_EXEC_UNITS, inter_op_parallelism_threads=16, allow_soft_placement=True, device_count = {'GPU': 1})

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.compat.v1.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.compat.v1.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def predict_image(q, sess, graph, image_bytes, img_uuid, labels, input_operation, output_operation, img_types):
   
    input_height  = 299
    input_width   = 299
    input_mean    = 0
    input_std     = 255

    image_reader  = tf.image.decode_png( image_bytes, channels=3, name="png_reader")
    float_caster  = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized       = tf.compat.v1.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized    = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess_image    = tf.compat.v1.Session(config=config)
    image         = sess_image.run(normalized)

    results       = sess.run(output_operation.outputs[0], { input_operation.outputs[0]: image })
    results       = np.squeeze(results)
    prediction    = results.argsort()[-5:][::-1][0]

    str_pred = str(labels[prediction].title())
    if str_pred in img_types:
        print ("\t+++++++++++++ Queue put:"+img_uuid+"-- Prediction:"+str(labels[prediction].title())+"-- Precent:"+str(results[prediction]))
        q.put(img_uuid)
        
def main():

    # Loop until we get the captcha in under 10 seconds
    success = False
    attempts = 1
    while not success and attempts<=25:

        print ("********************")
        print ("***** Starting *****")
        print ("********************\n")
        
        tf.compat.v1.disable_eager_execution()
        final_answer = ""

        # Loading the Trained Machine Learning Model created from running retrain.py on the training_images directory
        graph  = load_graph('C:\\HHC\\Objective8\\retrain_tmp\\output_graph.pb')
        labels = load_labels('C:\\HHC\\Objective8\\\\retrain_tmp\\output_labels.txt')

        # Load up our session
        input_operation  = graph.get_operation_by_name("import/Placeholder")
        output_operation = graph.get_operation_by_name("import/final_result")
        sess = tf.compat.v1.Session(graph=graph,config=config)

        # Creating a session to handle cookies
        s = requests.Session()
        url = "https://fridosleigh.com/"

        print ("Sending Request to: ["+url+"]...")
        json_resp = json.loads(s.get("{}api/capteha/request".format(url)).text)

        b64_images = json_resp['images'] # A list of dictionaries eaching containing the keys 'base64' and 'uuid'
        challenge_image_type = json_resp['select_type'].split(',') # The Image types the CAPTEHA Challenge is looking for.
        case1 = challenge_image_type[0].strip()
        case2 = challenge_image_type[1].strip()
        case3 = challenge_image_type[2].replace(' and ','').strip()
        challenge_image_types = [case1, case2, case3] # cleaning and formatting

        print ("Determined the following challenge image types: ["+str(challenge_image_types)+"]...\n")
      
        threads = []
        q = queue.Queue()

        # Start timestamp
        dateTimeObj1 = datetime.now()	
        print("Starting tensorflow analysis at timestamp: ["+str(dateTimeObj1)+"]")
    
        for i in range(len(b64_images)):
            for j in b64_images[i]:          
                if j == "base64":
                    img_uuid = b64_images[i]['uuid']

                    #predict_image function is expecting png image bytes so we read image as 'rb' to get a bytes object
                    image_bytes = base64.b64decode(b64_images[i][j])
                    t = Thread(target=predict_image, args=(q, sess, graph, image_bytes, img_uuid, labels, input_operation, output_operation, challenge_image_types),daemon=True)
                    threads.append(t)

        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

        # Getting a list of all threads returned results
        dateTimeObj2 = datetime.now()
        print("Completed tensorflow analysis in: ["+str(dateTimeObj2-dateTimeObj1)+"] time\n")

        # Create the final comma delimited list of image uuids to send to the server
        final_answer = ','.join( list(q.queue) )
  
        # This should be JUST a csv list image uuids ML predicted to match the challenge_image_type .
        json_resp = json.loads(s.post("{}api/capteha/submit".format(url), data={'answer':final_answer}).text)

        success = True
        if not json_resp['request']:
            # If it fails just run again. ML might get one wrong occasionally
            print('FAILED MACHINE LEARNING GUESS')
            print('--------------------\nOur ML Guess:\n--------------------\n{}'.format(final_answer))
            print('--------------------\nServer Response:\n--------------------\n{}'.format(json_resp['data']))
            success = False
            attempts = attempts + 1

            # Clear variables for next loop iteration
            del final_answer, q, threads, b64_images

            print ("\n====================================================================================================\n")

        # End While Loop
        
    print("CAPTEHA Solved on attempt ["+str(attempts)+"]!")

    # =============================================================================================
    # Submit for Drawing
    # =============================================================================================

    # If we get to here, we are successful and can submit a bunch of entries till we win
    userinfo = {
        'name':'Krampus Hollyfeld',
        'email':yourREALemailAddress,
        'age':180,
        'about':"Cause they're so flippin yummy!",
        'favorites':'thickmints'
    }
    # If we win the once-per minute drawing, it will tell us we were emailed. 
    # Should be no more than 200 times before we win. If more, somethings wrong.
    entry_response = ''
    entry_count = 1
    while yourREALemailAddress not in entry_response and entry_count < 200:
        print('Submitting lots of entries until we win the contest! Entry #{}'.format(entry_count))
        entry_response = s.post("{}api/entry".format(url), data=userinfo).text
        entry_count += 1
    print(entry_response)

if __name__ == "__main__":
    main()
