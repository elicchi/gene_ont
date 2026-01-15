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

tests/ # Development tests
