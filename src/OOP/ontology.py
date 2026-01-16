class GOterm:
    def __init__(self, ID, name, namespace, definition, comment=None, **kwargs):
        self.__ID=ID
        self.__name=name
        self.__namespace=namespace
        self.__definition=definition
        self.__comment=comment
        
        #ontology structure
        self.__parents=[]
        self.__children=[]
        
    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def namespace(self):
        return self.__namespace

    @property
    def definition(self):
        return self.__definition

    @property
    def parents(self):
        return tuple(self.__parents)

    @property
    def children(self):
        return tuple(self.__children)
    
    def __add_parent(self, parent):
        if parent not in self.__parents:
            self.__parents.append(parent)

    def __add_child(self, child):
        if child not in self.__children:
            self.__children.append(child)

    def get_ancestors(self):
        ancestors = set()
        stack = list(self.parents)

        while stack:
            term = stack.pop()
            if term not in ancestors:
                ancestors.add(term)
                stack.extend(term.parents)

        return ancestors

class GOgraph:
    def __init__(self):
        self.__terms={}
    
    @property
    def terms(self):
        return dict(self.__terms)

    def add_term(self,term: GOterm):
        self.__terms[term.ID]=term
        
    def add_edge(self, parent_id, child_id):
        parent = self.__terms[parent_id]
        child = self.__terms[child_id]

        parent._GOterm__add_child(child)
        child._GOterm__add_parent(parent)
    
    def get_term(self,term_id):
        return self.__terms.get(term_id)
    
    def has_term(self, term_id):
        return term_id in self.__terms
