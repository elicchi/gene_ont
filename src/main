from parser import parse_obo, parse_gaf
from OOP.analysis import AnnotationMatrixBuilder

class GOSystem:
    def __init__(self, obo_path, gaf_path):
        self.graph = parse_obo(obo_path)
        self.gaf = parse_gaf(gaf_path, self.graph)

    def get_genes(self, go_id):
        term = self.graph.get_term(go_id)
        return self.gaf.get_genes_for_term(term) if term else set()

    def annotation_matrix(self):
        builder = AnnotationMatrixBuilder(self.gaf)
        return builder.build()


if __name__ == "__main__":
    # Relative paths
    obo_path = "data/go-basic.obo"
    gaf_path = "data/goa_human.gaf"

    system = GOSystem(obo_path, gaf_path)
