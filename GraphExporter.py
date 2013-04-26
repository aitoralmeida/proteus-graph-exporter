# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:46:10 2013

@author: aitor
"""

from time import gmtime, strftime
import csv
from sets import Set


class Graph:
    def __init__(self, directed=False, description = '', node_attributes = {}):
        if directed:
            self.type = 'directed'
        else:
            self.type = 'undirected'
    
        self.creator = 'Graph_exporter'
        self.description = description
        self.modified = strftime("%Y-%m-%d", gmtime())
        self.node_attributes = node_attributes
        self.nodes = {}
        self.edges = []
    
    def add_node(self, id, node_attributes = []):
        self.nodes[id] = node_attributes
    
    def add_edge(self, id_from, id_to):
        self.edges.append([id_from, id_to])

    def node_exists(self, id):
        if id in self.nodes.keys:
            return True
        else:
            return False
            
    def export_graph_gefx(self, file_path):
        with open(file_path, 'w') as f:
            # header
            f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
            f.write("""<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2"\n""")
            
            # metadata
            f.write('    <meta lastmodifieddate="' + self.modified + '">\n')
            f.write('        <creator>' + self.creator + '</creator>\n')
            f.write('        <description>' + self.description + '</description>\n')
            f.write('    </meta>\n')
            
            #graph
            f.write('    <graph defaultedgetype="' + self.type +'">\n')
            
            #attributes
            if len(self.node_attributes) > 0:
                f.write('        <attributes class="node">\n')
                i = 0
                for att in self.node_attributes:
                    f.write('            <attribute id="' + str(i)  + '" title="' + att + " type=" + self.node_attributes[att] + '"/>\n' )
                    i += 1   
                f.write('        </attributes>\n')
                
            #nodes
            f.write('        <nodes>\n')
            for node in self.nodes:
                # right niow the id and label of the node are the same
                f.write('        <node id="' + node  + '" label="'+ node +'">\n')
                if len(self.nodes[node]) > 0:
                    f.write('            <attvalues>\n')
                    i = 0
                    for att in self.nodes[node]:
                        f.write('             <attvalue for="' + str(i) +'" value="' + att + '"/>\n')
                        i += 1
                    f.write('            </attvalues>\n')
                f.write('        </node>\n')            
            f.write('        </nodes>\n')
            
            #edges
            f.write('        <edges>\n')
            i = 0
            for edge in self.edges:
                f.write('            <edge id="' + str(i) + '" source="' +  edge[0] + '" target="' + edge[1] + '"/>\n')
                i += 1
                
            f.write('        </edges>\n')
            f.write('    </graph>\n')
            f.write('</gexf>\n')
            
    def export_graph_csv(self, file_path):
        with open(file_path, 'wb') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            for rel in self.edges:
                writer.writerow(rel) 
    
    def export_graph_ncol(self, file_path):
         with open(file_path, 'w') as file:
              for rel in self.edges:
                  file.write(str(rel[0]).replace(' ', '_') + " " + str(rel[1]).replace(' ', '_') + "\n")
    
    def import_graph_ncol(self, file_path):
        with open(file_path, 'r') as file:
            nodes = []
            for line in file: 
                line = line.strip()
                n = line.split(' ')
                nodes.append(n[0])
                nodes.append(n[1])
                self.add_edge(n[0], n[1])
            
            s = Set(nodes)
            for node in s:
                self.add_node(node)
                
    def export_graph_edgelist_fanmod(self, file_path):
         with open(file_path, 'w') as file:
              for rel in self.edges:
                  file.write(str(rel[0]).replace(' ', '_') + " " + str(rel[1]).replace(' ', '_') + " 1\n")
  
if __name__ == "__main__":
    g = Graph(False, "test", {'test_att' : 'string'})    
    g.add_node("node1", ["nodeatt1"])
    g.add_node("node2", ["nodeatt2"])
    g.add_edge('node1', 'node2')
    
    print 'Exporting csv'
    g.export_graph_csv('./files/graphCSV.csv')
    print 'Exporting ncol'
    g.export_graph_ncol('./files/graphNCOL.txt')
    print 'Exporting GEFX'
    g.export_graph_gefx('./files/graphGEFX.gefx')    
    
    print 'importing graph'
    g2 = Graph()
    g2.import_graph_ncol('./files/graphNCOL.txt')
    g2.export_graph_ncol('./files/graphNCOL2.txt')
    g2.export_graph_gefx('./files/graphGEFX2.gefx') 
    
    
    