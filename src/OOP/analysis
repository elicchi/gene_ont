import numpy as np
from annotations import GAF

class AnnotationMatrixBuilder:
    """
    Builds annotation matrices from a GAF object.
    """

    def __init__(self, gaf: GAF):
        self.gaf = gaf

    def build(self):
        annotations = self.gaf.annotations

        genes = list({ann.gene_id for ann in annotations})
        terms = list({ann.GOterm.ID for ann in annotations})

        gene_idx = {gene: i for i, gene in enumerate(genes)}
        term_idx = {term: j for j, term in enumerate(terms)}

        matrix = np.zeros((len(genes), len(terms)), dtype=int)

        for ann in annotations:
            i = gene_idx[ann.gene_id]
            j = term_idx[ann.GOterm.ID]
            matrix[i, j] = 1
        return matrix, genes, terms

    def build_for_category(self, category):
        filtered = [ann for ann in self.gaf.annotations if ann.category() == category]
        temp_gaf = GAF()
        for ann in filtered:
            temp_gaf.add_annotation(ann)
        return AnnotationMatrixBuilder(temp_gaf).build()
