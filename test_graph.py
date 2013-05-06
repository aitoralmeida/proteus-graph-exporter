# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:08:55 2013

@author: aitor
"""

from proteus_graph import Graph 
import unittest
import os

class TestSGraph(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('./files'):
            os.makedirs('./files')

    def test_export_csv(self):
        g = Graph(False, "test", {'test_att' : 'string'})    
        g.add_node("node1", ["nodeatt1"], "first node")
        g.add_node("node2", ["nodeatt2"], "second node")
        g.add_node("node3", ["nodeatt3"], "third node")
        g.add_edge('node1', 'node2')
        g.add_edge('node2', 'node3', 'edge2')

        g.export_graph_edgelist_csv('./files/graphCSV.csv')
        with open('./files/graphCSV.csv', 'r') as file:
            i = 0
            for line in file:
                if i == 0:
                    self.assertEquals(line, 'node1;node2\n')
                elif i == 1:
                    self.assertEquals(line, 'node2;node3\n')
                i += 1
                
    def test_export_import_ncol(self):
        g = Graph(False, "test", {'test_att' : 'string'})    
        g.add_node("node1", ["nodeatt1"], "first node")
        g.add_node("node2", ["nodeatt2"], "second node")
        g.add_node("node3", ["nodeatt3"], "third node")
        g.add_edge('node1', 'node2')
        g.add_edge('node2', 'node3', 'edge2')

        g.export_graph_edgelist_ncol('./files/graphNCOL.ncol')
        g2 = Graph()
        g2.import_graph_edgelist_ncol('./files/graphNCOL.ncol')
        
        #no attributes or labels in ncol
        self.assertEquals('node1', g2.nodes['node1'].id)
        self.assertEquals('node2', g2.nodes['node2'].id)
        self.assertEquals('node3', g2.nodes['node3'].id)
        self.assertEquals('node1', g2.edges[0].id_from)
        self.assertEquals('node2', g2.edges[0].id_to)
        self.assertEquals('node2', g2.edges[1].id_from)
        self.assertEquals('node3', g2.edges[1].id_to) 
        
    def test_export_import_gml(self):
        g = Graph(False, "test", {'test_att' : 'string'})    
        g.add_node("node1", ["nodeatt1"], "first node")
        g.add_node("node2", ["nodeatt2"], "second node")
        g.add_node("node3", ["nodeatt3"], "third node")
        g.add_edge('node1', 'node2')
        g.add_edge('node2', 'node3', 'edge2')

        g.export_graph_gml('./files/graphGML.gml')
        g2 = Graph()
        g2.import_graph_gml('./files/graphGML.gml')
        g2.export_graph_gml('./files/graphGML2.gml')
        with open('./files/graphGML.gml', 'r') as fileA:
            with open('./files/graphGML2.gml', 'r') as fileB:
                lineA = fileA.readline()
                while lineA != '':
                    lineB = fileB.readline()
                    self.assertEquals(lineA, lineB)
                    lineA = fileA.readline()
                    
        

if __name__ == '__main__':
    unittest.main()