from flask import Flask, render_template, request
from parser import parse_obo, parse_gaf
from OOP.analysis import AnnotationMatrixBuilder
from statistics_module import Statistics  
from system import GOSystem               

app = Flask(__name__)

# Load system once (important for performance)
obo_path = "data/go-basic.obo"
gaf_path = "data/goa_human.gaf.gz"
system = GOSystem(obo_path, gaf_path)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/genes", methods=["POST"])
def genes():
    go_id = request.form.get("go_id")
    genes = system.get_genes(go_id)

    return render_template(
        "genes.html",
        go_id=go_id,
        genes=sorted(list(genes)) if genes else []
    )


@app.route("/stats")
def stats():
    matrix, genes, terms = system.annotation_matrix()
    stats_obj = Statistics(system.gaf, matrix, genes, terms)
    summary = stats_obj.ann_statistics()

    return render_template("stats.html", stats=summary)


if __name__ == "__main__":
    app.run(debug=True)
