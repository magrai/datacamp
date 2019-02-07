# coding: utf-8
"""
Provides functions for finding and testing for locally `(k, l)`-connected
graphs.

"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)\nDan Schult (dschult@colgate.edu)"""
#    Copyright (C) 2004-2015 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

_all__ = ['kl_connected_subgraph', 'is_kl_connected']

import copy
import networkx_v1x as nx


def kl_connected_subgraph(G, k, l, low_memory=False, same_as_graph=False):
    """Returns the maximum locally `(k, l)`-connected subgraph of ``G``.

    A graph is locally `(k, l)`-connected if for each edge `(u, v)` in the
    graph there are at least `l` edge-disjoint paths of length at most `k`
    joining `u` to `v`.

    Parameters
    ----------
    G : NetworkX graph
        The graph in which to find a maximum locally `(k, l)`-connected
        subgraph.

    k : integer
        The maximum length of paths to consider. A higher number means a looser
        connectivity requirement.

    l : integer
        The number of edge-disjoint paths. A higher number means a stricter
        connectivity requirement.

    low_memory : bool
        If this is ``True``, this function uses an algorithm that uses slightly
        more time but less memory.

    same_as_graph : bool
        If this is ``True`` then return a tuple of the form ``(H, is_same)``,
        where ``H`` is the maximum locally `(k, l)`-connected subgraph and
        ``is_same`` is a Boolean representing whether ``G`` is locally `(k,
        l)`-connected (and hence, whether ``H`` is simply a copy of the input
        graph ``G``).

    Returns
    -------
    NetworkX graph or two-tuple
        If ``same_as_graph`` is ``True``, then this function returns a
        two-tuple as described above. Otherwise, it returns only the maximum
        locally `(k, l)`-connected subgraph.

    See also
    --------
    is_kl_connected

    References
    ----------
    .. [1]: Chung, Fan and Linyuan Lu. "The Small World Phenomenon in Hybrid
            Power Law Graphs." *Complex Networks*. Springer Berlin Heidelberg,
            2004. 89--104.

    """
    H=copy.deepcopy(G)    # subgraph we construct by removing from G

    graphOK=True
    deleted_some=True # hack to start off the while loop
    while deleted_some:
        deleted_some=False
        for edge in H.edges():
            (u,v)=edge
            ### Get copy of graph needed for this search
            if low_memory:
                verts=set([u,v])
                for i in range(k):
                    [verts.update(G.neighbors(w)) for w in verts.copy()]
                G2=G.subgraph(list(verts))
            else:
                G2=copy.deepcopy(G)
            ###
            path=[u,v]
            cnt=0
            accept=0
            while path:
                cnt += 1 # Found a path
                if cnt>=l:
                    accept=1
                    break
                # record edges along this graph
                prev=u
                for w in path:
                    if prev!=w:
                        G2.remove_edge(prev,w)
                        prev=w
#                path=shortest_path(G2,u,v,k) # ??? should "Cutoff" be k+1?
                try:
                    path=nx.shortest_path(G2,u,v) # ??? should "Cutoff" be k+1?
                except nx.NetworkXNoPath:
                    path = False
            # No Other Paths
            if accept==0:
                H.remove_edge(u,v)
                deleted_some=True
                if graphOK: graphOK=False
    # We looked through all edges and removed none of them.
    # So, H is the maximal (k,l)-connected subgraph of G
    if same_as_graph:
        return (H,graphOK)
    return H


def is_kl_connected(G, k, l, low_memory=False):
    """Returns ``True`` if and only if ``G`` is locally `(k, l)`-connected.

    A graph is locally `(k, l)`-connected if for each edge `(u, v)` in the
    graph there are at least `l` edge-disjoint paths of length at most `k`
    joining `u` to `v`.

    Parameters
    ----------
    G : NetworkX graph
        The graph to test for local `(k, l)`-connectedness.

    k : integer
        The maximum length of paths to consider. A higher number means a looser
        connectivity requirement.

    l : integer
        The number of edge-disjoint paths. A higher number means a stricter
        connectivity requirement.

    low_memory : bool
        If this is ``True``, this function uses an algorithm that uses slightly
        more time but less memory.

    Returns
    -------
    bool
        Whether the graph is locally `(k, l)`-connected subgraph.

    See also
    --------
    kl_connected_subgraph

    References
    ----------
    .. [1]: Chung, Fan and Linyuan Lu. "The Small World Phenomenon in Hybrid
            Power Law Graphs." *Complex Networks*. Springer Berlin Heidelberg,
            2004. 89--104.

    """
    graphOK=True
    for edge in G.edges():
        (u,v)=edge
        ### Get copy of graph needed for this search
        if low_memory:
            verts=set([u,v])
            for i in range(k):
                [verts.update(G.neighbors(w)) for w in verts.copy()]
            G2=G.subgraph(verts)
        else:
            G2=copy.deepcopy(G)
        ###
        path=[u,v]
        cnt=0
        accept=0
        while path:
            cnt += 1 # Found a path
            if cnt>=l:
                accept=1
                break
            # record edges along this graph
            prev=u
            for w in path:
                if w!=prev:
                    G2.remove_edge(prev,w)
                    prev=w
#            path=shortest_path(G2,u,v,k) # ??? should "Cutoff" be k+1?
            try:
                path=nx.shortest_path(G2,u,v) # ??? should "Cutoff" be k+1?
            except nx.NetworkXNoPath:
                path = False
        # No Other Paths
        if accept==0:
            graphOK=False
            break
    # return status
    return graphOK