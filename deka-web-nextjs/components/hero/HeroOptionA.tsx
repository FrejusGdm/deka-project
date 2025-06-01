"use client";

import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { DemoCard } from "./shared/DemoCard";
import { ProviderBadge } from "./shared/ProviderBadge";
import { ArrowRight, Zap } from "lucide-react";

const providers = [
  { name: "Google Translate", color: "bg-blue-50 text-blue-700", latency: "120ms", cost: "$0.002" },
  { name: "DeepL", color: "bg-indigo-50 text-indigo-700", latency: "180ms", cost: "$0.004" },
  { name: "Lelapa AI", color: "bg-green-50 text-green-700", latency: "250ms", cost: "$0.003" },
  { name: "Kaya AI", color: "bg-orange-50 text-orange-700", latency: "200ms", cost: "$0.003" },
];

const sampleTranslations = {
  "Hello, how are you today?": {
    "Google Translate": "Bonjour, comment allez-vous aujourd'hui ?",
    "DeepL": "Bonjour, comment vous portez-vous aujourd'hui ?",
    "Lelapa AI": "Salut, comment ça va aujourd'hui ?",
    "Kaya AI": "Bonjour, comment vous sentez-vous aujourd'hui ?",
  },
  "Welcome to our platform": {
    "Google Translate": "Bienvenue sur notre plateforme",
    "DeepL": "Bienvenue sur notre plateforme",
    "Lelapa AI": "Bienvenue dans notre plateforme",
    "Kaya AI": "Bienvenue à notre plateforme",
  },
};

export function HeroOptionA() {
  const [inputText, setInputText] = useState("Hello, how are you today?");
  const [isTranslating, setIsTranslating] = useState(false);
  const [showResults, setShowResults] = useState(false);

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

  const currentTranslations = sampleTranslations[inputText as keyof typeof sampleTranslations] || 
    sampleTranslations["Hello, how are you today?"];

  return (
    <section className="pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6"
          >
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              One API to{" "}
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Rule Them All
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Connect to Google, DeepL, and specialized African language providers through a single, 
              unified translation API. Compare outputs, transparent pricing, open source.
            </p>
          </motion.div>

          {/* Provider Badges */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex flex-wrap justify-center gap-3 mb-12"
          >
            {providers.map((provider, index) => (
              <ProviderBadge
                key={provider.name}
                name={provider.name}
                color={provider.color}
                delay={0.3 + index * 0.1}
              />
            ))}
          </motion.div>
        </div>

        {/* Interactive Demo */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-4xl mx-auto"
        >
          {/* Input Section */}
          <div className="bg-white rounded-2xl border border-gray-200 p-8 mb-8 shadow-sm">
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
                    <span>Translating...</span>
                  </>
                ) : (
                  <>
                    <span>Translate</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results Grid */}
          {(showResults || isTranslating) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {providers.map((provider, index) => (
                <DemoCard
                  key={provider.name}
                  title={provider.name}
                  content={
                    isTranslating 
                      ? "Translating..." 
                      : currentTranslations[provider.name] || "Translation not available"
                  }
                  metadata={{
                    latency: provider.latency,
                    cost: provider.cost,
                    confidence: isTranslating ? undefined : "95%"
                  }}
                  delay={isTranslating ? 0 : index * 0.1}
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
