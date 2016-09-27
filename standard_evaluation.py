#!/usr/bin/python

import json
import math
import numpy as np

"""
return a tuple with recall, precision, and f1 for one example
credit of this function goes to Xuchen Yao
"""
def computeF1(goldList, predictedList):

  """Assume all questions have at least one answer"""
  if len(goldList)==0:
    raise Exception("gold list may not be empty")
  """If we return an empty list recall is zero and precision is one"""
  if len(predictedList)==0:
    return (0, 1, 0)
  """It is guaranteed now that both lists are not empty"""

  precision = 0
  for entity in predictedList:
    if entity in goldList:
      precision += 1
  precision = float(precision) / len(predictedList)

  recall = 0
  for entity in goldList:
    if entity in predictedList:
      recall += 1
  recall = float(recall) / len(goldList)

  f1 = 0
  if precision + recall > 0:
    f1 = 2 * recall * precision / (precision + recall)
  return (recall, precision, f1)

m = {}
m['qid'] = 0
m['time'] = 1
m['answers'] = 2
m['predictions'] = 3
m['structure'] = 4
m['function'] = 5
m['answer_cardinality'] = 6
m['commonness'] = 7
m['precision'] = 8
m['recall'] = 9
m['f1'] = 10

res_file = 'jacana.res'

"""Go over all lines and compute recall, precision and F1"""
res = []
with open(res_file) as f:
  for line in f:
    if len(line) == 0 or line[0] == '#':
      continue  
							
    tokens = line.split("\t")
    try:
        qid = long(tokens[m['qid']])    
        time = float(tokens[m['time']])
        answers = json.loads(tokens[m['answers']])
        predictions = json.loads(tokens[m['predictions']])
        structure = int(tokens[m['structure']].split(',')[1])
        function = tokens[m['function']]
        answer_cardinality = int(tokens[m['answer_cardinality']])
        commonness = float(tokens[m['commonness']])
    except:
        print line
        continue
    recall, precision, f1 = computeF1(answers, predictions)
    res.append([qid, time, answers, predictions, structure,
                function, answer_cardinality, commonness, 
                precision, recall, f1])

def print_result(options):
    '''
    print the average results over the subset of the questions meeting
    a list of conditions (options). 
    
    An option is a 3-tuple (field, value, operator), e.g., 
    (m['structure'], 1, '==') select questions whose number of edges equals 1.
    
    AND multiple options.
    '''
    averageRecall=0
    averagePrecision=0
    averageF1=0
    count=0
    time = 0
    f1 = []
    for e in res:
        flag = True
        if not len(options) == 0:
            for op in options:
                field = op[0]
                value = op[1]
                operator = op[2]
                if (operator == '==' and e[field] != value) \
                    or (operator == '!=' and e[field] == value) \
                    or (operator == '>' and e[field] <= value) \
                    or (operator == '>=' and e[field] < value) \
                    or (operator == '<' and e[field] >= value) \
                    or (operator == '<=' and e[field] > value):
                        flag = False
        if flag:
            averageRecall += e[m['recall']]
            averagePrecision += e[m['precision']]
            averageF1 += e[m['f1']]
            f1.append(e[m['f1']])
            time += e[m['time']]
            count+=1
    if count != 0:
        print '\t'.join([str(count), str(float(averagePrecision)/count), str(float(averageRecall)/count), \
            str(float(averageF1)/count), str(np.std(f1)), str(float(time)/count)])
    else:
        print '\t'.join(['0.0', '0.0', '0.0', '0.0', '0.0', '0.0'])
        
def print_result_individual(options, fields2print):
    '''print individual question results'''
    for e in res:
        flag = True
        if not len(options) == 0:
            # AND multiple options
            for op in options:
                field = op[0]
                value = op[1]
                operator = op[2]
                if (operator == '==' and e[field] != value) \
                    or (operator == '!=' and e[field] == value) \
                    or (operator == '>' and e[field] <= value) \
                    or (operator == '>=' and e[field] < value) \
                    or (operator == '<' and e[field] >= value) \
                    or (operator == '<=' and e[field] > value):
                        flag = False
        if flag and not len(fields2print) == 0:
            s = ''
            for field in fields2print:
                s += str(e[m[field]]) + '\t'
            print s 
 
#print '------------------overall-------------------'
print('overall performance')
options = []
print_result(options)
#print '------------------structure_nEdge=1-------------------'
print('nEdge = 1')
options = []
options.append([m['structure'], 1, '=='])
print_result(options)
#print '------------------structure_nEdge=2-------------------'
print('nEdge = 2')
options = []
options.append([m['structure'], 2, '=='])
print_result(options)
#print '------------------structure_nEdge=3-------------------'
print('nEdge = 3')
options = []
options.append([m['structure'], 3, '=='])
print_result(options)
#print '------------------function-------------------'
print('function = none')
options = []
options.append([m['function'], 'none', '=='])
print_result(options)
print('function = count')
options = []
options.append([m['function'], 'count', '=='])
print_result(options)
print('function = superlative')
options = []
options.append([m['function'], 'superlative', '=='])
print_result(options)
print('function = comparative')
options = []
options.append([m['function'], 'comparative', '=='])
print_result(options)
#print '------------------answer_cardinality-------------------'
print('answer_card = 1')
options = []
options.append([m['answer_cardinality'], 1, '=='])
print_result(options)
print('answer_card > 1')
options = []
options.append([m['answer_cardinality'], 1, '>'])
print_result(options)
#print '------------------commonness-------------------'
print('-40 <= commonness < -30')
options = []
options.append([m['commonness'], -40, '>='])
options.append([m['commonness'], -30, '<'])
print_result(options)
print('-30 <= commonness < -20')
options = []
options.append([m['commonness'], -30, '>='])
options.append([m['commonness'], -20, '<'])
print_result(options)
print('-20 <= commonness < -10')
options = []
options.append([m['commonness'], -20, '>='])
options.append([m['commonness'], -10, '<'])
print_result(options)
print('-10 <= commonness < 0')
options = []
options.append([m['commonness'], -10, '>='])
options.append([m['commonness'], 0, '<'])
print_result(options)

## paraphrasing analysis
def analyze_paraphrasing():
    pmap = {}
    for e in res:
        qid = e[m['qid']]
        f1 = e[m['f1']]
        tid = qid / 1000000
        if pmap.has_key(tid):
            pmap.get(tid).append(f1)
        else:
            pmap[tid] = [f1]
    n_max = 0
    for key in pmap.keys():
        pmap.get(key).sort(reverse=True)
        if size(pmap.get(key)) > n_max:
            n_max = size(pmap.get(key))
    
    for i in range(0,n_max):
        f1 = 0
        n = 0
        for key in pmap.keys():
            l = pmap.get(key)
            if size(l) > i:
                f1 += l[i]
                n += 1
        if n != 0:
            f1 /= n
        print '\t'.join([str(i), str(n), str(f1)])
        
print('paraphrasing')
analyze_paraphrasing()
