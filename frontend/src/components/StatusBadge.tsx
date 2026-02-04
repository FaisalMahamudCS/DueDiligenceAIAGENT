/**
 * Status Badge Component
 *
 * Reusable component for displaying status badges (project status, answer
 * review status, request status).
 */

interface StatusBadgeProps {
  status: string;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
}

export default function StatusBadge({ status, variant = 'default' }: StatusBadgeProps) {
  // TODO: Implement status badge component
  // - Display status text
  // - Apply color based on variant
  // - Support different status types

  return (
    <span className={`status-badge status-badge-${variant}`}>
      {status}
    </span>
  );
}


