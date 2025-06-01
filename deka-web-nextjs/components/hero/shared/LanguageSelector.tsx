"use client";

import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { useState } from "react";

interface Language {
  code: string;
  name: string;
  flag?: string;
}

interface LanguageSelectorProps {
  label: string;
  languages: Language[];
  selected: Language;
  onSelect: (language: Language) => void;
  delay?: number;
}

export function LanguageSelector({ 
  label, 
  languages, 
  selected, 
  onSelect, 
  delay = 0 
}: LanguageSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className="relative"
    >
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between px-4 py-3 bg-white border border-gray-300 rounded-lg hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-colors"
        >
          <div className="flex items-center space-x-2">
            {selected.flag && <span className="text-lg">{selected.flag}</span>}
            <span className="text-gray-900">{selected.name}</span>
          </div>
          <ChevronDown 
            className={`w-4 h-4 text-gray-500 transition-transform ${
              isOpen ? 'rotate-180' : ''
            }`} 
          />
        </button>

        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded-lg shadow-lg z-10 max-h-60 overflow-y-auto"
          >
            {languages.map((language) => (
              <button
                key={language.code}
                onClick={() => {
                  onSelect(language);
                  setIsOpen(false);
                }}
                className="w-full flex items-center space-x-2 px-4 py-3 text-left hover:bg-gray-50 transition-colors"
              >
                {language.flag && <span className="text-lg">{language.flag}</span>}
                <span className="text-gray-900">{language.name}</span>
              </button>
            ))}
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
