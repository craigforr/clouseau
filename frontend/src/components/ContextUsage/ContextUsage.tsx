import React from 'react';

interface ContextUsageProps {
  used: number;
  total: number;
}

function ContextUsage({ used, total }: ContextUsageProps) {
  const percentage = (used / total) * 100;

  return (
    <div className="context-usage">
      <div className="text-sm text-gray-600">
        Context: {used.toLocaleString()} / {total.toLocaleString()} tokens ({percentage.toFixed(1)}%)
      </div>
    </div>
  );
}

export default ContextUsage;
