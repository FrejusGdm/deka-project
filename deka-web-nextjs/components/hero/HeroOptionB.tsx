"use client";

import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { DemoCard } from "./shared/DemoCard";
import { LanguageSelector } from "./shared/LanguageSelector";
import { ArrowRight, Zap, ArrowRightLeft } from "lucide-react";

const languages = [
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "fr", name: "French", flag: "🇫🇷" },
  { code: "yo", name: "Yoruba", flag: "🇳🇬" },
  { code: "zu", name: "Zulu", flag: "🇿🇦" },
  { code: "ha", name: "Hausa", flag: "🇳🇬" },
  { code: "sw", name: "Swahili", flag: "🇰🇪" },
];

const sampleTranslations = {
  "en-fr": {
    input: "Hello, how are you today?",
    outputs: [
      { provider: "Google", text: "Bonjour, comment allez-vous aujourd'hui ?", latency: "120ms", cost: "$0.002" },
      { provider: "DeepL", text: "Bonjour, comment vous portez-vous aujourd'hui ?", latency: "180ms", cost: "$0.004" },
      { provider: "Lelapa AI", text: "Salut, comment ça va aujourd'hui ?", latency: "250ms", cost: "$0.003" },
    ]
  },
  "en-yo": {
    input: "Welcome to our platform",
    outputs: [
      { provider: "Google", text: "Kaabo si ẹrọ wa", latency: "140ms", cost: "$0.002" },
      { provider: "Lelapa AI", text: "Ẹ ku abọ si pẹpẹ wa", latency: "200ms", cost: "$0.003" },
      { provider: "Kaya AI", text: "Kaabo si ile-iṣẹ wa", latency: "180ms", cost: "$0.003" },
    ]
  },
  "en-zu": {
    input: "Thank you very much",
    outputs: [
      { provider: "Google", text: "Ngiyabonga kakhulu", latency: "130ms", cost: "$0.002" },
      { provider: "Lelapa AI", text: "Siyabonga kakhulu", latency: "190ms", cost: "$0.003" },
      { provider: "Kaya AI", text: "Ngiyabonga kakhulu", latency: "170ms", cost: "$0.003" },
    ]
  },
};

export function HeroOptionB() {
  const [sourceLanguage, setSourceLanguage] = useState(languages[0]);
  const [targetLanguage, setTargetLanguage] = useState(languages[1]);
  const [inputText, setInputText] = useState("Hello, how are you today?");
  const [isTranslating, setIsTranslating] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const translationKey = `${sourceLanguage.code}-${targetLanguage.code}` as keyof typeof sampleTranslations;
  const currentTranslation = sampleTranslations[translationKey] || sampleTranslations["en-fr"];

  const handleTranslate = () => {
    setIsTranslating(true);
    setShowResults(false);
    
    setTimeout(() => {
      setIsTranslating(false);
      setShowResults(true);
    }, 1500);
  };

  useEffect(() => {
    // Auto-trigger translation on mount
    setTimeout(() => {
      handleTranslate();
    }, 1000);
  }, []);

  useEffect(() => {
    // Update input text when translation changes
    setInputText(currentTranslation.input);
  }, [currentTranslation]);

  return (
    <section className="pt-24 pb-16 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6"
          >
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Compare{" "}
              <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                Every Provider
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              See side-by-side translations from multiple providers. Compare quality, speed, and cost 
              to choose the best result for your needs.
            </p>
          </motion.div>
        </div>

        {/* Interactive Demo */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-5xl mx-auto"
        >
          {/* Input Section */}
          <div className="bg-white rounded-2xl border border-gray-200 p-8 mb-8 shadow-sm">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              <LanguageSelector
                label="From"
                languages={languages}
                selected={sourceLanguage}
                onSelect={setSourceLanguage}
                delay={0.1}
              />
              
              <div className="flex items-end justify-center">
                <motion.div
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                  className="p-3 bg-gray-100 rounded-full"
                >
                  <ArrowRightLeft className="w-5 h-5 text-gray-600" />
                </motion.div>
              </div>

              <LanguageSelector
                label="To"
                languages={languages.filter(lang => lang.code !== sourceLanguage.code)}
                selected={targetLanguage}
                onSelect={setTargetLanguage}
                delay={0.3}
              />
            </div>

            <div className="flex flex-col sm:flex-row gap-4 items-end">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Text to translate
                </label>
                <Input
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Enter text to translate..."
                  className="text-lg py-3"
                />
              </div>
              <button
                onClick={handleTranslate}
                disabled={isTranslating}
                className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
              >
                {isTranslating ? (
                  <>
                    <Zap className="w-4 h-4 animate-pulse" />
                    <span>Comparing...</span>
                  </>
                ) : (
                  <>
                    <span>Compare</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results Grid */}
          {(showResults || isTranslating) && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {currentTranslation.outputs.map((output, index) => (
                <DemoCard
                  key={output.provider}
                  title={output.provider}
                  content={
                    isTranslating 
                      ? "Translating..." 
                      : output.text
                  }
                  metadata={{
                    latency: output.latency,
                    cost: output.cost,
                    confidence: isTranslating ? undefined : `${90 + Math.floor(Math.random() * 10)}%`
                  }}
                  delay={isTranslating ? 0 : index * 0.15}
                  className={isTranslating ? "animate-pulse" : ""}
                />
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </section>
  );
}
