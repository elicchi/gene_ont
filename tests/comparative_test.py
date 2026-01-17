# test execution
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from OOP.ontology import GOgraph
from OOP.ontology import GOterm
from OOP.annotations import GAF
from OOP.annotations import Annotation
from OOP.analysis import AnnotationMatrixBuilder
from ontology_test import Row,create_annotation
from comparative.neighborhood import Neighbourhood
from comparative.statistics import Statistics
from comparative.similarity import SimilarityCalculator

graph = GOgraph()

root_bp = GOterm("GO:0008150", "biological_process", "BP", "root")
cell_death = GOterm("GO:0001906", "cell killing", "BP", "cell death")
apoptosis = GOterm("GO:0006915", "apoptotic process", "BP", "programmed cell death")
mol_func = GOterm("GO:0003674", "molecular_function", "MF", "root mf")

graph = GOgraph()
graph.add_term(root_bp)
graph.add_term(cell_death)
graph.add_term(apoptosis)
graph.add_term(mol_func)

graph.add_edge("GO:0008150", "GO:0001906") 
graph.add_edge("GO:0001906", "GO:0006915")

# Create Annotations
gaf = GAF()
row1 = Row("TP53", "GO:0006915", "EXP")  # TP53 -> Apoptosis (Exp)
row2 = Row("TP53", "GO:0001906", "IDA")  # TP53 -> Cell killing (Exp)
row3 = Row("BRCA1", "GO:0008150", "ISS") # BRCA1 -> Bio Process (Comp)
row4 = Row("GENEX", "GO:0003674", "EXP") # GENEX -> Mol Function (Exp)
annotations = []
for r in [row1, row2, row3, row4]:
    ann = create_annotation(r, graph)
    gaf.add_annotation(ann)
    annotations.append(ann)
print(f"Total annotations loaded: {len(gaf.annotations)}")
# output --> Total annotations loaded: 4
  
print("Apoptosis Parent:", apoptosis.parents[0].name)  # → cell killing
#output --> Apoptosis Parent: cell killing

print("Root Children:", [c.name for c in root_bp.children]) # → ['cell killing']
#output --> Root Children: ['cell killing']


#  TEST NEIGHBOURHOOD 
nb = Neighbourhood(graph)

dev_proc = GOterm("GO:0032502", "developmental process", "BP", "dev")
graph.add_term(dev_proc)
graph.add_edge("GO:0008150", "GO:0032502") # root -> dev process

sibs = nb.get_siblings("GO:0001906") # siblings of cell killing
print("Siblings of 'cell killing':", [t.name for t in sibs]) 
#output --> Siblings of 'cell killing': ['developmental process']

desc = nb.get_descendants("GO:0008150") # descendants of root
print("Descendants of 'root':", [t.name for t in desc])
#output --> Descendants of 'root': ['cell killing', 'developmental process', 'apoptotic process']

nb_graph = nb.build_neighbourhood_graph("GO:0008150")
print("Neighbourhood Graph Keys (Root):", list(nb_graph.keys()))
#output --> Neighbourhood Graph Keys (Root): ['GO:0008150', 'GO:0001906', 'GO:0032502', 'GO:0006915']


#  TEST STATISTICS
stats = Statistics(gaf)
final_output = stats.get_summary()
print(f"statistical analysis {final_output}")
# output --> statistical analysis {'GO:0003674': {'go_term': 'GO:0003674', 'num_genes': 1, 'annotations_per_gene_mean': 1.0, 'annotations_per_gene_std': 0.0, 'category_breakdown': {'experimental': 1}}, 'GO:0008150': {'go_term': 'GO:0008150', 'num_genes': 1, 'annotations_per_gene_mean': 1.0, 'annotations_per_gene_std': 0.0, 'category_breakdown': {'computational': 1}}, 'GO:0006915': {'go_term': 'GO:0006915', 'num_genes': 1, 'annotations_per_gene_mean': 1.0, 'annotations_per_gene_std': 0.0, 'category_breakdown': {'experimental': 1}}, 'GO:0001906': {'go_term': 'GO:0001906', 'num_genes': 1, 'annotations_per_gene_mean': 1.0, 'annotations_per_gene_std': 0.0, 'category_breakdown': {'experimental': 1}}}


#  TEST SIMILARITY 
calc = SimilarityCalculator()
# 1. Compare TP53 (Apoptosis, Exp) vs BRCA1 (Root, Comp)
ann_tp53 = annotations[0] 
ann_brca = annotations[2]
print(f"Comparing {ann_tp53.gene_id} ({ann_tp53.GOterm.name}) vs {ann_brca.gene_id} ({ann_brca.GOterm.name})")
#output --> Comparing TP53 (apoptotic process) vs BRCA1 (biological_process)

# Test Semantic Similarity (GO ID)
sim_go = calc.similarity_goid(ann_tp53.GOterm, ann_brca.GOterm)
print(f"GO Semantic Similarity: {sim_go:.4f}")
#output --> GO Semantic Similarity: 0.3333

# Test Namespace Similarity
sim_ns = calc.similarity_namespace(ann_tp53.GOterm, ann_brca.GOterm)
print(f"Namespace Similarity: {sim_ns}")
#output --> Namespace Similarity: True

# Test Evidence Similarity
sim_ev = calc.similarity_evidence(ann_tp53, ann_brca)
print(f"Evidence Similarity: {sim_ev}")
#output --> Evidence Similarity: False

# Test Full Calculation (Should now only have 3 keys)
full_results = calc.similarity_between_annotations(ann_tp53, ann_brca)
print("Full Results Dictionary:", full_results)
#output --> Full Results Dictionary: {'goid_semantic_similarity': 0.3333333333333333, 'evidence_similarity': False, 'namespace_similarity': True}



