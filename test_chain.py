#!/usr/bin/python

"""test functions for ChainNode"""
from fractions import Fraction
from chain_node import ChainNode

def create_walk_chain(perc, links, opt):
    """Create a chain of ChainNodes with the following rule:
       The root node has opt possible values with equal apriori probabilities.
       Child nodes have a perc probability of having the same value as their parent, (1 - perc)/2 of having the 2 adjacent values (mod opt)
       and so zero probability of having the opposite value. Returns the root node"""
    name = "A"
    root = ChainNode(name=name, probs={0:0.25, 1:0.25, 2:0.25, 3:0.25})
    links -= 1
    probs = {}
    for key in range(opt):
        probs[key] = {key:perc, (key + 1) % opt: (1 - perc)/2, (key + (opt-1)) % opt:(1 - perc)/2}
    parent = root
    while links > 0:
        name = chr(ord(name) + 1)
        new_node = ChainNode(name=name, probs=probs, parent=parent)
        parent = new_node
        links -= 1
    return root
    
def create_decay_chain(perc, links, opt):
    """Create a chain of ChainNodes with the following rule:
       The root starts out at opt - 1
       Each step down the chain there is a perc possibility of stayng the same and perc-1 of lowering the current value by 1, unless value is 1
       if we get down to zero we are stuck there.
    """
    name = "A"
    root = ChainNode(name=name, probs={opt - 1:perc, opt -2:1 - perc})
    links -= 1
    probs = {}
    for key in range(1, opt):
        probs[key] = {key:perc, key-1: 1 - perc}
        probs[0] = {0:1}
    parent = root
    while links > 0:
        name = chr(ord(name) + 1)
        new_node = ChainNode(name=name, probs=probs, parent=parent)
        parent = new_node
        links -= 1
    return root

    

if __name__ == '__main__':
     import argparse
     parser = argparse.ArgumentParser()
     parser.add_argument('--perc', help="perc value to use", default=0.5)
     parser.add_argument('--links', help="number of links in the chain", type=int, default=6)
     parser.add_argument('--opt', help="number of options for a node", type=int, default=4)
     parser.add_argument('--chain', help="type of chain to test", default="decay")
     parser.add_argument('--node', help="index of node to actualize (root=0)", default=1, type=int)
     parser.add_argument('--val', help="value to give the actualized node", default=1, type=int)
     args = parser.parse_args()
     if type(args.perc) == str and '/' in args.perc:
         perc = Fraction(args.perc)
     else:
         perc = float(args.perc)
     if args.chain == 'walk':
         root = create_walk_chain(perc, args.links, args.opt)
     else:
         root = create_decay_chain(perc, args.links, args.opt)
     index = 0
     node = root
     while index < args.node:
         node = node.child
         index += 1
     node.set_current_probs({args.val:1})
     node.set_downstream_probs()
     node.set_upstream_probs()
     node = root
     print("node {} probs {}".format(node.name, node.current_probs))
     while node.child is not None:
         node = node.child
         print("node {} probs {}".format(node.name, node.current_probs))
