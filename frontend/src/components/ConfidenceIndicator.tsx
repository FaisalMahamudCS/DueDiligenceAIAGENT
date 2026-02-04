/**
 * Confidence Indicator Component
 *
 * Visual indicator for answer confidence scores (0.0 to 1.0).
 */

interface ConfidenceIndicatorProps {
  confidence: number; // 0.0 to 1.0
  showLabel?: boolean;
}

export default function ConfidenceIndicator({
  confidence,
  showLabel = true
}: ConfidenceIndicatorProps) {
  // TODO: Implement confidence indicator component
  // - Display progress bar or gauge
  // - Color coding (red/yellow/green)
  // - Show percentage or score
  // - Optional label

  const percentage = Math.round(confidence * 100);
  const color = confidence >= 0.7 ? 'green' : confidence >= 0.4 ? 'yellow' : 'red';

  return (
    <div className="confidence-indicator">
      {showLabel && <span>Confidence: </span>}
      <div className={`confidence-bar confidence-${color}`} style={{ width: `${percentage}%` }}>
        {percentage}%
      </div>
    </div>
  );
}


