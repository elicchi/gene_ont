import gzip
import pandas as pd
from OOP.ontology import GOterm, GOgraph
from OOP.annotations import GAF, ExperimentalAnnotation, ComputationalAnnotation, CuratedAnnotation

def parse_obo(obo_path):
    graph = GOgraph()
    current = None

    with open(obo_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "[Term]":
                current = {}
            elif line.startswith("id: ") and current is not None:
                current['id'] = line[4:]
            elif line.startswith("name: ") and current is not None:
                current['name'] = line[6:]
            elif line.startswith("namespace: ") and current is not None:
                current['namespace'] = line[11:]
            elif line.startswith("def: ") and current is not None:
                current['definition'] = line[5:].split('"')[1] if '"' in line else ''
            elif line.startswith("is_a: ") and current is not None:
                if 'parents' not in current:
                    current['parents'] = []
                parent_id = line[6:].split(" ! ")[0]
                current['parents'].append(parent_id)
            elif line == "" and current is not None and 'id' in current:
                term = GOterm(
                    ID=current['id'],
                    name=current.get('name', ''),
                    namespace=current.get('namespace', ''),
                    definition=current.get('definition', '')
                )

                # temporarily store parent IDs on the term
                term.GOterm_parents = current.get('parents', [])

                graph.add_term(term)
                current = None


    # Add edges
    for term in graph.terms.values():
        for parent_id in getattr(term, "GOterm_parents", []):
            if graph.has_term(parent_id):
                graph.add_edge(parent_id, term.ID)

    return graph


def parse_gaf(gaf_path, go_graph):
    gaf_obj = GAF()

    cols = [1, 2, 4, 6, 8]
    names = ['DB_Object_ID', 'Symbol', 'GO_ID', 'Evidence', 'Aspect']

    df = pd.read_csv(
        gaf_path,
        sep='\t',
        comment='!',
        header=None,
        usecols=cols,
        names=names,
        low_memory=False
    )

    for _, row in df.iterrows():
        go_term = go_graph.get_term(row['GO_ID'])
        if not go_term:
            continue

        evidence = row['Evidence']

        if evidence in {'EXP','IDA','IPI','IMP','IGI','IEP','HDA','HMP','HGI','HEP'}:
            ann = ExperimentalAnnotation(row['Symbol'], go_term)
        elif evidence in {'IEA','ISS','ISO','ISA','ISM','IGC','RCA'}:
            ann = ComputationalAnnotation(row['Symbol'], go_term)
        else:
            ann = CuratedAnnotation(row['Symbol'], go_term)

        gaf_obj.add_annotation(ann)

    return gaf_obj


# Usage
# go_graph = parse_obo("go-basic.obo")
# gaf = parse_gaf("goa_human.gaf.gz", go_graph)
