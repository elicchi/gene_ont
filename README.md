# project

Project structure:

src/

├── parser/ # Part 1: OBO and GAF parsing ()

├── OOP/ # Part 2: Ontology representation and analysis

│ ├── ontology.py # GOterm, GOgraph

│ ├── annotations.py # Annotation hierarchy and GAF

│ └── analysis.py # NumPy-based numerical representations

├── comparative/ # Part 3: Analytical and comparative computations

│ ├── similarity.py # similarity metrics(between terms,annotations)

│ ├── neighborhood.py # GO graph neighborhood, sibling/descendant computations

│ └──  statistics.py # Annotation statistics(mean,median,std)

├── main #Part 2: Integration

├── app/ # Part 4: User Interface

├── data/ # The GO and GAF files

├── templates/ # Part 4: User Interface

tests/ # Development tests

The project report can be found in the code files under the name "Gene Ontology Analysis System"

## Required data files

The following files are required but not included due to GitHub size limits:

- go-basic.obo
  
- goa_human.gaf.gz


Download from: https://current.geneontology.org/ontology/go-basic.obo and: https://current.geneontology.org/annotations/goa_human.gaf.gz

Place them in the `data/` folder.

## How to start the app

- Install Flask

- Open a terminal inside the src folder and run:

python app.py

- Open in browser:

http://127.0.0.1:5000/
