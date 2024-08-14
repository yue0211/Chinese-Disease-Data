# -*- coding：utf-8 -*-

from __future__ import absolute_import, division, print_function


import logging
import os
import sys
from io import open
import json
import copy
import csv
import glob
import tqdm
from typing import List
from transformers import PreTrainedTokenizer
import sklearn.metrics as metrics
logger = logging.getLogger(__name__)
import xlrd
import random

def read_knowledge_base(pathtoknowledge="E:\Project-TCM\TCM\data_preprocess\\v2_tcm.xlsx"):
    wb = xlrd.open_workbook(filename=pathtoknowledge)
    sheet_1 = wb.sheet_by_name("Sheet1")
    instances = []
    # all_description=[]
    for line_no in range(1,2139):
        Name = sheet_1.cell(line_no, 4).value
        Definition = sheet_1.cell(line_no, 5).value
        # Definition = sheet_1.cell(line_no, 5).value.replace(Name,'').replace("中医病证名","").replace("中医病名",'').replace("，。",'').replace("，，",'')
        Typical_performance = sheet_1.cell(line_no, 6).value
        Common_isease  =sheet_1.cell(line_no, 7).value

        instance = {
            "Name":Name,
            "Definition": Definition,
            "Typical_performance": Typical_performance,
            "Common_isease": Common_isease,
        }

        instances.append(instance)
    unique_instances = [dict(t) for t in {tuple(d.items()) for d in instances}]
    kb_in_dict={}
    for syndrome in unique_instances:
        kb_in_dict[syndrome['Name']]=syndrome
    return kb_in_dict

class InputExample(object):
    """A single training/test example"""
    def __init__(self, user_id, chief_complaint, history, detection, syndrome_name, knowledge_para = None,knowledge =None,syndrome_label=None):
        '''
        :param user_id: 用户的ID
        :param chief_complaint:      主诉        `
        :param history:  病史
        :param detection: 四诊
        :param syndrome_name: 证名
        :param syndrome_label: 证对应的序号
        '''
        self.user_id = user_id
        self.chief_complaint = chief_complaint
        self.history = history
        self.detection = detection
        self.syndrome_name = syndrome_name
        self.knowledge =knowledge
        self.knowledge_para = knowledge_para
        self.syndrome_label = syndrome_label


class InputFeatures(object):
    """

    """

    def __init__(self, input_ids, attention_mask=None, token_type_ids=None, label=None):
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.token_type_ids = token_type_ids
        self.label = label

    def __repr__(self):
        return str(self.to_json_string())

    def to_dict(self):
        """Serializes this instance to a Python dictionary."""
        output = copy.deepcopy(self.__dict__)
        return output

    def to_json_string(self):
        """Serializes this instance to a JSON string."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"



class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir,args=None):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir,args=None):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_test_examples(self, data_dir,args=None):
        """Gets a collection of `InputExample`s for the test set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()



