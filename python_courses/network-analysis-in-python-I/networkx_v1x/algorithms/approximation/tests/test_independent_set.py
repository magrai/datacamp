from nose.tools import *
import networkx_v1x as nx
import networkx_v1x.algorithms.approximation as a

def test_independent_set():
    # smoke test
    G = nx.Graph()
    assert_equal(len(a.maximum_independent_set(G)),0)
