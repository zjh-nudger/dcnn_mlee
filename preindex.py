import cPickle
import copy
from process_gdep_tree import Node as node
'''
"preindex.py" reforms the sentence into a tree format from the parse file.
'''
'''
class node:

    def __init__(self, word):
        if word != None:
            self.word = word
            self.kidsword = []
            self.kidsindex = []
            self.parent = []
            self.finished = 0
            self.is_word = 1
            self.selfindex = 0
            self.parentindex = 0
            self.label = ""

            # the "ind" variable stores the look-up index of the word in the 
            # word embedding matrix We. set this value when the vocabulary is finalized
            self.ind = -1

        else:
            self.is_word = 0
'''

if __name__=="__main__": 
    import glob
    #input_file  = "TREC/TREC_all_parsed.txt"
    input_file = 'MLEE_DATA/mlee-train-data.txt'
    #output_file = "TREC/TREC_all_tree.p"
    output_file = 'MLEE_DATA/mlee_train_tree.p'
        
    ## [advmod(develop-4, How-1), aux(develop-4, did-2), nsubj(develop-4, serfdom-3), root(ROOT-0, develop-4), prt(develop-4, in-5), cc(develop-4, and-6), advmod(leave-8, then-7), conj(develop-4, leave-8), dobj(leave-8, Russia-9), punct(develop-4, ?-10)]
    input = open(input_file)
    doc = []
    for i in input.readlines():
        i = i.strip()
        i = i.strip("[]")
        current = i.split("), ")
        print current
        
        node_container = {}
        ROOT = node("ROOT")
        node_container[0] = ROOT    
        for index,j in enumerate(current[1:]):
            dependency = j.split("(")[0] # dependency relation
            j = j.split("(")[1].strip(")")
            current_list = [i.strip() for i in j.split(", ")]
            #print index, current_list
            current_node = node("_".join(current_list[0].\
                                         split("-")[:-1]))
            current_node.index = int(current_list[0].\
                                     split("-")[-1])
            current_node.dependency = dependency
            
            if "_".join(current_list[1].split("-")[:-1]) == "ROOT":
                current_node.parent = ROOT
            else:    
                current_node.parent = "_".join(current_list[0].\
                                               split("-")[:-1])
            current_node.parent_index = int(current_list[0].\
                                       split("-")[-1])
            node_container[current_node.selfindex] = current_node
        
        node_container1 = copy.deepcopy(node_container)
        for i in node_container1:
            current = node_container1[i]
            p_index = current.parentindex
            #print p_index
            if p_index not in node_container:
                new_node = node(current.parent)
                new_node.parent = ROOT
                new_node.selfindex = p_index
                node_container[p_index] = new_node    
        
        for i in node_container:
            current = node_container[i]
            if current.word == "ROOT":
                continue            
            p_index = current.parentindex
            #print p_index
            if p_index not in node_container:
                new_node = node(current.parent)
                new_node.parent = ROOT
                new_node.selfindex = p_index
                node_container[p_index] = new_node
                
            p = node_container[p_index]
            
            p.kidsword.append(current.word)
            p.kidsindex.append(current.selfindex)
        
        for j in node_container:
            i = node_container[j]
            print "self", i.selfindex, "parent", i.parentindex,\
                "child", i.kidsindex
        
        doc.append(node_container)
    
    #print len(doc)
    cPickle.dump(doc, open(output_file, "wb"))