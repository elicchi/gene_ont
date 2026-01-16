class GAF:
    def __init__(self):
        self.__annotations=[]
        self.__by_gene={}
    @property
    def annotations(self):
        return tuple(self.__annotations)
    
    def add_annotation(self,annotation):
        self.__annotations.append(annotation)
        if annotation.gene_id not in self.__by_gene:
            self.__by_gene[annotation.gene_id]=[]
        self.__by_gene[annotation.gene_id].append(annotation)
    
    def get_genes_for_term(self, term):
        genes = set()

        for ann in self.annotations:
            if ann.GOterm == term or term in ann.GOterm.get_ancestors():
                genes.add(ann.gene_id)

        return genes
    
    #query methods
    def get_annotations_by_gene(self, gene_id):
        return list(self.__by_gene.get(gene_id, []))
    
    def get_annotations_by_category(self, category):
        return [ann for ann in self.annotations if ann.category() == category]
    
    #summarisation methods
    def count_annotations_per_gene(self):
        return {gene: len(anns) for gene, anns in self.__by_gene.items()}
    
    def count_by_category(self):
        summary = {}
        for ann in self.annotations:
            cat = ann.category()
            summary[cat] = summary.get(cat, 0) + 1
        return summary



from abc import ABC, abstractmethod
class Annotation(ABC):
    def __init__(self, gene_id, GOterm):
        self.__gene_id=gene_id
        self.__GOterm=GOterm
    
    @property
    def gene_id(self):
        return self.__gene_id
    
    @property
    def GOterm(self):
        return self.__GOterm
    
    @abstractmethod
    def category(self):
        pass
    
class ExperimentalAnnotation(Annotation):
    def category(self):
        return "experimental"

class ComputationalAnnotation(Annotation):
    def category(self):
        return "computational"

class CuratedAnnotation(Annotation):
    def category(self):
        return "curated"
