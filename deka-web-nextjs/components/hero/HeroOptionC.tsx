/*
  COMMENTED OUT - ORIGINAL HERO DESIGN (LOVED BUT NOT PERFECT FOR SDK)
  This is the beautiful API-flow hero that shows the translation routing concept.
  Keeping it here because we love the design and might use it for API version later.
*/

/*
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
    cost: "Fast & Reliable",
    result: "Bonjour, comment allez-vous ?"
  },
  {
    name: "OpenAI GPT-4",
    color: "bg-green-50 border-green-200",
    textColor: "text-green-700",
    latency: "1.9s",
    cost: "High Quality",
    result: "Bonjour, comment vous portez-vous ?"
  },
  {
    name: "Anthropic Claude",
    color: "bg-purple-50 border-purple-200",
    textColor: "text-purple-700",
    latency: "2.5s",
    cost: "Nuanced",
    result: "Bonjour, comment allez-vous aujourd\\'hui ?"
  },
  {
    name: "GhanaNLP (Twi)",
    color: "bg-orange-50 border-orange-200",
    textColor: "text-orange-700",
    latency: "680ms",
    cost: "African Languages",
    result: "Hello, wo ho te sɛn?"
  },
];

export function HeroOptionC() {*/

// NEW CODE-FIRST HERO FOR SDK
"use client";

import { motion } from "framer-motion";
import { useState, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Terminal, CheckCircle, Github } from "lucide-react";

const codeSteps = [
  "$ pip install deka",
  "",
  "import deka",
  "",
  "# Configure with your API keys",
  "deka.configure({",
  "    'openai_api_key': 'your-key',",
  "    'ghananlp_api_key': 'your-key'",
  "})",
  "",
  "# Compare AI models vs African languages",
  "comparison = deka.compare(",
  "    'Hello, how are you?',",
  "    'twi',",
  "    providers=['openai/gpt-4', 'ghananlp']",
  ")",
  "",
  "# Get the best result",
  "print(comparison.results[0].text)"
];

const results = [
  {
    provider: "OpenAI GPT-4",
    result: "Akwaaba, wo ho te sɛn?",
    speed: "1.9s",
    icon: "🤖"
  },
  {
    provider: "GhanaNLP (Twi)",
    result: "Hello, wo ho te sɛn?",
    speed: "680ms",
    icon: "🌍"
  }
];

export function HeroOptionC() {
  const [currentStep, setCurrentStep] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [typingComplete, setTypingComplete] = useState(false);

  useEffect(() => {
    if (currentStep < codeSteps.length) {
      const timer = setTimeout(() => {
        setCurrentStep(currentStep + 1);
      }, currentStep === 0 ? 1000 : 150); // Slower start, then faster typing
      return () => clearTimeout(timer);
    } else if (!typingComplete) {
      setTypingComplete(true);
      setTimeout(() => setShowResults(true), 500);
    }
  }, [currentStep, typingComplete]);

  return (
    <section className="pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-6"
          >
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              The Only Translation SDK{" "}
              <span className="text-black font-extrabold">
                You&apos;ll Ever Need
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-4xl mx-auto">
              Install once with pip, then access Google Translate, GPT-4, Claude 3.5, Gemini, DeepL,
              and 11 African languages through GhanaNLP. Compare quality and pick the best translation.
            </p>
          </motion.div>
        </div>

        {/* Code-First Demo */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="max-w-6xl mx-auto"
        >
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

            {/* Left Side - Code Terminal */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <Card className="bg-gray-900 border-gray-700 overflow-hidden">
                {/* Terminal Header */}
                <div className="flex items-center space-x-2 px-4 py-3 bg-gray-800 border-b border-gray-700">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <div className="flex items-center space-x-2 ml-4">
                    <Terminal className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-400 text-sm">deka-demo.py</span>
                  </div>
                </div>

                {/* Code Content */}
                <div className="p-6 font-mono text-sm">
                  {codeSteps.slice(0, currentStep).map((line, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.1 }}
                      className={`${
                        line.startsWith('#') ? 'text-gray-400' :
                        line.startsWith('$') ? 'text-green-400' :
                        line.includes('deka') ? 'text-blue-400' :
                        line.includes("'") ? 'text-yellow-400' :
                        'text-gray-300'
                      } leading-relaxed`}
                    >
                      {line || '\u00A0'}
                    </motion.div>
                  ))}
                  {currentStep < codeSteps.length && (
                    <motion.div
                      animate={{ opacity: [1, 0, 1] }}
                      transition={{ duration: 0.8, repeat: Infinity }}
                      className="inline-block w-2 h-5 bg-green-400"
                    />
                  )}
                </div>
              </Card>
            </motion.div>

            {/* Right Side - Results */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="space-y-4"
            >
              <div className="text-center mb-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Translation Results
                </h3>
                <p className="text-gray-600">
                  Compare quality across providers instantly
                </p>
              </div>

              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{
                    opacity: showResults ? 1 : 0.3,
                    y: showResults ? 0 : 20
                  }}
                  transition={{ duration: 0.4, delay: showResults ? index * 0.1 : 0 }}
                >
                  <Card className="p-4 bg-white border-2 border-gray-200 hover:border-gray-300 transition-all">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{result.icon}</span>
                        <div>
                          <h4 className="font-medium text-gray-900">
                            {result.provider}
                          </h4>
                          <span className="text-xs text-gray-500">
                            ⚡ {result.speed}
                          </span>
                        </div>
                      </div>
                      {showResults && (
                        <CheckCircle className="w-5 h-5 text-green-500" />
                      )}
                    </div>

                    <div className="text-gray-700 font-medium">
                      &quot;{result.result}&quot;
                    </div>
                  </Card>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </motion.div>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2 }}
          className="text-center mt-12"
        >
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="https://pypi.org/project/deka/"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 bg-black text-white px-8 py-4 rounded-lg font-medium hover:bg-gray-800 transition-colors text-lg"
            >
              <Terminal className="w-5 h-5" />
              <span>pip install deka</span>
            </a>
            <a
              href="https://github.com/FrejusGdm/deka-project"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 bg-white border-2 border-gray-300 text-gray-900 px-8 py-4 rounded-lg font-medium hover:bg-gray-50 transition-colors text-lg"
            >
              <Github className="w-5 h-5" />
              <span>View on GitHub</span>
            </a>
          </div>

          <p className="text-gray-500 mt-4 text-sm">
            ✅ Live on PyPI • 🎯 6 Providers • 🌍 15+ Models • 🚀 African Languages
          </p>
        </motion.div>
      </div>
    </section>
  );
}

/*
  END OF COMMENTED OUT ORIGINAL HERO
  The original hero code was here - beautiful API flow design that we loved!
  It's preserved above in case we want to use it for an API version later.
*/
