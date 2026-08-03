import React from 'react';

const TechTable = ({ data, columns }) => {
  return (
    <div className="overflow-x-auto my-8">
      <table className="min-w-full bg-white border border-gray-200 shadow-sm rounded">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-200">
            {columns.map((col, idx) => (
              <th key={idx} className="py-3 px-6 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.map((row, idx) => (
            <tr key={idx} className="hover:bg-gray-50 transition-colors">
              {Object.values(row).map((val, vIdx) => (
                <td key={vIdx} className="py-3 px-6 text-sm text-gray-700">
                  {val}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TechTable;
