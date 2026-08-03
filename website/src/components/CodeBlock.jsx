import React from 'react';

const CodeBlock = ({ code, language = 'text' }) => {
  return (
    <div className="my-6 rounded-md overflow-hidden bg-[#1e1e1e] shadow-md border border-gray-800">
      <div className="bg-gray-800 px-4 py-2 text-xs font-mono text-gray-400 border-b border-gray-700 flex justify-between items-center">
        <span>{language}</span>
      </div>
      <pre className="p-4 overflow-x-auto text-sm text-gray-200 font-mono">
        <code>{code}</code>
      </pre>
    </div>
  );
};

export default CodeBlock;
