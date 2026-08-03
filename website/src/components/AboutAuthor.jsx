import React from 'react';
import profileImg from '../assets/profile.jpg';

const AboutAuthor = () => {
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 my-12 shadow-sm">
      <div className="flex flex-col md:flex-row items-start md:items-center gap-8">
        <div className="flex-shrink-0">
          <img 
            src={profileImg} 
            alt="Priyanshu Premchand Kannaujiya" 
            className="w-48 h-48 object-cover rounded-full border-4 border-white shadow-md mx-auto md:mx-0"
          />
        </div>
        <div className="flex-grow">
          <h2 className="text-3xl font-extrabold text-gray-900 mb-2 border-none">
            Priyanshu Premchand Kannaujiya
          </h2>
          <p className="text-blue-600 font-semibold mb-4 text-lg">
            Data Engineer & AI/ML Enthusiast
          </p>
          
          <div className="space-y-3 text-gray-700 text-sm mb-6">
            <div className="flex items-start">
              <svg className="w-5 h-5 text-gray-400 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"></path></svg>
              <div>
                <strong>BE in Artificial Intelligence & Machine Learning</strong><br/>
                <span className="text-gray-500">Lokmanya Tilak College of Engineering, 2024–2027 (Final Year)</span>
              </div>
            </div>
            <div className="flex items-start">
              <svg className="w-5 h-5 text-gray-400 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path></svg>
              <div>
                <strong>Diploma in Artificial Intelligence & Machine Learning</strong><br/>
                <span className="text-gray-500">MSBTE, 2022–2024 (Grade: A+)</span>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3 border-b pb-1 inline-block border-gray-300">Technical Expertise</h4>
            <div className="flex flex-wrap gap-2">
              <span className="px-2.5 py-1 bg-white border border-gray-300 text-gray-700 text-xs font-bold rounded-md shadow-sm">Python</span>
              <span className="px-2.5 py-1 bg-white border border-gray-300 text-gray-700 text-xs font-bold rounded-md shadow-sm">PySpark</span>
              <span className="px-2.5 py-1 bg-white border border-blue-200 text-blue-800 text-xs font-bold rounded-md shadow-sm">Azure Data Factory</span>
              <span className="px-2.5 py-1 bg-white border border-blue-200 text-blue-800 text-xs font-bold rounded-md shadow-sm">ADLS Gen2</span>
              <span className="px-2.5 py-1 bg-white border border-blue-200 text-blue-800 text-xs font-bold rounded-md shadow-sm">Azure Databricks</span>
              <span className="px-2.5 py-1 bg-white border border-blue-200 text-blue-800 text-xs font-bold rounded-md shadow-sm">Azure Synapse</span>
              <span className="px-2.5 py-1 bg-white border border-orange-200 text-orange-800 text-xs font-bold rounded-md shadow-sm">AWS</span>
              <span className="px-2.5 py-1 bg-white border border-gray-300 text-gray-700 text-xs font-bold rounded-md shadow-sm">Power BI</span>
              <span className="px-2.5 py-1 bg-white border border-gray-300 text-gray-700 text-xs font-bold rounded-md shadow-sm">Medallion Architecture</span>
              <span className="px-2.5 py-1 bg-white border border-gray-300 text-gray-700 text-xs font-bold rounded-md shadow-sm">ETL Pipelines</span>
              <span className="px-2.5 py-1 bg-white border border-gray-300 text-gray-700 text-xs font-bold rounded-md shadow-sm">Data Lakes</span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 font-medium">
            <a href="mailto:kannaujiyapriyanshu111@gmail.com" className="flex items-center hover:text-blue-600 transition-colors">
              <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
              kannaujiyapriyanshu111@gmail.com
            </a>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path></svg>
              +91 9372079707
            </span>
            <a href="https://github.com/priyanshukannaujiya" target="_blank" rel="noopener noreferrer" className="flex items-center hover:text-blue-600 transition-colors">
              <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              GitHub
            </a>
            <a href="https://www.linkedin.com/in/priyanshu-premchand-kannaujiya-355346262/" target="_blank" rel="noopener noreferrer" className="flex items-center hover:text-blue-600 transition-colors">
              <svg className="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
              LinkedIn
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutAuthor;
