import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-darkNavbar text-white py-12 mt-20">
      <div className="max-w-article mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <div className="w-6 h-6 bg-blue-500 rounded flex items-center justify-center font-bold text-sm">AI</div>
            <span className="font-bold tracking-tight">AI Data Engineering</span>
          </div>
          <p className="text-gray-400 text-sm leading-relaxed">
            A comprehensive showcase of an enterprise-grade AWS data platform 
            integrating real-time streaming, PySpark ETL, and Agentic AI using 
            Amazon Bedrock and Model Context Protocol.
          </p>
        </div>
        
        <div>
          <h4 className="font-bold mb-4 uppercase text-sm text-gray-300 tracking-wider">Resources</h4>
          <ul className="space-y-2 text-sm text-gray-400">
            <li><a href="#" className="hover:text-white transition-colors">GitHub Repository</a></li>
            <li><a href="#" className="hover:text-white transition-colors">AWS Architecture</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Model Context Protocol</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Apache Airflow DAGs</a></li>
          </ul>
        </div>
        
        <div>
          <h4 className="font-bold mb-4 uppercase text-sm text-gray-300 tracking-wider">Connect</h4>
          <ul className="space-y-2 text-sm text-gray-400">
            <li><a href="#" className="hover:text-white transition-colors">LinkedIn</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Portfolio</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
          </ul>
        </div>
      </div>
      
      <div className="max-w-article mx-auto px-6 mt-12 pt-8 border-t border-gray-800 text-sm text-gray-500 text-center flex flex-col md:flex-row justify-between items-center">
        <p>&copy; {new Date().getFullYear()} AI Data Engineering Platform. All rights reserved.</p>
        <p className="mt-2 md:mt-0">Built with React & Tailwind CSS</p>
      </div>
    </footer>
  );
};

export default Footer;
