import numpy as np

from OOP.annotations import GAF
from OOP.annotations import Annotation 
from OOP.annotations import ExperimentalAnnotation 
from OOP.annotations import ComputationalAnnotation
from OOP.annotations import CuratedAnnotation
from OOP.ontology import GOterm

class Statistics:
    def __init__(self, gaf):
        """
        gaf.annotations returns a tuple of Annotation objects.
        """
        self.gaf = gaf

    def tc_statistics(self, go_term_id):
        # 1. Access the annotations 
        all_anns = self.gaf.annotations
        
        if not all_anns:
            return "No annotations available"

        # 2. Filter for the specific GO term ID
        term_annotations = [ann for ann in all_anns if ann.GOterm.ID == go_term_id]

        if not term_annotations:
            return f"GO term {go_term_id} not found in annotations."

        # 3. Aggregate data in a single pass using dictionaries
        # gene_counts will store gene_id -> number of annotations
        # cat_summary will store category_name -> count
        gene_counts = {}
        cat_summary = {}

        for ann in term_annotations:
            # Handle Gene Counts
            id = ann.gene_id
            if id in gene_counts:
                gene_counts[id] += 1
            else:
                gene_counts[id] = 1
            
            # Handle Category Summary
            cat = ann.category()
            if cat in cat_summary:
                cat_summary[cat] += 1
            else:
                cat_summary[cat] = 1

        # 4. Extract values for numerical analysis
        counts_per_gene = list(gene_counts.values())

        # 5. Return results
        return {
            "go_term": go_term_id,
            "num_genes": len(gene_counts),
            "annotations_per_gene_mean": round(float(np.mean(counts_per_gene)), 2),
            "annotations_per_gene_std": round(float(np.std(counts_per_gene)), 2),
            "category_breakdown": cat_summary
        }

    def get_summary(self):
        #Returns the master dictionary for all terms in the GAF
        unique_ids = {ann.GOterm.ID for ann in self.gaf.annotations}
        return {go_id: self.tc_statistics(go_id) for go_id in unique_ids}
