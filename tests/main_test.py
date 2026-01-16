import sys
import os

# Add src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import GOSystem
from OOP.analysis import AnnotationMatrixBuilder
from comparative.statistics import Statistics

if __name__ == "__main__":
    # Relative paths
    obo_path = "data/go-basic.obo"
    gaf_path = "data/goa_human.gaf"

    system = GOSystem(obo_path, gaf_path)

    # --- Test genes ---
    genes = system.get_genes("GO:0006915")
    print("Apoptosis genes:", len(genes))
    print("Sample genes:", list(genes)[:5])

    # --- Test annotation matrix ---
    builder = AnnotationMatrixBuilder(system.gaf)
    matrix, gene_list, term_list = builder.build()
    print("Matrix shape:", matrix.shape)
    print("First 5 genes:", gene_list[:5])
    print("First 5 terms:", term_list[:5])

    # --- Test category-specific matrix ---
    matrix_exp, genes_exp, terms_exp = builder.build_for_category("experimental")
    print("Experimental matrix shape:", matrix_exp.shape)

    # --- Test statistics ---
    stats = Statistics(system.gaf, matrix, gene_list, term_list)
    print("\nTerm count statistics:")
    stats.tc_statistics()

    print("\nAnnotation statistics:")
    ann_summary = stats.ann_statistics()
    print(ann_summary)
