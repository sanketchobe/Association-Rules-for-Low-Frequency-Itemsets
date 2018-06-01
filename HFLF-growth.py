# encoding: utf-8

"""
A Python implementation of the FP-growth algorithm.

Basic usage of the module is very simple:

    > from fp_growth import find_frequent_itemsets
    > find_frequent_itemsets(transactions, minimum_support)
"""

from collections import defaultdict, namedtuple
from itertools import imap
from datetime import datetime

__author__ = 'Sanket Chobe <sanketchobe@gmail.com>'
__copyright__ = 'Copyright © 2018 Sanket Chobe'


def find_association_rules(itemset, hf_itemset, lf_itemset, min_support, min_confidence):
    
    rules = list()
    for item1,supp1 in hf_itemset.items():
        for item2,supp2 in lf_itemset.items():
          #  print 'item1:',set(item1), 'item2:',set(item2), set(item1).issubset(set(item2))
            if len(item1) >= 1 and len(item2) >= 1:
                 support1 = supp1[1]
                 support2 = supp2[1]
                 if set(item1).issubset(set(item2)):
                         confidence = float(float(support2) / float(support1)) * 100
                        # print 'item1:',item1, 'item2:', item2, 'support1:', support1, 'support2:', support2, 'conf:', confidence, 'min_conf:', min_confidence
                         if confidence >= float(min_confidence):
                
                            rules.append((item1, item2, confidence ))   
    return  rules
        
    
def find_hflf_utility(hf_itemset, utility_dictionary,itemset_trans, min_utility, min_threshold_util):
    
        
    current_item =[]
    prev_item =[]
    hflfhu =dict()
    hflflu =dict()
    utility=0
    i=0
    for item,supp in hf_itemset:
        current_item =[]
        prev_item =[]
        if len(item) ==1:
            trans =itemset_trans[item[0]]
            for it in trans:
                for lst in utility_dictionary[it]:
                    if item ==lst.keys():
                        utility = int(lst.values()[0]) + utility
            if utility >=min_utility:   
                hflfhu[tuple(item[0])] =(utility,supp)
            else:
                if utility > min_threshold_util:
                    hflflu[tuple(item[0])] =(utility,supp)
            utility =0
        else:
            for itm in item:
                i =i+1
                if (not current_item) and (not prev_item):
                    prev_item =itemset_trans[(itm)]
                    current_item =itemset_trans[itm]
                else:
                    current_item =itemset_trans[itm]
                    prev_item = list(set(current_item).intersection(prev_item))
           # print 'commn item:',prev_item
            
            for it in prev_item:
                for lst in utility_dictionary[it]:
                    for itm in item:
            #            print 'item:', item, 'lst:', int(lst.keys()[0]),int(lst.values()[0])
                        if (itm) ==(lst.keys()[0]):
             #               print 'item:', itm, 'lst:', lst.items()
                            utility = int(lst.values()[0]) + utility
            if utility >=min_utility:   
                hflfhu[tuple(item)] =(utility,supp)
            else:
                if utility >= min_threshold_util:
                    hflflu[tuple(item)] =(utility,supp)
            utility =0
            
    return hflfhu,hflflu
    

def find_utility_item(transactions,utility_transactions):
    utility_dictionary =dict()
    trans_dictionary =dict()
    itemset =dict()
    items = defaultdict(lambda: 0)
    util_list =[]
    item_list=[]
    count =0
    i =0
    j=0
    
    for transaction in transactions:
     #   print 'len of transaction:', len(transaction)
        count =count+1
        for utility in utility_transactions:
            i = i+1
            if count ==i:
                for j in range(len(utility)):
                    trans_dictionary[transaction[j]] =utility[j]
                    util_list.append(trans_dictionary)
                    trans_dictionary =dict()
        utility_dictionary[count] =util_list
        trans_dictionary =dict()
        util_list=[]
        j=0
        i=0
    
    for transaction in transactions:
        for item in transaction:
            items[item] += 1
       
    count1=0
    i=0
    for item in items.keys():
        for transaction in transactions:
            count1 =count1+1
            if item in transaction or i==0:
                item_list.append(count1)
                itemset[item] =item_list
            i=i+1
        item_list=[]
        count1 =0
        
                
   # print 'utility_dictionary:', utility_dictionary,'count:', count,'items:', itemset
        
    return utility_dictionary, itemset
