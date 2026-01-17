from flask import Flask, render_template, request
from parser import parse_obo, parse_gaf
from OOP.analysis import AnnotationMatrixBuilder
from comparative.similarity import SimilarityCalculator
from comparative.statistics import Statistics
from main import GOSystem

app = Flask(__name__)

# Load system once
obo_path = "data/go-basic.obo"
gaf_path = "data/goa_human.gaf"
system = GOSystem(obo_path, gaf_path)


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
        return render_template("stats.html")
        
    result = stats_obj.tc_statistics(go_id)
    
    if isinstance(result, str):
        return render_template(
            "stats.html",
            go_id=go_id,
            error=result
        )
        
    return render_template(
        "stats.html",
        go_id=go_id,
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

    result = {
        "same_namespace": sim.similarity_namespace(term1, term2),
        "semantic_similarity": sim.similarity_goid(term1, term2)
    }

    return render_template(
        "compare.html",
        term1=term1,
        term2=term2,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
