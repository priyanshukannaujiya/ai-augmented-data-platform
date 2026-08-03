import React from 'react';

const ArticleHeader = () => {
  return (
    <header className="py-12 mb-8 text-center max-w-4xl mx-auto border-b border-gray-100">
      <div className="text-sm font-bold text-blue-600 mb-4 tracking-wider uppercase">
        DATA ENGINEERING • AWS • AGENTIC AI
      </div>
      
      <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6 leading-tight">
        AI-Augmented E-Commerce Data Engineering Platform on AWS
      </h1>
      
      <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
        Building an Enterprise Data Platform with Kafka, AWS Glue, PySpark,
        Apache Airflow, Amazon Athena, Bedrock and Model Context Protocol
      </p>
      
      <div className="inline-block bg-gray-100 rounded-full px-4 py-1 text-sm font-semibold text-gray-700 mb-8">
        End-to-End Data Engineering Project
      </div>
      
      <div className="flex flex-wrap justify-center gap-2 mt-2">
        {['AWS', 'Python', 'Kafka', 'PySpark', 'Airflow', 'Bedrock', 'MCP'].map(tag => (
          <span key={tag} className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-bold rounded">
            {tag}
          </span>
        ))}
      </div>
    </header>
  );
};

export default ArticleHeader;