class TcmProcessor(DataProcessor):
    """Processor for the TCM data set."""

    def get_train_examples(self, data_dir,args=None):
        """See base class."""

        logger.info("LOOKING AT {} train".format(data_dir))
        return self._create_examples(self._read_json(os.path.join(data_dir, "train_v3_knowledge_tfidf_3k_shuffle.json")),self._get_kb(data_dir),args.no_knowledge)


    def get_dev_examples(self, data_dir,args=None):
        """See base class."""
        logger.info("LOOKING AT {} dev".format(data_dir))
        return self._create_examples(self._read_json(os.path.join(data_dir, "dev_v3_knowledge_tfidf_3k.json")),self._get_kb(data_dir),args.no_knowledge)

    def get_test_examples(self, data_dir, args=None):
        """See base class."""
        logger.info("LOOKING AT {} dev".format(data_dir))
        return self._create_examples(self._read_json(os.path.join(data_dir, "test_v3_knowledge_tfidf_3k.json")),self._get_kb(data_dir),args.no_knowledge)

    def get_labels(self):
        """See base class."""
        labels = []
        # /home/mcren/TCM/data_preprocess/syndrome_vocab.txt
        # E:\Project-TCM\TCM\data_preprocess\syndrome_vocab.txt
        with open("/home/mcren/TCM/data_preprocess/syndrome_vocab.txt", 'r',encoding='utf-8') as f:
            for line in f:
                labels.append(line.strip('\n'))
        return labels

    def _get_kb(selfs,data_dir):
        kb = read_knowledge_base(os.path.join(data_dir,"v2_tcm.xlsx"))
        return kb
    def _read_json(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as fin:
            lines = fin.readlines()
            return lines

    def _create_examples(self, lines,kb,k=3):
        """Creates examples for the training and dev sets."""
        examples = []
        knowledge_examples={}
        labels = self.get_labels()
        for line in lines:
            # initialize current valid knowledge

            data_raw = json.loads(line.strip('\n'))
            user_id = data_raw['user_id']
            lcd_id = data_raw['lcd_id']
            lcd_name = data_raw['lcd_name']
            syndrome = data_raw['syndrome']
            chief_complaint = data_raw['chief_complaint']
            description = data_raw['description']
            detection  = data_raw['detection']
            norm_syndrome = data_raw['norm_syndrome']

            try:
                knowledge_para = data_raw['knowledge_para']
                try:
                    external_knowledge = kb[norm_syndrome]['Definition']
                except:
                    external_knowledge = ""
            except:
                print("WARNING~ finding knowledge for %s" % norm_syndrome)
                all_knowledge_definition=[kb[l]['Definition'] for l in labels if l in kb.keys()]
                all_knowledge_definition_syndrome = [l for l in labels if l in kb.keys()]
                try:
                    external_knowledge = kb[norm_syndrome]['Definition']
                    index_current_syndrome = all_knowledge_definition_syndrome.index(norm_syndrome)
                    del all_knowledge_definition[index_current_syndrome]
                    knowledge_para_sentences = random.sample(all_knowledge_definition, k)
                    knowledge_para_sentences.extend([external_knowledge])

                except:
                    external_knowledge = ""
                    knowledge_para_sentences = random.sample(all_knowledge_definition, k)
                    print("WARNING~No valid knowledge for %s" % norm_syndrome)
                    # print(knowledge_para_sentences)

                random.shuffle(knowledge_para_sentences)
                knowledge_para = ' '.join(knowledge_para_sentences)

            # print(len(all_knowledge_definition))


            examples.append(InputExample(
                user_id=user_id,
                chief_complaint=chief_complaint,
                history=description,
                detection= detection,
                syndrome_name= norm_syndrome,
                syndrome_label= norm_syndrome,
                knowledge= external_knowledge,
                knowledge_para = knowledge_para,
            ))

        # if knowledge_as_example:
        #     u_id =1000000
        #     for k,v in knowledge_examples.items():
        #         # print(v)
        #         examples.append(InputExample(
        #             user_id=u_id,
        #             chief_complaint=v[k]['Typical_performance'],
        #             history=v[k]['Definition'],
        #             detection=v[k]['Typical_performance'],
        #             syndrome_name=k,
        #             syndrome_label=k,
        #             knowledge=v[k]['Definition'],
        #         ))
        #         u_id+=1

        return examples


def tcm_convert_examples_to_features(examples, tokenizer,
                                      max_length=512,
                                      label_list=None,
                                      pad_on_left=False,
                                      pad_token=0,
                                      pad_token_segment_id=0,
                                      mask_padding_with_zero=True,
                                      differentiation_element = None,
                                      do_train= False,
                                      has_knowledge= False,

                                     ):
    """
    :param examples:
    :param tokenizer:
    :param max_length:
    :param label_list:
    :param pad_on_left:
    :param pad_token:
    :param pad_token_segment_id:
    :param mask_padding_with_zero:
    :return:

    """
    processor = TcmProcessor()
    label_map = {label: i for i, label in enumerate(label_list)}
    features = []
    for (ex_index, example) in tqdm.tqdm(enumerate(examples), desc="convert examples to features"):
    # for (ex_index, example) in enumerate(examples):
        if ex_index % 10000 == 0:
            logger.info("Writing example %d" % (ex_index))
        if  has_knowledge :
            if differentiation_element == "full":
                inputs = tokenizer.encode_plus(
                    text=example.knowledge_para,
                    text_pair= example.chief_complaint+'[SEP]'+example.history,
                    add_special_tokens=True,
                    max_length=max_length,
                    # truncation_strategy="only_first"
                )
            elif differentiation_element == "history":
                inputs = tokenizer.encode_plus(
                    text=example.knowledge_para,
                    text_pair= example.history,
                    add_special_tokens=True,
                    max_length=max_length,
                    # truncation_strategy="only_first"
                )
            elif differentiation_element == "chief_complaint":
                inputs = tokenizer.encode_plus(
                    text=example.knowledge_para,
                    text_pair= example.chief_complaint,
                    add_special_tokens=True,
                    max_length=max_length,
                    # truncation_strategy="only_first"
                )

        else:
            if differentiation_element == "full" :
                inputs = tokenizer.encode_plus(
                    text=example.chief_complaint,
                    text_pair=example.history,
                    add_special_tokens=True,
                    max_length=max_length,
                )
            elif differentiation_element == "history":
                inputs = tokenizer.encode_plus(
                    text= example.history,
                    text_pair=None,
                    add_special_tokens=True,
                    max_length=max_length,
                )
            elif differentiation_element == "chief_complaint":
                inputs = tokenizer.encode_plus(
                    text=example.chief_complaint,
                    text_pair=None,
                    add_special_tokens=True,
                    max_length=max_length,
                )
        input_ids, token_type_ids = inputs["input_ids"], inputs["token_type_ids"]

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        attention_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)
        # Zero-pad up to the sequence length.
        padding_length = max_length - len(input_ids)

        if pad_on_left:
            input_ids = ([pad_token] * padding_length) + input_ids
            attention_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + attention_mask
            token_type_ids = ([pad_token_segment_id] * padding_length) + token_type_ids
        else:
            input_ids = input_ids + ([pad_token] * padding_length)
            attention_mask = attention_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
            token_type_ids = token_type_ids + ([pad_token_segment_id] * padding_length)

        assert len(input_ids) == max_length, "Error with input length {} vs {}".format(len(input_ids), max_length)
        assert len(attention_mask) == max_length, "Error with input length {} vs {}".format(len(attention_mask), max_length)
        assert len(token_type_ids) == max_length, "Error with input length {} vs {}".format(len(token_type_ids), max_length)

        label = label_map[example.syndrome_label]


        if ex_index < 5:
            logger.info("*** Example ***")
            logger.info("guid: %s" % (example.user_id))
            logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            logger.info('input_tokens: %s' % " ".join([str(x) for x in tokenizer.convert_ids_to_tokens(input_ids)]))
            logger.info("attention_mask: %s" % " ".join([str(x) for x in attention_mask]))
            logger.info("token_type_ids: %s" % " ".join([str(x) for x in token_type_ids]))
            logger.info("label: %s (id = %d)" % (example.syndrome_label, label))

        features.append(
                InputFeatures(input_ids=input_ids,
                              attention_mask=attention_mask,
                              token_type_ids=token_type_ids,
                              label=label))

    return features

