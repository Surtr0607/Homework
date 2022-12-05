def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph


class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """

    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v, w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                + str(self._vertices[1]) + ' : '
                + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class Graph:
    """ Represent a simple graph.

    This version maintains only undirected graphs, and assumes no
    self loops.
    """

    # Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.

    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    # -----------------------------------------------------------------------#

    # ADT methods to query the graph

    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])  # the dict of edges for v
        return num // 2  # divide by 2, since each edege appears in the
        # vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                and v in self._structure
                and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    # ----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.

        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements.

        Args:
            elist - a list of pairs of vertex objects
        """
        for (v, w) in elist:
            self.add_edge(v, w, None)


class Vertex:
    """ A Vertex in a graph. """

    def __init__(self, value, key=None, index=None):
        self._key = key
        self._element = value
        self._index = index

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self.getKey() < v.getKey()

    def element(self):
        """ Return the data for the vertex. """
        return self._element

    def __hash__(self):
        return id(self)

    def getKey(self):
        return self._key

    def setKey(self, newkey):
        self._key = newkey

    def setIndex(self, index):
        self._index = index

    def getIndex(self):
        return self._index


class PriorityQueue:
    def __init__(self, filename):
        self.priorityQueue = []
        self.graph = graphreader(filename)

    def getList(self):
        return self.priorityQueue

    def add(self, key, value):
        v = self.graph.get_vertex_by_label(value)
        v.setKey(key)
        index = self.length()
        v.setIndex(index)
        self.priorityQueue.append(v)
        while (index-1)//2 >= 0:
            if self.priorityQueue[index]< self.priorityQueue[(index-1)//2]:
                temp_vertex = self.priorityQueue[index]
                self.priorityQueue[index] = self.priorityQueue[(index-1)//2]
                self.priorityQueue[(index - 1) // 2] = temp_vertex
                self.priorityQueue[(index - 1) // 2].setIndex((index - 1) // 2)
                self.priorityQueue[index].setIndex(index)
            index = (index-1)//2
        return v

    def min(self):
        # Read first element in array and return
        if self.is_empty():
            return None
        else:
            temp = self.priorityQueue[0]
            return temp.getKey(), temp.getValue()

    def remove_min(self):
        # Remove and return the value with the minimum key
        if self.length() == 1:
            temp = self.priorityQueue[0]
            self.priorityQueue.pop(0)
            return temp
        else:
            temp_element = self.priorityQueue[0]
            self.priorityQueue[0] = self.priorityQueue[self.length()-1]
            self.priorityQueue[self.length()-1] = temp_element
            self.priorityQueue[self.length()-1].setIndex(self.length()-1)
            self.priorityQueue[0].setIndex(0)
            self.priorityQueue.pop()
            index = 0
            while index*2+1 <= self.length()-1:
                if self.priorityQueue[index*2+1] < self.priorityQueue[index]:
                    temp = self.priorityQueue[index]
                    self.priorityQueue[index] = self.priorityQueue[index*2+1]
                    self.priorityQueue[index*2+1] = temp
                    self.priorityQueue[index*2+1].setIndex(index*2+1)
                    self.priorityQueue[index].setIndex(index)
                    if index*2+2 <= self.length()-1:
                        if self.priorityQueue[index * 2 + 2] < self.priorityQueue[index]:
                            temp = self.priorityQueue[index]
                            self.priorityQueue[index] = self.priorityQueue[index * 2 + 2]
                            self.priorityQueue[index * 2 + 2] = temp
                            self.priorityQueue[index * 2 + 2].setIndex(index * 2 + 2)
                            self.priorityQueue[index].setIndex(index)
                index = index*2+1
            # Return popped (key,value) pair
            return temp_element

    def is_empty(self):
        if len(self.priorityQueue) is 0:
            return True
        return False

    def length(self):
        return len(self.priorityQueue)

    def update_key(self, element, newkey):
        element.setKey(newkey)

    def get_key(self, element):
        return element.getKey()

    def get_graph(self):
        return self.graph


class Dijkastra:
    def __init__(self, filename):
        self.preds = dict()
        self.locs = dict()
        # locs is a empty dictionary(keys are vertices and values are location in open)
        self.closed = dict()
        # closed starts as an empty dictionary
        self.open = PriorityQueue(filename)
        self.graph = self.open.get_graph()

    def process(self, s):
        # s is a element
        newcost = 0
        temp = self.open.add(0, s)
        self.locs[temp] = 0
        self.preds[temp] = None
        # preds starts as a dictionary with value for s = None
        while self.open.length() is not 0:

            current = self.open.remove_min()

            del self.locs[current]
            self.closed[current.element()] = (current.getKey(), self.preds[current].__str__())
            del self.preds[current]
            for e in self.graph.get_edges(current):
                w = e.opposite(current)
                if w.element() not in self.closed:
                    newcost = current.getKey() + e.element()
                    if w not in self.locs:
                        self.preds[w] = current
                        temp = self.open.add(newcost, w.element())
                        self.locs[w] = w.getIndex()
                    elif newcost < self.open.get_key(w):
                        self.preds[w] = current
                        self.open.update_key(w, newcost)
        return self.closed

    def get_graph(self):
        return self.graph


a = Dijkastra('simplegraph2.txt')
graph = a.get_graph()
print(a.process(1))
