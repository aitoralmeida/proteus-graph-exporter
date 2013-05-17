# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 10:46:10 2013

@author: aitor
"""

from time import gmtime, strftime
import csv

class Graph:
    def __init__(self, directed=False, description = '', node_attributes = []):
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
    
    def add_node(self, id, node_attributes = [], label = ""):
        if not self.node_exists(id):
            node = Node(id, node_attributes, label)
            self.nodes[id] = node
    
    def add_edge(self, id_from, id_to, label = ""):
        self.edges.append(Edge(id_from, id_to, label))

    def node_exists(self, id): 
        if id in self.nodes:
            return True
        else:
            return False
            
    def export_graph_gexf(self, file_path):
        with open(file_path, 'w') as f:
            # header
            f.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
            f.write("""<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2"\n>""")
            
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
                    f.write('            <attribute id="' + str(i)  + '" title="' + att[0] + '" type="' + att[1] + '"/>\n' )
                    i += 1   
                f.write('        </attributes>\n')
                
            #nodes
            f.write('        <nodes>\n')
            for node in self.nodes.values():
                # right niow the id and label of the node are the same
                f.write('        <node id="' + node.id  + '" label="'+ node.label +'">\n')
                if len(node.attributes) > 0:
                    f.write('            <attvalues>\n')
                    i = 0
                    for att in node.attributes:
                        f.write('             <attvalue for="' + str(i) +'" value="' + att + '"/>\n')
                        i += 1
                    f.write('            </attvalues>\n')
                f.write('        </node>\n')            
            f.write('        </nodes>\n')
            
            #edges
            f.write('        <edges>\n')
            i = 0
            for edge in self.edges:
                f.write('            <edge id="' + str(i) + '" source="' +  edge.id_from + '" target="' + edge.id_to + '"/>\n')
                i += 1
                
            f.write('        </edges>\n')
            f.write('    </graph>\n')
            f.write('</gexf>\n')
            
    def export_graph_edgelist_csv(self, file_path):
        with open(file_path, 'wb') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            for rel in self.edges:
                writer.writerow([rel.id_from, rel.id_to]) 
    
    def export_graph_edgelist_ncol(self, file_path):
         with open(file_path, 'w') as file:
              for rel in self.edges:
                  file.write(str(rel.id_from).replace(' ', '_') + " " + str(rel.id_to).replace(' ', '_') + "\n")
    
    def import_graph_edgelist_ncol(self, file_path):     
        with open(file_path, 'r') as file:
            nodes = set()
            for line in file: 
                line = line.strip()
                n = line.split(' ')
                nodes.add(n[0])
                nodes.add(n[1])
                self.add_edge(n[0], n[1])
            
            for node in nodes:
                self.add_node(node)
                
    def export_graph_edgelist_fanmod(self, file_path):
         with open(file_path, 'w') as file:
              for rel in self.edges:
                  file.write(str(rel.id_from).replace(' ', '_') + " " + str(rel.id_to).replace(' ', '_') + " 1\n")
  
    def export_graph_gml(self, file_path):
        with open(file_path, 'w') as file:
            file.write('graph\n')
            file.write('[\n')
            for node in self.nodes.values():
                file.write('    node\n')
                file.write('    [\n')
                file.write('        id ' + str(node.id) + '\n')
                file.write('        label "' + node.label + '"\n')
                file.write('    ]\n')
            
            for edge in self.edges:
                file.write('    edge\n')
                file.write('    [\n')
                file.write('        source ' + str(edge.id_from) + '\n')
                file.write('        target ' + str(edge.id_to) + '\n')
                file.write('        label "' + edge.label + '"\n')
                file.write('    ]\n')
                
            file.write(']\n')
            
    def import_graph_gml(self, file_path):
        with open(file_path, 'r') as file:
            node_data = False
            edge_data = False
            ID = ''
            label = ''
            source = ''
            target = ''
            for line in file: 
                line = line.strip()
                if 'node' in line and len(line.split(' ')) == 1:
                    node_data = True
                    edge_data = False
                    ID = ''
                    label = ''
                    source = ''
                    target = ''
                elif 'edge' in line and len(line.split(' ')) == 1:
                    edge_data = True
                    node_data = False
                    ID = ''
                    label = ''
                    source = ''
                    target = ''
                elif 'id' in line:
                    ID = line.split()[1]
                elif 'label' in line:
                    label = line.split('"')[1]
                elif 'source' in line:
                     source = line.split()[1]
                elif 'target' in line:
                    target = line.split()[1]
                elif ']' in line:
                    if node_data:
                        self.add_node(id=ID, label=label)
                        node_data = False
                    elif edge_data:
                        self.add_edge(source, target, label)
                        edge_data = False
        
class Node:
    def __init__(self, id, attributes, label):
        self.id = id
        self.label = label
        self.attributes = attributes

class Edge:
    def __init__(self, id_from, id_to, label=""):
        self.label = label
        self.id_from = id_from
        self.id_to = id_to

    
    