def shuffle_sentence(text_a, text_b=None):
    text_a_sents = text_a.split('，')
    text_b_sents = text_b.split('，') if text_b else []
    final_sentence = text_a_sents+text_b_sents
    random.shuffle(final_sentence)
    return '，'.join(final_sentence)

# def compute_metrics_for_multiclass_tcm(labels,prediction):
#     '''
#     The function used for computing full metrics
#     :param labels:  a series of golden label
#     :param prediction:  an array prediction scores.
#     :return:
#         1. basic Accuracy, Recall, Precison
#         2. balanced Accuracy
#         3. Top K Accuracy
#         4. F1, F1-micro, F1-macro
#         5. Roc_Auc
#         6. MCC, Cohen K
#     '''
#     def

def store_preds_labels(out_path,labels,predicts):
    writer = open(os.path.join(out_path,"predict_array.txt"),'w+',encoding='utf-8')
    out = {
        "labels":labels,
        "predicts":predicts,
    }
    writer.write(json.dumps(out))
    writer.close()
    return None

path ="E:\Project-TCM\TCM\predict_array.txt"
def read_pred_files(path):
    import numpy as np
    with open(path,'r') as f:
        a = f.readline()
    b = json.loads(a)
    y_true = b['labels']
    y_pred =y_pred = np.argmax(b['predicts'],1).tolist()

    print("acc:",metrics.accuracy_score(y_true,y_pred))
    print("balanced_acc:",metrics.balanced_accuracy_score(y_true,y_pred))
    print("f1-micro %f \n Recall %f \n Precison %f" % (metrics.f1_score(y_true,y_pred,average='micro'),metrics.recall_score(y_true,y_pred,average='micro'),metrics.precision_score(y_true,y_pred,average='micro')))

    print("f1-macro %f \n Recall %f \n Precison %f" % (metrics.f1_score(y_true,y_pred,average='macro'),metrics.recall_score(y_true,y_pred,average='macro'),metrics.precision_score(y_true,y_pred,average='macro')))
    # print("f1-macro:", metrics.f1_score(y_true, y_pred, average='macro'))
    r = metrics.classification_report(y_true, y_pred, output_dict=True)