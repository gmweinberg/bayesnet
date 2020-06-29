"""A ChainNode has zero or one parents and zero or one children. It will have probabilities conditional on the possible values of its parent.
   We want to be able to go up and down the chain calculating probabilities.""" 
   
# We will treat the root node as if it has an ancester called nature which always has the value zero,
# So the a_priori probabilites are the  conditional probabilities when nature has a value of zero.

from collections import defaultdict

class ChainNode(object):
    def __init__(self, name, probs, parent=None):
        self.name = name
        self.parent = parent
        self.probs = dict(probs) # these are the conditional probabilities
        if parent:
            parent.child = self
            self.apriori_probs = self.get_conditioned_probs(parent.apriori_probs)
        else:
            self.apriori_probs = self.probs
        self.current_probs = None # this is a temporary value we will use if we instantiate a node
        self.child = None
        
    def get_prob_type(self):
        """Check what type we are using to store out probabilities (float or Fraction probably).
           Requires current_probs to be set."""
        for aval in self.current_probs.values():
            return type(aval)

        
    def set_current_probs(self, probs):
         """Set the current probability for this node. In articular, we can instantiate this bode by setting the probability of one node value to zero."""
         self.current_probs = probs
         
         
    def set_upstream_probs(self, child_probs = None):
         """Set current_probs for all upstream nodes, and for this node itself it is not set already.
            Returns the root node"""
         node = self
         while(True):
             if not node.parent:
                 break
             node.set_parent_probs()
             node = node.parent
         return node
         
    def set_parent_probs(self):
        """Use bayes's rule to set parent probabilities based on current probs and parent's apriori probs."""
        if not self.current_probs:
            raise Exception('Must have current probs')
        new_probs = {}
        norm = 0
        for sval in self.current_probs:
            mul = self.current_probs.get(sval, 0)
            for pval in self.parent.apriori_probs:
                if not self.probs[pval].get(sval):
                    continue
                contrib = mul * self.parent.apriori_probs[pval] * self.probs[pval][sval]
                norm += contrib
                #print('pval {} sval {} parent apriori {} self {}'.format(pval, sval, self.parent.apriori_probs, self.probs))
                if new_probs.get(pval):
                    new_probs[pval] += contrib
                else:
                    new_probs[pval] = contrib
        for key in new_probs:
            new_probs[key] /= norm
        self.parent.current_probs = new_probs

         
    def set_downstream_probs(self):
        """Set the value of all nodes downstream of this node. We must set probabilities for this node before calling this method."""
        if self.current_probs is None:
            raise Exception("Must have current_probs.""")
        child = self.child
        parent_probs = self.current_probs
        while child:
            new_probs = child.get_conditioned_probs(parent_probs)
            child.current_probs = new_probs
            child = child.child
            parent_probs = new_probs
        
    def get_conditioned_probs(self, parent_probs):
        """Compute new_probs probs based on parent_probs and conditional probs. Returns the new_probs"""
        new_probs = {}
        for key in parent_probs:
            for child_key in self.probs[key]:
                if child_key in new_probs:
                    new_probs[child_key] += parent_probs[key] * self.probs[key][child_key]
                else:
                    new_probs[child_key] =  parent_probs[key] * self.probs[key][child_key]
        return new_probs

