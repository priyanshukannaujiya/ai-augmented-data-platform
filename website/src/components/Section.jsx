import React from 'react';

const Section = ({ title, children, noMargin }) => {
  return (
    <section className={`max-w-4xl mx-auto ${noMargin ? '' : 'mb-16'}`}>
      {title && (
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6 border-b-2 border-blue-500 pb-2 inline-block">
          {title}
        </h2>
      )}
      <div className="text-gray-700 leading-relaxed text-lg space-y-6">
        {children}
      </div>
    </section>
  );
};

export default Section;
