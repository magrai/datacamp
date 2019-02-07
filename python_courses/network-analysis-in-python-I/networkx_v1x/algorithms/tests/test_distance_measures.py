#!/usr/bin/env python
from nose.tools import *
import networkx

class TestDistance:

    def setUp(self):
        G=networkx_v1x.Graph()
        from networkx_v1x import convert_node_labels_to_integers as cnlti
        G=cnlti(networkx_v1x.grid_2d_graph(4,4),first_label=1,ordering="sorted")
        self.G=G

    def test_eccentricity(self):
        assert_equal(networkx_v1x.eccentricity(self.G,1),6)
        e=networkx_v1x.eccentricity(self.G)
        assert_equal(e[1],6)
        sp=networkx_v1x.shortest_path_length(self.G)
        e=networkx_v1x.eccentricity(self.G,sp=sp)
        assert_equal(e[1],6)
        e=networkx_v1x.eccentricity(self.G,v=1)
        assert_equal(e,6)
        e=networkx_v1x.eccentricity(self.G,v=[1,1])  #This behavior changed in version 1.8 (ticket #739)
        assert_equal(e[1],6)
        e=networkx_v1x.eccentricity(self.G,v=[1,2])
        assert_equal(e[1],6)
        # test against graph with one node
        G=networkx_v1x.path_graph(1)
        e=networkx_v1x.eccentricity(G)
        assert_equal(e[0],0)
        e=networkx_v1x.eccentricity(G,v=0)
        assert_equal(e,0)
        assert_raises(networkx_v1x.NetworkXError, networkx_v1x.eccentricity, G, 1)
        # test against empty graph
        G=networkx_v1x.empty_graph()
        e=networkx_v1x.eccentricity(G)
        assert_equal(e,{})



        
    def test_diameter(self):
        assert_equal(networkx_v1x.diameter(self.G),6)

    def test_radius(self):
        assert_equal(networkx_v1x.radius(self.G),4)

    def test_periphery(self):
        assert_equal(set(networkx_v1x.periphery(self.G)),set([1, 4, 13, 16]))

    def test_center(self):
        assert_equal(set(networkx_v1x.center(self.G)),set([6, 7, 10, 11]))

    def test_radius_exception(self):
        G=networkx_v1x.Graph()
        G.add_edge(1,2)
        G.add_edge(3,4)
        assert_raises(networkx_v1x.NetworkXError, networkx_v1x.diameter, G)

    @raises(networkx_v1x.NetworkXError)
    def test_eccentricity_infinite(self):
        G=networkx_v1x.Graph([(1,2),(3,4)])
        e = networkx_v1x.eccentricity(G)

    @raises(networkx_v1x.NetworkXError)
    def test_eccentricity_invalid(self):
        G=networkx_v1x.Graph([(1,2),(3,4)])
        e = networkx_v1x.eccentricity(G,sp=1)


