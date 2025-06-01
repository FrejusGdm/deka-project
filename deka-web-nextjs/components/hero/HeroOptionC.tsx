"use client";

import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ArrowRight, Zap, User, Globe } from "lucide-react";

const providers = [
  { 
    name: "Google Translate", 
    color: "bg-blue-50 border-blue-200", 
    textColor: "text-blue-700",
    latency: "120ms", 
    cost: "$0.002",
    result: "Bonjour, comment allez-vous ?"
  },
  { 
    name: "DeepL", 
    color: "bg-indigo-50 border-indigo-200", 
    textColor: "text-indigo-700",
    latency: "180ms", 
    cost: "$0.004",
    result: "Bonjour, comment vous portez-vous ?"
  },
  { 
    name: "Lelapa AI", 
    color: "bg-green-50 border-green-200", 
    textColor: "text-green-700",
    latency: "250ms", 
    cost: "$0.003",
    result: "Salut, comment ça va ?"
  },
  { 
    name: "Kaya AI", 
    color: "bg-orange-50 border-orange-200", 
    textColor: "text-orange-700",
    latency: "200ms", 
    cost: "$0.003",
    result: "Bonjour, comment vous sentez-vous ?"
  },
];

export function HeroOptionC() {
  const [inputText, setInputText] = useState("Hello, how are you?");
  const [isTranslating, setIsTranslating] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [animationStep, setAnimationStep] = useState(0);

  const handleTranslate = () => {
    setIsTranslating(true);
    setShowResults(false);
    setAnimationStep(0);
    
    // Animate the flow
    setTimeout(() => setAnimationStep(1), 300);  // Input to Deka
    setTimeout(() => setAnimationStep(2), 800);  // Deka to providers
    setTimeout(() => setAnimationStep(3), 1300); // Show results
    setTimeout(() => {
      setIsTranslating(false);
      setShowResults(true);
    }, 1800);
  };

  useEffect(() => {
    // Auto-trigger translation on mount
    setTimeout(() => {
      handleTranslate();
    }, 1000);
  }, []);

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
              <span className="text-black font-extrabold">
                Rule Them All
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Connect to Google, DeepL, and specialized African language providers through a single, 
              unified translation API. Compare outputs, transparent pricing, open source.
            </p>
          </motion.div>
        </div>

        {/* Interactive Flow Diagram */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-6xl mx-auto relative"
        >
          {/* SVG for curved arrows - positioned absolutely */}
          <svg
            className="absolute inset-0 w-full h-full pointer-events-none z-0"
            viewBox="0 0 1200 500"
            preserveAspectRatio="xMidYMid meet"
          >
            {/* First curved arrow: Input to Deka */}
            <motion.path
              d="M 280 250 Q 420 180 580 250"
              stroke="currentColor"
              strokeWidth="3"
              fill="none"
              className="text-gray-300"
              strokeDasharray="12,6"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{
                pathLength: animationStep >= 1 ? 1 : 0,
                opacity: animationStep >= 1 ? 1 : 0.3
              }}
              transition={{ duration: 1.2, delay: 0.3 }}
            />
            <motion.polygon
              points="570,245 580,250 570,255"
              fill="currentColor"
              className="text-gray-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: animationStep >= 1 ? 1 : 0.3 }}
              transition={{ delay: 1.2 }}
            />

            {/* Second curved arrow: Deka to Results */}
            <motion.path
              d="M 620 250 Q 760 320 920 250"
              stroke="currentColor"
              strokeWidth="3"
              fill="none"
              className="text-gray-300"
              strokeDasharray="12,6"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{
                pathLength: animationStep >= 2 ? 1 : 0,
                opacity: animationStep >= 2 ? 1 : 0.3
              }}
              transition={{ duration: 1.2, delay: 0.5 }}
            />
            <motion.polygon
              points="910,245 920,250 910,255"
              fill="currentColor"
              className="text-gray-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: animationStep >= 2 ? 1 : 0.3 }}
              transition={{ delay: 1.4 }}
            />
          </svg>

          <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">

            {/* User Input Section */}
            <div className="lg:col-span-3">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                <Card className="p-6 bg-white border-2 border-gray-200 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                      <User className="w-5 h-5 text-gray-600" />
                    </div>
                    <h3 className="font-semibold text-gray-900">Your Input</h3>
                  </div>

                  <Input
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    placeholder="Enter text to translate..."
                    className="mb-4 border-gray-200 focus:border-gray-400"
                  />

                  <button
                    onClick={handleTranslate}
                    disabled={isTranslating}
                    className="w-full px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 disabled:opacity-50 transition-colors flex items-center justify-center space-x-2"
                  >
                    {isTranslating ? (
                      <>
                        <Zap className="w-4 h-4 animate-pulse" />
                        <span>Processing...</span>
                      </>
                    ) : (
                      <>
                        <span>Translate</span>
                        <ArrowRight className="w-4 h-4" />
                      </>
                    )}
                  </button>
                </Card>
              </motion.div>
            </div>

            {/* Spacer for curved arrow */}
            <div className="lg:col-span-2 hidden lg:block"></div>

            {/* Deka API Center */}
            <div className="lg:col-span-3">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{
                  opacity: 1,
                  scale: animationStep >= 1 ? 1.05 : 1,
                }}
                transition={{ duration: 0.6, delay: 0.6 }}
              >
                <Card className="p-8 bg-gray-50 border-2 border-gray-300 shadow-lg hover:shadow-xl transition-shadow relative overflow-hidden">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-black rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                      <Globe className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">Deka API</h3>
                    <p className="text-gray-600 text-sm mb-4">Translation Meta-Router</p>

                    {/* Processing indicators */}
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="bg-white border border-gray-200 rounded px-2 py-1">
                        <span className="text-gray-600 font-medium">Routing</span>
                      </div>
                      <div className="bg-white border border-gray-200 rounded px-2 py-1">
                        <span className="text-gray-600 font-medium">Comparing</span>
                      </div>
                      <div className="bg-white border border-gray-200 rounded px-2 py-1">
                        <span className="text-gray-600 font-medium">Optimizing</span>
                      </div>
                      <div className="bg-white border border-gray-200 rounded px-2 py-1">
                        <span className="text-gray-600 font-medium">Aggregating</span>
                      </div>
                    </div>
                  </div>

                  {/* Animated pulse effect */}
                  {isTranslating && (
                    <motion.div
                      className="absolute inset-0 bg-gray-200 rounded-lg"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: [0, 0.1, 0] }}
                      transition={{ duration: 1, repeat: Infinity }}
                    />
                  )}
                </Card>
              </motion.div>
            </div>

            {/* Spacer for curved arrow */}
            <div className="lg:col-span-1 hidden lg:block"></div>

            {/* Provider Results */}
            <div className="lg:col-span-3">
              <div className="grid grid-cols-1 gap-4">
                {providers.map((provider, index) => (
                  <motion.div
                    key={provider.name}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{
                      opacity: animationStep >= 3 ? 1 : 0.3,
                      x: animationStep >= 3 ? 0 : 20
                    }}
                    transition={{ duration: 0.4, delay: 0.1 * index }}
                  >
                    <Card className="p-4 bg-white border-2 border-gray-200 shadow-sm hover:shadow-md transition-all">
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <h4 className="font-medium text-gray-900">
                            {provider.name}
                          </h4>
                          {showResults && (
                            <span className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded-full">
                              ✓
                            </span>
                          )}
                        </div>

                        <div className="text-sm text-gray-700">
                          {showResults ? provider.result : "Translating..."}
                        </div>

                        {showResults && (
                          <div className="flex justify-between text-xs text-gray-500 pt-2 border-t border-gray-200">
                            <span>⚡ {provider.latency}</span>
                            <span>💰 {provider.cost}</span>
                          </div>
                        )}
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
