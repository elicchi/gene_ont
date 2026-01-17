import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from OOP.annotations import GAF
from OOP.annotations import Annotation 
from OOP.annotations import ExperimentalAnnotation 
from OOP.annotations import ComputationalAnnotation
from OOP.annotations import CuratedAnnotation
from OOP.ontology import GOterm


class SimilarityCalculator:
    """
    Calculates similarities between GO terms, genes, and annotations
    based on the provided domain models.
    """

    @staticmethod
    def similarity_namespace(term1, term2) :
        """
        Calculates similarity between two namespaces.
        Returns True if identical (e.g., both 'biological_process'), else False.
        """
        return term1.namespace == term2.namespace

    @staticmethod
    def similarity_evidence(ann1, ann2) :
        """
        Calculates similarity between two Evidence categories.
        Uses the polymorphic .category() method from Annotation classes.
        """
        # Exact category match (e.g., "experimental" vs "experimental")
        return ann1.category() == ann2.category()

    @staticmethod
    def similarity_goid(term1, term2) :
        """
        Calculates Semantic Similarity between two GO IDs using Jaccard Index on Ancestors.

        Formula: J(A, B) = |Ancestors(A) ∩ Ancestors(B)| / |Ancestors(A) ∪ Ancestors(B)|
        """

        # Use the get_ancestors method from GOterm class

        ancestors_1 = term1.get_ancestors()
        ancestors_1.add(term1)

        ancestors_2 = term2.get_ancestors()
        ancestors_2.add(term2)

        intersection = len(ancestors_1.intersection(ancestors_2))
        union = len(ancestors_1.union(ancestors_2))

        if union == 0:
            return False

        return intersection / union

    def similarity_between_annotations(self, ann1, ann2):
        """
         similarity between two Annotation objects.
        """

        # GO ID Similarity (Semantic)
        sim_go = self.similarity_goid(ann1.GOterm, ann2.GOterm)

        # Evidence Similarity
        sim_ev = self.similarity_evidence(ann1, ann2)

        # Namespace Similarity
        sim_ns = self.similarity_namespace(ann1.GOterm, ann2.GOterm)


        

        return {
            "goid_semantic_similarity": sim_go,
            "evidence_similarity": sim_ev,
            "namespace_similarity": sim_ns,
            
        }
        
   
