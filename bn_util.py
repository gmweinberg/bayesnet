"""Utility functions for the bayes network."""

def oneish(afloat):
    """Determine whether a number is considered 'close enough' to one. Disjoint probabilities should sum to one.
       Returns a boolean."""
    if afloat > 0.99999 and afloat < 1.00001:
        return True
    return False
