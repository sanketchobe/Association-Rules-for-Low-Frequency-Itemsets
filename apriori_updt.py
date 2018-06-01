# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:11:41 2017

@author: Sanketchobe
"""

import math
import argparse
from itertools import chain, combinations
from datetime import datetime


def joinset1(itemset,c_itemset, k):
    return set([i.union(j) for i in itemset for j in c_itemset if len(i.union(j)) == k])

def joinset2(itemset, c_itemset, k):
    return set([i.union(j) for i in itemset for j in c_itemset if len(i.union(j)) == k])


def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])
    

def itemset_from_data(data):
    print "In itemset_from_data\n"
    itemset = set()
    transaction_list = list()
    for row in data:
        transaction_list.append(frozenset(row))
 #       transaction_list.append(row)
        for item in row:
            if item:
                itemset.add(frozenset([item]))
#               itemset.add(item)
#    print "itemset:\n", itemset,"& transaction:\n", transaction_list
    return itemset, transaction_list


def itemset_from_utility(data, utility):
    print "In itemset_from_utility\n"
    utility_item = dict()
    trans_list = list()
    utility_list = list()
    item_util = dict()
    item_util_list = list()
    save_k = list()
    i = 0
    j = 0
    c = 0
    d = 1
 #   utrowcount = 0
    for row in data:
        trans_list.append(row)
    #print "Trans list:", trans_list
    for utrow in utility:
        utility_list.append(utrow)  
   # print "utility list:", utility_list
 #   for i in range(len(utility_list)):
 #       utility_item = dict(zip(trans_list[i], utility_list[i]))

    for trans in trans_list:
        i = i + 1
        for utlist in utility_list:
            j = j + 1
            if i == j:
         #       print "Trans:",i,"value:",trans
          #      print "Utlist:",j,"value:",utlist 
     #           item_util[trans] = utlist
                item_util_list.append((trans, utlist))
                for l in range(len(trans)):
    #                item_util[trans[l]] = utlist[l]
                    if trans[l] and utlist[l] and c > 0:
 #                       print "save_k:", save_k
                        if trans[l] in save_k:
#                        for k in save_k:
#                            print "key", k, "& item:", trans[l] 
#                            print "utility_item:", utility_item                         
#                            if trans[l] == k:
  #                          print "key", trans[l], "utility_item:", utility_item[trans[l]],"utlist_itm:",utlist[l]
#                utility_item = dict(zip(trans, utlist))
                            utility_item[trans[l]] = int(utility_item[trans[l]]) + int(utlist[l])
      #                      break
                        else:
                            if trans[l] not in save_k:
                                utility_item[trans[l]] = utlist[l]
                                save_k.append(trans[l])
      #                          break
                    else:
                        utility_item[trans[l]] = utlist[l]
                        save_k.append(trans[l])
                        c = c + 1
  #              item_util_list.append(item_util)
                item_util = dict()
 #               d = 1
        j = 0
    i = 0   
#    for utitem, utvalue in utility:
#            for utlist in utility:
#                for utvalue in utlist:
#                utility_item[item] = utlist 
    return utility_list, item_util_list, utility_item
    

def itemset_support(transaction_list, itemset, item_utility, util_thresh, min_support):
    print "In itemset_support\n"
    len_transaction_list = len(transaction_list)
    l = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row)))/len_transaction_list) 
  #       (item, float(sum(1 for row in transaction_list if item in row))/len_transaction_list) 
        for item in itemset
    ]
    return dict([(item, support) for item, support in l if support >= min_support])
# Find Support values to find infrequent itemsets...
def infrqnt_support(transaction_list, c_itemset, item_utility, util_thresh, min_support):
    print "In infrqnt_support\n"
    s = 0
    util = 0
    l = list()
    len_transaction_list = len(transaction_list)
    for item in c_itemset:
        for row in transaction_list:
            if item.issubset(row):
#                print "item:", item, "row:", row
                s = s + 1
#        print "item:", item, "s:", s
        if s > 500:
            supp = (float(s) / float(len_transaction_list))
            for itm in item:
                if itm in item_utility:
#                    print "item:", itm,"utility:", item_utility[itm]
                    util = util + int(item_utility[itm])
            if supp > 0.0 and supp < min_support:
 #           print "item:", item,"util:", util
                if util > util_thresh:
                    l.append((item,supp))
            s = 0
            util = 0
 #   print "l:",l
        
 #   l = [
#        (item, float(sum(1 for row in transaction_list if item.issubset(row)))/len_transaction_list) 
  #       (item, float(sum(x1 for row in transaction_list if item in row))/len_transaction_list) 
 #       for item in itemset
 #   ]
  #  print "l:", l
#    return l
    return dict([(item, support) for item, support in l if (support < min_support and support > 0.0)])



def freq_itemset(transaction_list, c_itemset, item_utility, util_thresh, min_support):
    print "In freq_support\n"
    f_itemset = dict()

    k = 1
    while True:
        if k > 1:
            c_itemset = joinset1(c_itemset, l_itemset, k)
        l_itemset = itemset_support(transaction_list, c_itemset, item_utility, util_thresh, min_support)
        if not l_itemset or k > 3:
            break
        f_itemset.update(l_itemset)
        k += 1

    return f_itemset   
    
# Find Infrequent itemsets...
def infreq_itemset(transaction_list, c_itemset, item_utility, util_thresh, min_support):
    print "In infreq_itemset\n"
    lf_itemset = dict()

    k = 1
    while True:
        if k > 1:
            c_itemset = joinset2(c_itemset, l_itemset, k)
 #           print "join itemset:", c_itemset
        l_itemset = infrqnt_support(transaction_list, c_itemset, item_utility, util_thresh, min_support)
        if not l_itemset or k > 3:
            break
        lf_itemset.update(l_itemset)
        k += 1
        
    return lf_itemset 

#Find High Utility High Frequency Itemsets...
def hfhu_itemset(transaction_list, hf_itemset, item_utility, item_util_list, min_util):
    print "In hfhu_itemset\n"
    hfhu_itemset = dict()
    util=0 
    prev_util = 0
    i = 0
    
    l = [
        (item, int(sum(1 for row in transaction_list if item.issubset(row))))
  #       (item, int(sum(1 for row in transaction_list if item in row)) * item_utility[item])
        for item in hf_itemset
        ]
#========================================================================================================
 #   print "itemset with frequency:", l
 #   for key, value in l:
 #       util = 0
 #       for itm in key:
 #    #       print "key", key," and frequency:", value
 #           print "key item:", itm,"& utility of item", item_utility[itm]
  #          util = util + (int(value) * int(item_utility[itm]))
 #           util = util + (int(item_utility[itm]))
    #    print "utility:", util
 #       hfhu_itemset[key] = util
 #========================================================================================================
 
    for key, value in l:
        util = 0
        for trans, ut in item_util_list:
            for itm in key:
            #         print "key", key," and frequency:", value
   #         print "key item:", itm,"& utility of item", item_utility[itm]
   #         util = util + (int(value) * int(item_utility[itm]))
                 if itm in trans:
                     i = i + 1
                     util = util + (int(ut[trans.index(itm)]))
             #        print "trans:", trans," key:", key," item:", itm,"util:", util
                 else:
                     i = 0
                     util = 0
                     break
          #  print "i:", i, "itm:", itm
            if i > 0:
          #      print "Transaction:", trans,"itemset:", key,"utility:", util
                hfhu_itemset[key] = prev_util + util
                prev_util = util
            else:
                util = 0
                prev_util = 0
        i = 0
  #  print "key:", key,"utility:", util
    return dict([(item, ut) for item, ut in hfhu_itemset.items() if ut >= min_util])
#     return hufh_itemset
#Find High Utility Itemsets...
def hflu_itemset(transaction_list, hf_itemset, item_utility, item_util_list, min_util):
    print "In hflu_itemset\n"
    hflu_itemset = dict()
    util=0 
    i = 0
    prev_util = 0
                
    l = [
        (item, int(sum(1 for row in transaction_list if item.issubset(row))))
  #       (item, int(sum(1 for row in transaction_list if item in row)) * item_utility[item])
        for item in hf_itemset
        ]
    for key, value in l:
        util = 0
        for trans, ut in item_util_list:
            for itm in key:
            #         print "key", key," and frequency:", value
   #         print "key item:", itm,"& utility of item", item_utility[itm]
   #         util = util + (int(value) * int(item_utility[itm]))
                 if itm in trans:
                     i = i + 1
                     util = util + (int(ut[trans.index(itm)]))
       #              print "trans:", trans," key:", key," item:", itm,"util:", util
                 else:
                     i = 0
                     util = 0
                     break
      #      print "i:", i, "itm:", itm
            if i > 0:
       #         print "Transaction:", trans,"itemset:", key,"utility:", util
                hflu_itemset[key] = prev_util + util
                prev_util = util
            else:
                util = 0
                prev_util = 0
        i = 0
   # print "key:", key,"utility:", util
#=====================================================================================================
#    print "itemset with frequency:", l
 #   for key, value in l:
 #       util = 0
 #       for itm in key:
   #         print "key", key," and frequency:", value
   #         print "key item:", itm,"& utility of item", item_utility[itm]
   #         util = util + (int(value) * int(item_utility[itm]))
   #          util = util + (int(item_utility[itm]))
 ##       print "utility:", util
    #    hflu_itemset[key] = util
#======================================================================================================
    
    return dict([(item, ut) for item, ut in hflu_itemset.items() if ut < min_util])
    
#Find Low Frequency High Utility Itemsets...
def lfhu_itemset(transaction_list, lf_itemset, item_utility, item_util_list, min_util):
   print "In lfhu_itemset\n"
   lfhu_itemset = dict()
   i = 0
   prev_util = 0
                
   l = [
        (item, int(sum(1 for row in transaction_list if item.issubset(row))))
  #       (item, int(sum(1 for row in transaction_list if item in row)) * item_utility[item])
        for item in lf_itemset
        ]
        
   for key, value in l:
        util = 0
        for trans, ut in item_util_list:
            for itm in key:
            #         print "key", key," and frequency:", value
   #         print "key item:", itm,"& utility of item", item_utility[itm]
   #         util = util + (int(value) * int(item_utility[itm]))
                 if itm in trans:
                     i = i + 1
                     util = util + (int(ut[trans.index(itm)]))
         #            print "trans:", trans," key:", key," item:", itm,"util:", util
                 else:
                     i = 0
                     util = 0
                     break
        #    print "i:", i, "itm:", itm
            if i > 0:
        #        print "Transaction:", trans,"itemset:", key,"utility:", util
                lfhu_itemset[key] = prev_util + util
                prev_util = util
            else:
                util = 0
                prev_util = 0
        i = 0
  # print "key:", key,"utility:", util
#================================================================================================================
#   print "itemset with frequency:", l
  # for key, value in l:
  #      util = 0
 #       for itm in key:
   #         print "key", key," and frequency:", value
   #         print "key item:", itm,"& utility of item", item_utility[itm]
   #         util = util + (int(value) * int(item_utility[itm]))
   #         util = util + (int(item_utility[itm]))
      #  print "utility:", util
    #    lfhu_itemset[key] = util
#================================================================================================================
   return dict([(item, ut) for item, ut in lfhu_itemset.items() if ut >= min_util])
#Find High Utility Itemsets...
def lflu_itemset(transaction_list, lf_itemset, item_utility, item_util_list, min_util):
    print "In lflu_itemset\n"
    lflu_itemset = dict()
    i = 0
    prev_util = 0
                
    l = [
        (item, int(sum(1 for row in transaction_list if item.issubset(row))))
  #       (item, int(sum(1 for row in transaction_list if item in row)) * item_utility[item])
        for item in lf_itemset
    ]
  #  print "itemset with frequency:", l
    for key, value in l:
        util = 0
        for trans, ut in item_util_list:
            for itm in key:
            #         print "key", key," and frequency:", value
   #         print "key item:", itm,"& utility of item", item_utility[itm]
   #         util = util + (int(value) * int(item_utility[itm]))
                 if itm in trans:
                     i = i + 1
                     util = util + (int(ut[trans.index(itm)]))
      #               print "trans:", trans," key:", key," item:", itm,"util:", util
                 else:
                     i = 0
                     util = 0
                     break
          #  print "i:", i, "itm:", itm
            if i > 0:
        #        print "Transaction:", trans,"itemset:", key,"utility:", util
                lflu_itemset[key] = prev_util + util
                prev_util = util
            else:
                util = 0
                prev_util = 0
        i = 0
   # print "key:", key,"utility:", util

    return dict([(item, ut) for item, ut in lflu_itemset.items() if ut < min_util])

def apriori(data, transaction_list, itemset1, itemset2, min_support, min_confidence):
    print "In apriori:\n"

    # Association rules
    l1 = dict()
    p1 = dict()
    len_transaction_list = len(transaction_list)
    l1 = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row)))/len_transaction_list) 
        for item in itemset1
    ]
 #   for item, support in l :
 #       l1[item] = support
 #   print "Itemset1:", l1
    
    p1 = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row)))/len_transaction_list) 
        for item in itemset2
    ]
  #  for item, support in p :
  #      p1[item] = support
  #  return dict([(item, support) for item, support in l if support >= min_support])
 #   print "Itemset2:", p1
    
    rules = list()
    for item1, support1 in l1:
        for item2, support2 in p1:
            if len(item1) > 1 and len(item2) > 1:
#                for A in subsets(item1):
#                    B = item.difference(A)
#                    if B in item2 and A in item1:
#                        A = frozenset(A)
#                        AB = A | B
                   # item1 = frozenset(item1)
                   # item2 = frozenset(item2)
 #                   item12 = item1 | item2
   ##              for A in subsets(item1):
    #                 B = item1.difference(A)
      #           print "item1:", item1,"support1:", support1
      #           print "item2:", item2,"support2:", support2
     #                if B in item2:
     #                    A = frozenset(A)
     #                    AB = A | B
                 if item1.issubset(item2):
                         confidence = float(support2 / support1) * 100
      #                   print "item1:", item1
      #                   print "item2:", item2
      #                   print "confidence:", confidence
                         if confidence >= min_confidence * 100:
    #                        print "item1:", item1, "item2:", item2,"support1:", support1, "support2:", support2, "conf:", confidence
                            rules.append((item1, item2, confidence ))  
#                    rules[item1] = item2
  #                  rules[item2] = confidence  
    return  rules
    


#def print_report(outfilename, rules):
#    f = open(outfilename, 'w')
#    for row in rules:  
#        f.write(''.join(str(row) for s in row) + '\n')
#    print('--Frequent Itemset--')
#    for item, support in sorted(f_itemset.items(), key=lambda (item, support): support):
#        print('[I] {} : {}'.format(tuple(item), round(support, 4)))
        
#        print('--InFrequent Itemset--')
#    for item, support in sorted(lf_itemset.items(), key=lambda (item, support): support):
#        print('[I] {} : {}'.format(tuple(item), round(support, 4)))

#    print('')
#   f = open(outfilename, 'w')
#    f.write(rules)
#   f.writelines('--Rules--')
#   for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
#       f.writelines('[R] {} => {} : {}'.format(tuple(A), tuple(B), round(confidence, 4))) 


def data_from_csv(filename):
    print "In data_from_csv\n"
    f = open(filename, 'rU')
    for l in f:
        row = map(str.strip, l.split(','))
        yield row

def utility_from_csv(utfilename):
    print "In utility_from_csv\n"
    f = open(utfilename, 'rU')
    for l in f:
        utrow = map(str.strip, l.split(','))
        yield utrow


def parse_options():
    optparser = argparse.ArgumentParser(description='Apriori Algorithm.')
    optparser.add_argument(
        '-f', '--input_file',
        dest='filename',
        help='filename containing csv',
        required=True
    )
    optparser.add_argument(
        '-uf', '--utility_file',
        dest='utfilename',
        help='utfilename containing csv',
        required=True
    )
    optparser.add_argument(
        '-op', '--output_file',
        dest='outfilename',
        help='outfilename containing csv',
        required=True
    )
    optparser.add_argument(
        '-s', '--min_support',
        dest='min_support'  ,
        help='minimum support',
        default=0.30,
        type=float
    )
    optparser.add_argument(
        '-c', '--min_confidence',
        dest='min_confidence',
        help='minimum confidence',
        default=0.30,
        type=float
    )
    optparser.add_argument(
        '-u', '--min_util',
        dest='min_util',
        help='minimum utility',
        default=3,
        type=int
    )
    optparser.add_argument(
        '-ut', '--util_thresh',
        dest='util_thresh',
        help='utility threshold',
        default=3,
        type=int
    )
    return optparser.parse_args()


def main():
    start_time = datetime.now()
    options = parse_options()

    data = data_from_csv(options.filename)
    utility = utility_from_csv(options.utfilename)
    item_utility =dict()
# Get first itemset and transactions
    itemset, transaction_list = itemset_from_data(data)
#    print "itemset:/n", itemset,"& transaction:/n", transaction_list
    data = data_from_csv(options.filename)
    utility_list,item_util_list, item_utility = itemset_from_utility(data, utility)
#    print "itemset:/n", itemset,"& transaction:/n", transaction_list
    print "items & utility:\n", item_util_list
    print "items & utility:\n", utility_list

    # Get the frequent and infrequent itemset
    hf_itemset = freq_itemset(transaction_list, itemset, item_utility, options.util_thresh, options.min_support)
    print "frequent itemsets:\n", hf_itemset
    lf_itemset = infreq_itemset(transaction_list, itemset, item_utility, options.util_thresh, options.min_support)
    print "Infrequent itemsets:\n", lf_itemset
    hfhu = hfhu_itemset(transaction_list,hf_itemset, item_utility, item_util_list, options.min_util)
  #  print "high utility high frequency itemsets:\n", hfhu
    hflu = hflu_itemset(transaction_list, hf_itemset, item_utility, item_util_list, options.min_util)
  #  print "low utility high frequency itemsets:\n", hflu
    lfhu = lfhu_itemset(transaction_list, lf_itemset, item_utility, item_util_list, options.min_util)
   # print "high utility low frequency itemsets:\n", lfhu
    lflu = lflu_itemset(transaction_list, lf_itemset, item_utility, item_util_list, options.min_util)
  #  print "low utility low frequency itemsets:\n", lflu
#    luhf_itemset = lutility_itemset(transaction_list, hf_itemset, options.min_util)
#    hulf_itemset = hutility_itemset(transaction_list, lf_itemset, options.min_util)
#    lulf_itemset = lutility_itemset(transaction_list, lf_itemset, options.min_util)

    f = open(options.outfilename, 'w')
    rules = apriori(data, transaction_list, hfhu, lfhu, options.min_support, options.min_confidence)
#    print_report(options.outfilename, rules)
    print "HFHU -> LFHU"
    f.write (' Rules for HFHU -> LFHU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4))) 
#    for row in rules:  
#        f.write(''.join(str(row) for s in row) + '\n')
    rules = apriori(data, transaction_list, hflu, lfhu, options.min_support, options.min_confidence)
    print "HFLU -> LFHU"
    f.write('Rules for HFLU -> LFHU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
#    print_report(options.outfilename,rules)
#    for row in rules:  
#        f.write(''.join(str(row) for s in row) + '\n')
    rules = apriori(data, transaction_list, hfhu, lflu, options.min_support, options.min_confidence)
    print "HFHU -> LFLU"
    f.write('Rules for HFHU -> LFLU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
#    print_report(options.outfilename,rules)
#    for row in rules:  
#        f.write(''.join(str(row) for s in row) + '\n')
    rules = apriori(data, transaction_list, hflu, lflu, options.min_support, options.min_confidence)
    print "HFLU -> LFLU"
    f.write('Rules for HFLU -> LFLU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
#    for row in rules:  
#        f.write(''.join(str(row) for s in row) + '\n')
    f.close()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
#    print_report(options.outfilename,rules)
     
 #   print " Rules for High Utility Low Frequency itemset:"
 #   rules, itemset = apriori(data, utility, hulf_itemset, lf_itemset, options.min_support, options.min_confidence)
 #   print_report(rules, itemset)
    
 #   print " Rules for Low Utility High Frequency itemset:"    
 #   rules, itemset = apriori(data, utility, luhf_itemset, lf_itemset, options.min_support, options.min_confidence)
 #   print_report(rules, itemset)
    
 #   print " Rules for Low Utility Low Frequency itemset:"
 #   rules, itemset = apriori(data, utility, lulf_itemset, lf_itemset, options.min_support, options.min_confidence)
 #   print_report(rules, itemset)


if __name__ == '__main__':
    main()