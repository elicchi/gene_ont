from flask import Flask, render_template, request
from parser import parse_obo, parse_gaf
from OOP.analysis import AnnotationMatrixBuilder
from comparative.neighborhood import Neighbourhood
from comparative.similarity import SimilarityCalculator
from comparative.statistics import Statistics
from main import GOSystem

app = Flask(__name__)

# Load system once
obo_path = "data/go-basic.obo"
gaf_path = "data/goa_human.gaf"
system = GOSystem(obo_path, gaf_path)

neighbourhood = Neighbourhood(system.graph)

@app.route("/")
def index():
    return render_template("index.html")


# GO term search with explanation
@app.route("/term", methods=["POST"])
def term():
    go_id = request.form.get("go_id")
    term = system.graph.get_term(go_id)

    if not term:
        return render_template("term.html", error="Invalid GO ID")

    genes = system.get_genes(go_id)

    return render_template(
        "term.html",
        term=term,
        genes=sorted(list(genes))
    )


# Statistics page
@app.route("/stats")
def stats():
    go_id = request.args.get("go_id")
    stats_obj = Statistics(system.gaf)

    if not go_id:
        return render_template("stats.html")  # or a simple form page

    result = stats_obj.tc_statistics(go_id)

    if isinstance(result, str):  # error message
        return render_template("stats.html", error=result)

    return render_template(
        "matrix_single_term.html",  # new template
        stats=result
    )


# GO term comparison
@app.route("/compare", methods=["POST"])
def compare():
    go1 = request.form.get("go1")
    go2 = request.form.get("go2")

    term1 = system.graph.get_term(go1)
    term2 = system.graph.get_term(go2)

    if not term1 or not term2:
        return render_template("compare.html", error="Invalid GO IDs")

    sim = SimilarityCalculator()

    # include evidence similarity:
    # Take one annotation per term as an example (or compute all vs all)
    ann1 = system.gaf.get_annotations_by_gene(go1)
    ann2 = system.gaf.get_annotations_by_gene(go2)

    # fallback if no annotation exists for term
    ev_similarity = None
    if ann1 and ann2:
        # take first annotation for simplicity
        ev_similarity = sim.similarity_evidence(ann1[0], ann2[0])

    result = {
        "same_namespace": sim.similarity_namespace(term1, term2),
        "semantic_similarity": sim.similarity_goid(term1, term2),
        "evidence_similarity": ev_similarity
    }

    return render_template(
        "compare.html",
        term1=term1,
        term2=term2,
        result=result
    )

# Neighbourhood visualization
@app.route("/neighbourhood", methods=["GET", "POST"])
def neighbourhood_view():
    term_id = request.form.get("go_id") if request.method == "POST" else None
    term = system.graph.get_term(term_id) if term_id else None

    if term:
        parents = [p.ID for p in term.parents]
        children = [c.ID for c in term.children]
        siblings = [s.ID for s in neighbourhood.get_siblings(term_id)]
        return render_template(
            "neighbourhood.html",
            term=term,
            parents=parents,
            children=children,
            siblings=siblings,
            term_id=term_id
        )

    return render_template(
        "neighbourhood.html",
        term=None,
        term_id=term_id
    )


if __name__ == "__main__":
    app.run(debug=True)
