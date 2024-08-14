# -*- coding：utf-8 -*-
import json
import sklearn
import tqdm
from bert_serving.client import BertClient
import argparse
import os
import numpy as np
import sklearn.metrics as metrics
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import random

def convert_text_to_datapoint(datapath,output_path,bc,prefix='CD'):
    total_example = []
    writer = open(os.path.join(output_path,prefix,"train_datapoint.json"),'w+',encoding='utf-8')
    with open(datapath, 'r', encoding='utf-8') as fin:
        lines = fin.readlines()
    for line in tqdm.tqdm(lines,desc="reading!"):
        data_raw = json.loads(line.strip('\n'))
        chief_complaint = data_raw['chief_complaint']
        description = data_raw['description']
        norm_syndrome = data_raw['norm_syndrome']
        if prefix=="CD":
            statement = chief_complaint+' [SEP] '+description
        elif prefix=="C":
            statement = chief_complaint
        total_example.append(statement)
    # print(len(total_example))
    batch_size =32
    chunk_example = [total_example[i:i+batch_size] for i in range(0,len(total_example),batch_size)]

    for b_example in tqdm.tqdm(chunk_example,desc="convert text to datapoint"):
        batch_encoded_example = bc.encode(b_example).tolist()
        for i in batch_encoded_example:
            writer.write(json.dumps(i))
            writer.write('\n')

    return None

def read_label(path_labellist = "syndrome_vocab.txt"):
    labels = []
    with open(path_labellist, 'r', encoding='utf-8') as f:
        for line in f:
            labels.append(line.strip('\n'))
    label_map = {label: i for i, label in enumerate(labels)}
    return label_map

def read_examples_labels(label_map,path_ex):
    with open(path_ex,'r',encoding='utf-8') as label_ex:
        labels_lines = label_ex.readlines()
    y_label = []
    for line in labels_lines:
        data_raw = json.loads(line.strip('\n'))
        norm_syndrome = data_raw['norm_syndrome']
        label = label_map[norm_syndrome]
        y_label.append(label)
    return y_label

def read_datapoints(path_datapoint):
    with open(path_datapoint,'r') as datapoint:
        lines=datapoint.readlines()
    x_input =[ json.loads(i.strip('\n')) for i in lines]

    return x_input




if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--datapath", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--output_path", default=None, type=str, required=True,
                        help="The output directory where the model predictions and checkpoints will be written.")
    parser.add_argument("--prefix", default=None, type=str, required=False,
                        help="The output directory where the model predictions and checkpoints will be written.")

    # args = parser.parse_args()
    # if not os.path.exists(os.path.join(args.output_path,args.prefix)):
    #     os.makedirs(os.path.join(args.output_path,args.prefix))
    # bc = BertClient()
    # convert_text_to_datapoint(args.datapath,args.output_path,bc,args.prefix)

    labels_map =read_label()
    train_label= read_examples_labels(labels_map)
    train_input = read_datapoints()
    dev_label = read_examples_labels(labels_map,"path_to_dev")
    dev_input = read_datapoints("path_to_dev")

    test_label = read_examples_labels(labels_map, "path_to_test")
    test_input = read_datapoints("path_to_test")

    print("buidling SVM")
    clf = make_pipeline(StandardScaler(), SVC(gamma='auto',decision_function_shape='ovo'))
    clf.fit(train_input,train_label)
    print("predicting dev")
    dev_pred = clf.predict([i for i in dev_input])
    dev_report = metrics.classification_report(dev_label,dev_pred,output_dict= True)
    print("predicting test")
    test_pred = clf.predict([i for i in test_input])
    test_report = metrics.classification_report(test_label,test_pred,output_dict= True)

    from sklearn import tree
    clf_dt = tree.DecisionTreeClassifier()
    clf_dt = clf_dt.fit(train_input,train_label)