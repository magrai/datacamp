#-*- coding: utf-8 -*-
"""Generators of  x-y pairs of node data."""
import networkx_v1x as nx
from networkx_v1x.utils import dict_to_numpy_array
__author__ = ' '.join(['Aric Hagberg <aric.hagberg@gmail.com>'])
__all__ = ['node_attribute_xy',
           'node_degree_xy']

def node_attribute_xy(G, attribute, nodes=None):
    """Return iterator of node-attribute pairs for all edges in G.

    Parameters
    ----------
    G: NetworkX graph

    attribute: key
       The node attribute key.

    nodes: list or iterable (optional)
        Use only edges that are adjacency to specified nodes.
        The default is all nodes.

    Returns
    -------
    (x,y): 2-tuple
        Generates 2-tuple of (attribute,attribute) values.

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_node(1,color='red')
    >>> G.add_node(2,color='blue')
    >>> G.add_edge(1,2)
    >>> list(nx.node_attribute_xy(G,'color'))
    [('red', 'blue')]

    Notes
    -----
    For undirected graphs each edge is produced twice, once for each edge 
    representation (u,v) and (v,u), with the exception of self-loop edges 
    which only appear once.
    """
    if nodes is None:
        nodes = set(G)
    else:
        nodes = set(nodes)
    node = G.node 
    for u,nbrsdict in G.adjacency_iter():
        if u not in nodes:
            continue
        uattr = node[u].get(attribute,None)
        if G.is_multigraph():
            for v,keys in nbrsdict.items():
                vattr = node[v].get(attribute,None)                
                for k,d in keys.items():
                    yield (uattr,vattr)
        else:
            for v,eattr in nbrsdict.items():
                vattr = node[v].get(attribute,None)
                yield (uattr,vattr)


def node_degree_xy(G, x='out', y='in', weight=None, nodes=None):
    """Generate node degree-degree pairs for edges in G.

    Parameters
    ----------
    G: NetworkX graph

    x: string ('in','out')
       The degree type for source node (directed graphs only).

    y: string ('in','out')
       The degree type for target node (directed graphs only).

    weight: string or None, optional (default=None)
       The edge attribute that holds the numerical value used 
       as a weight.  If None, then each edge has weight 1.
       The degree is the sum of the edge weights adjacent to the node.

    nodes: list or iterable (optional)
        Use only edges that are adjacency to specified nodes.
        The default is all nodes.

    Returns
    -------
    (x,y): 2-tuple
        Generates 2-tuple of (degree,degree) values.


    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_edge(1,2)
    >>> list(nx.node_degree_xy(G,x='out',y='in'))
    [(1, 1)]
    >>> list(nx.node_degree_xy(G,x='in',y='out'))
    [(0, 0)]

    Notes
    -----
    For undirected graphs each edge is produced twice, once for each edge 
    representation (u,v) and (v,u), with the exception of self-loop edges 
    which only appear once.
    """
    if nodes is None:
        nodes = set(G)
    else:
        nodes = set(nodes)
    xdeg = G.degree_iter
    ydeg = G.degree_iter
    if G.is_directed():
        direction = {'out':G.out_degree_iter,
                     'in':G.in_degree_iter}
        xdeg = direction[x]
        ydeg = direction[y]

    for u,degu in xdeg(nodes, weight=weight):
        neighbors = (nbr for _,nbr in G.edges_iter(u) if nbr in nodes)
        for v,degv in ydeg(neighbors, weight=weight):
            yield degu,degv
 

# fixture for nose tests
def setup_module(module):
    from nose import SkipTest
    try:
        import numpy
    except:
        raise SkipTest("NumPy not available")
    try:
        import scipy
    except:
        raise SkipTest("SciPy not available")