def find_frequent_itemsets(transactions, minimum_support, min_threshold_sup, include_support=False):
    """
    Find frequent itemsets in the given transactions using FP-growth. This
    function returns a generator instead of an eagerly-populated list of items.

    The `transactions` parameter can be any iterable of iterables of items.
    `minimum_support` should be an integer specifying the minimum number of
    occurrences of an itemset for it to be accepted.

    Each item must be hashable (i.e., it must be valid as a member of a
    dictionary or a set).

    If `include_support` is true, yield (itemset, support) pairs instead of
    just the itemsets.
    """
    items = defaultdict(lambda: 0) # mapping from items to their supports

    # Load the passed-in transactions and count the support that individual
    # items have.
    for transaction in transactions:
        for item in transaction:
            items[item] += 1
    #    print 'trans:', transaction, 'item:', item
   # print 'items:', items

    # Remove infrequent items from the item support dictionary.
    items = dict((item, support) for item, support in items.iteritems())
    #    items = dict((item, support))
    #    if support >= minimum_support)

    # Build our FP-tree. Before any transactions can be added to the tree, they
    # must be stripped of infrequent items and their surviving items must be
    # sorted in decreasing order of frequency.
    def clean_transaction(transaction):
        transaction = filter(lambda v: v in items, transaction)
        transaction.sort(key=lambda v: items[v], reverse=True)
        print 'clear transaction:', transaction
        return transaction

    master = FPTree()
    for transaction in imap(clean_transaction, transactions):
        master.add(transaction)
    
    print 'FP tree:',master.nodes

    def find_hf_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix:
                # New winner!
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set

                # Build a conditional tree and recursively search for frequent
                # itemsets within it.
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_hf_with_suffix(cond_tree, found_set):
                    print 'itemset:', s
                    yield s # pass along the good news to our caller
    
    def find_lf_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support < minimum_support and item not in suffix and support >=min_threshold_sup:
                # New winner!
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set

                # Build a conditional tree and recursively search for frequent
                # itemsets within it.
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_lf_with_suffix(cond_tree, found_set):
                    
                    print 'itemset:', s
                    yield s # pass along the good news to our caller
                
                

    # Search for frequent itemsets, and yield the results we find.
    for hf_itemset in find_hf_with_suffix(master, []):
        yield hf_itemset
    
    # Search for low frequency itemsets, and yield the results we find.
    for lf_itemset in find_lf_with_suffix(master, []):
        yield lf_itemset
    

class FPTree(object):
    """
    An FP tree.

    This object may only store transaction items that are hashable
    (i.e., all items must be valid as dictionary keys or set members).
    """

    Route = namedtuple('Route', 'head tail')

    def __init__(self):
        # The root node of the tree.
        self._root = FPNode(self, None, None)

        # A dictionary mapping items to the head and tail of a path of
        # "neighbors" that will hit every node containing that item.
        self._routes = {}

    @property
    def root(self):
        """The root node of the tree."""
        return self._root

    def add(self, transaction):
        """Add a transaction to the tree."""
        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                # There is already a node in this tree for the current
                # transaction item; reuse it.
                next_point.increment()
            else:
                # Create a new point and add it as a child of the point we're
                # currently looking at.
                next_point = FPNode(self, item)
                point.add(next_point)

                # Update the route of nodes that contain this item to include
                # our new node.
                self._update_route(next_point)

            point = next_point

    def _update_route(self, point):
        """Add the given node to the route through all nodes for its item."""
        assert self is point.tree

        try:
            route = self._routes[point.item]
            route[1].neighbor = point # route[1] is the tail
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            # First node for this item; start a new route.
            self._routes[point.item] = self.Route(point, point)

    def items(self):
        """
        Generate one 2-tuples for each item represented in the tree. The first
        element of the tuple is the item itself, and the second element is a
        generator that will yield the nodes in the tree that belong to the item.
        """
        for item in self._routes.iterkeys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        """
        Generate the sequence of nodes that contain the given item.
        """

        try:
            node = self._routes[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        """Generate the prefix paths that end with the given item."""

        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))

    def inspect(self):
        print 'Tree:'
        self.root.inspect(1)

        print
        print 'Routes:'
        for item, nodes in self.items():
            print '  %r' % item
            for node in nodes:
                print '    %r' % node

def conditional_tree_from_paths(paths):
    """Build a conditional FP-tree from the given prefix paths."""
    tree = FPTree()
    condition_item = None
    items = set()

    # Import the nodes in the paths into the new tree. Only the counts of the
    # leaf notes matter; the remaining counts will be reconstructed from the
    # leaf counts.
    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item):
       # print 'tree paths:', path
        count = path[-1].count
        for node in reversed(path[:-1]):
            print 'node in path:', node.item, node.count
            node._count += count
            
    return tree

