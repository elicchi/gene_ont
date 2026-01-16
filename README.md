# project

Project structure:

src/

├── parsing/ # Part 1: OBO and GAF parsing ()

├── OOP/ # Part 2: Ontology representation and analysis

│ ├── ontology.py # GOterm, GOgraph

│ ├── annotations.py # Annotation hierarchy and GAF

│ └── analysis.py # NumPy-based numerical representations

├── comparative/              # Part 3: Analytical and comparative computations

│ ├── similarity.py         # similarity metrics(between terms,annotations)

│ ├── neighborhood.py       # GO graph neighborhood, sibling/descendant computations

│ └──  statistics.py         # Annotation statistics(mean,median,std)

├── main #Paart 2: Integration

├── data/ # The GO and GAF files

tests/ # Development tests

## Required data files

The following files are required but not included due to GitHub size limits:

- go-basic.obo
  
- goa_human.gaf.gz


Download from: https://current.geneontology.org/ontology/go-basic.obo and: https://current.geneontology.org/annotations/goa_human.gaf.gz

Place them in the `data/` folder.
