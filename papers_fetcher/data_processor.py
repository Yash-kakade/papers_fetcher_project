from typing import List, Dict


class PaperDataProcessor:
    @staticmethod
    def filter_by_non_academic_authors(papers: List[Dict]) -> List[Dict]:
        """Relaxed filter for debugging."""
        # Relax filter: Include all papers for now
        return papers
