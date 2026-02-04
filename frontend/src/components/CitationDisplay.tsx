/**
 * Citation Display Component
 *
 * Displays citations with document references, page numbers, and bounding
 * box information.
 */

interface Citation {
  document_id: string;
  document_name: string;
  chunk_text: string;
  page_number: number;
  bounding_box?: {
    x0: number;
    y0: number;
    x1: number;
    y1: number;
  };
  relevance_score?: number;
}

interface CitationDisplayProps {
  citations: Citation[];
}

export default function CitationDisplay({ citations }: CitationDisplayProps) {
  // TODO: Implement citation display component
  // - Display list of citations
  // - Show document name and page number
  // - Display chunk text preview
  // - Show relevance score
  // - Click to highlight in document viewer
  // - Support bounding box visualization

  return (
    <div className="citations">
      <h3>Citations</h3>
      {citations.map((citation, index) => (
        <div key={index} className="citation-item">
          <p>{citation.document_name} - Page {citation.page_number}</p>
          <p className="citation-text">{citation.chunk_text}</p>
        </div>
      ))}
    </div>
  );
}


