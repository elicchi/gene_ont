#import the classes
import sys
import os

# Add src folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from OOP.ontology import GOgraph
from OOP.ontology import GOterm
from OOP.annotations import GAF, Annotation, ComputationalAnnotation, ExperimentalAnnotation, CuratedAnnotation
from OOP.analysis import AnnotationMatrixBuilder
#test the classes, methods and functions
def create_annotation(row, go_graph):
    go_term = go_graph.get_term(row.go_id)
    if row.evidence in {"EXP", "IDA", "IPI"}:
        return ExperimentalAnnotation(row.gene_id, go_term)
    elif row.evidence in {"ISS", "IEA"}:
        return ComputationalAnnotation(row.gene_id, go_term)
    else:
        return CuratedAnnotation(row.gene_id, go_term)


# create terms
bp = GOterm("GO:0008150", "biological_process", "BP", "root process")
apoptosis = GOterm("GO:0006915", "apoptotic process", "BP", "cell death process")

# create graph and add terms
graph = GOgraph()
graph.add_term(bp)
graph.add_term(apoptosis)

# add relationship (apoptosis is a child of biological_process)
graph.add_edge("GO:0008150", "GO:0006915")

# check parents/children
print(bp.children[0].name)   # → apoptotic process
print(apoptosis.parents[0].name)  # → biological_process

# gene TP53 annotated to apoptosis
ann1 = ComputationalAnnotation("TP53", graph.get_term("GO:0006915"))
# gene BRCA1 annotated to biological process root
ann2 = CuratedAnnotation("BRCA1", graph.get_term("GO:0008150"))

# create GAF and add annotations
gaf = GAF()
gaf.add_annotation(ann1)
gaf.add_annotation(ann2)
# get all annotations for TP53
tp53_annotations = gaf.get_annotations_by_gene("TP53")

for ann in tp53_annotations:
    print(ann.gene_id, ann.GOterm.name, ann.category())

# Output:
# TP53 apoptotic process experimental

# get annotations for BRCA1
brca_annotations = gaf.get_annotations_by_gene("BRCA1")
for ann in brca_annotations:
    print(ann.gene_id, ann.GOterm.name, ann.category())

# Output:
# BRCA1 biological_process curated

ann = tp53_annotations[0]
print("Gene:", ann.gene_id)
print("Direct GO term:", ann.GOterm.name)

# get parent terms
parents = [p.name for p in ann.GOterm.parents]
print("Parents:", parents)

# Output:
# Gene: TP53
# Direct GO term: apoptotic process
# Parents: ['biological_process']

class Row:
    def __init__(self, gene_id, go_id, evidence):
        self.gene_id = gene_id
        self.go_id = go_id
        self.evidence = evidence

row = Row("TP53", "GO:0006915", "EXP")
ann = create_annotation(row, graph)
gaf.add_annotation(ann)

print(ann.gene_id, ann.GOterm.name, ann.category())
# Output: TP53 apoptotic process experimental


builder = AnnotationMatrixBuilder(gaf)
matrix, genes, terms = builder.build()


tp53 = matrix[genes.index("TP53")]
brca1 = matrix[genes.index("BRCA1")]
