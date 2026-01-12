 # --- TEST EXECUTION ---
if __name__ == "__main__":
    system = GeneOntologySystem()

    # INPUT: Provide the paths to the official files you downloaded
    system.load_data("go-basic.obo", "goa_human.gaf.gz")

    # Verification: Query the term for 'Apoptotic Process'
    test_id = "GO:0006915"
    result = system.get_info(test_id)

    print("\n--- OFFICIAL DATA TEST ---")
    print(f"GO ID: {test_id}")
    print(f"Name: {result['name']}")
    print(f"Total Genes Annotated: {result['gene_count']}")
    print(f"Sample Genes: {result['sample_genes']}")
