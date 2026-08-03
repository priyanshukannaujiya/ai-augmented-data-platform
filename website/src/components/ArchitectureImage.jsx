import React from 'react';

const ArchitectureImage = ({ src, alt, caption }) => {
  return (
    <figure className="my-12">
      <div className="bg-white border border-gray-200 p-2 rounded shadow-sm">
        <a href={src} target="_blank" rel="noopener noreferrer" className="cursor-zoom-in block">
          <img 
            src={src} 
            alt={alt} 
            className="w-full max-w-[1200px] mx-auto h-auto object-contain"
          />
        </a>
      </div>
      {caption && (
        <figcaption className="text-center text-sm text-gray-500 mt-4 font-medium">
          {caption}
        </figcaption>
      )}
    </figure>
  );
};

export default ArchitectureImage;