class FPNode(object):
    """A node in an FP tree."""

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add(self, child):
        """Add the given FPNode `child` as a child of this node."""

        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")

        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    def search(self, item):
        """
        Check whether this node contains a child node for the given item.
        If so, that node is returned; otherwise, `None` is returned.
        """
        try:
            return self._children[item]
        except KeyError:
            return None

    def __contains__(self, item):
        return item in self._children

    @property
    def tree(self):
        """The tree in which this node appears."""
        return self._tree

    @property
    def item(self):
        """The item contained in this node."""
        return self._item

    @property
    def count(self):
        """The count associated with this node's item."""
        return self._count

    def increment(self):
        """Increment the count associated with this node's item."""
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1

    @property
    def root(self):
        """True if this node is the root of a tree; false if otherwise."""
        return self._item is None and self._count is None

    @property
    def leaf(self):
        """True if this node is a leaf in the tree; false if otherwise."""
        return len(self._children) == 0

    @property
    def parent(self):
        """The node's parent"""
        return self._parent

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a parent.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a parent from another tree.")
        self._parent = value

    @property
    def neighbor(self):
        """
        The node's neighbor; the one with the same value that is "to the right"
        of it in the tree.
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a neighbor.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a neighbor from another tree.")
        self._neighbor = value

    @property
    def children(self):
        """The nodes that are children of this node."""
        return tuple(self._children.itervalues())

    def inspect(self, depth=0):
        print ('  ' * depth) + repr(self)
        for child in self.children:
            child.inspect(depth + 1)

    def __repr__(self):
        if self.root:
            return "<%s (root)>" % type(self).__name__
        return "<%s %r (%r)>" % (type(self).__name__, self.item, self.count)


if __name__ == '__main__':
    from optparse import OptionParser
    import csv
    
    start_time = datetime.now()
    p = OptionParser(usage='%prog data_file')
    p.add_option('-s', '--minimum-support', dest='minsup', type='int',
        help='Minimum itemset support (default: 2)')
    p.add_option('-n', '--numeric', dest='numeric', action='store_true',
        help='Convert the values in datasets to numerals (default: false)')
    p.add_option('-u', '--minimum-utility', dest='minutil', type='int',
        help='Minimum itemset utility (default: 5)')
    p.add_option('-c', '--minimum-confidence', dest='minconf', type='int',
        help='Minimum threshold confidence (default: 20)')

    p.set_defaults(minsup=2)
    p.set_defaults(minutil=5)
    p.set_defaults(minconf=20)
    p.set_defaults(minthreshsup=1)
    p.set_defaults(minthreshutil=1)
    p.set_defaults(numeric=False)
    
    hf_itemset=[]
    lf_itemset=[]

    options, args = p.parse_args()
    if len(args) < 1:
        p.error('must provide the path to a CSV file to read')
    
    f = open(args[2], 'w')

    transactions = []
    with open(args[0]) as database:
        for row in csv.reader(database):
            if options.numeric:
                transaction = []
                for item in row:
                    transaction.append(long(item))
                transactions.append(transaction)
            else:
                transactions.append(row)
    
    utility_transactions = []
    with open(args[1]) as utility_db:
        for row in csv.reader(utility_db):
            if options.numeric:
                utility_trans = []
                for util in row:
                    utility_trans.append(long(util))
                utility_transactions.append(transaction)
            else:
                utility_transactions.append(row)
#    print 'utility transactions:', utility_transactions
        
    utility_dictionary =dict()
    utility_dictionary,itemset_trans = find_utility_item(transactions, utility_transactions)

    result = []
    itemset_supp =dict()
    for itemset, support in find_frequent_itemsets(transactions, options.minsup,1, True):
        result.append((itemset,support))
        itemset_supp[tuple(itemset)] = support
    print 'itemset with support:', itemset_supp

    result = sorted(result, key=lambda i: i[0])
    for itemset, support in result:
        if support >= options.minsup:
            hf_itemset.append((itemset,support))
        else:
            lf_itemset.append((itemset,support))
        print str(itemset) + ' ' + str(support)
    print 'hf itemset:', hf_itemset, 'lf_itemset:', lf_itemset
    
    hfhu,hflu =find_hflf_utility(hf_itemset, utility_dictionary,itemset_trans, options.minutil,1)
    print 'hfhu:', hfhu, '\n hflu:', hflu
    lfhu,lflu =find_hflf_utility(lf_itemset, utility_dictionary,itemset_trans, options.minutil,1)
    print 'lfhu:', lfhu, '\n lflu:', lflu
    
    rules = find_association_rules(itemset_supp, hfhu, lfhu, options.minsup, options.minconf)
    print "HFHU -> LFHU :"
    f.write (' Rules for HFHU -> LFHU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
    
    rules =[]
    rules = find_association_rules(itemset_supp, hflu, lfhu, options.minsup, options.minconf)
    print "HFLU -> LFHU :"
    f.write (' Rules for HFLU -> LFHU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
    
    rules =[]
    rules = find_association_rules(itemset_supp, hfhu, lflu, options.minsup, options.minconf)
    print "HFHU -> LFLU :"
    f.write (' Rules for HFHU -> LFLU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
    
    rules =[]
    rules = find_association_rules(itemset_supp, hflu, lflu, options.minsup, options.minconf)
    print "HFLU -> LFLU :"
    f.write (' Rules for HFLU -> LFLU:\n')
    for A, B, confidence in sorted(rules, key=lambda (A, B, confidence): confidence):
        f.writelines('[R] {} => {} : {}\n'.format(tuple(A), tuple(B), round(confidence, 4)))
    
    f.close()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

    