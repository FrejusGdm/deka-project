"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { Zap, DollarSign, Globe, Code, ArrowRight } from "lucide-react";

const benefits = [
  {
    id: "unified-api",
    icon: Code,
    title: "One API Instead of Many",
    subtitle: "No more API chaos",
    description: "Stop juggling multiple APIs, documentation, and authentication methods. Deka provides a single, unified interface to access all major translation providers.",
    features: [
      "Single REST endpoint for all providers",
      "Unified authentication system",
      "Consistent response format",
      "No need to read multiple docs"
    ],
    codeExample: `// Before: Multiple APIs
const googleResult = await google.translate(text);
const deeplResult = await deepl.translate(text);
const lelapaResult = await lelapa.translate(text);

// After: One API
const results = await deka.translate({
  text: "Hello world",
  providers: ["google", "deepl", "lelapa"]
});`
  },
  {
    id: "african-languages",
    icon: Globe,
    title: "Specialized in Niche Languages",
    subtitle: "African languages included",
    description: "Access African language providers like Lelapa AI and Kaya AI alongside global giants. Perfect for Yoruba, Zulu, Hausa, and other underserved languages.",
    features: [
      "50+ African languages supported",
      "Native provider integrations",
      "Cultural context preservation",
      "Regional dialect support"
    ],
    codeExample: `// Translate to African languages
const result = await deka.translate({
  text: "Welcome to our platform",
  source: "en",
  target: "yo", // Yoruba
  provider: "lelapa"
});

// Result: "Ẹ ku abọ si pẹpẹ wa"`
  },
  {
    id: "transparent-pricing",
    icon: DollarSign,
    title: "Fair & Transparent Pricing",
    subtitle: "Provider cost + 10%",
    description: "Simple pricing model: provider cost + 10%. No hidden fees, no markup surprises. You pay exactly what you use with full cost transparency.",
    features: [
      "Real-time cost calculation",
      "Per-character pricing",
      "No hidden fees or markups",
      "Prepaid wallet system"
    ],
    codeExample: `{
  "text": "Hello world",
  "characters": 11,
  "provider_cost": "$0.0011",
  "deka_fee": "$0.0001",
  "total_cost": "$0.0012",
  "wallet_balance": "$24.9988"
}`
  },
  {
    id: "comparison",
    icon: Zap,
    title: "Compare Before You Choose",
    subtitle: "Quality comparison built-in",
    description: "See side-by-side results from multiple providers with latency and cost metrics. Make informed decisions about quality vs. speed vs. price.",
    features: [
      "Side-by-side comparisons",
      "Quality confidence scores",
      "Latency and cost metrics",
      "Best result recommendations"
    ],
    codeExample: `// Compare multiple providers
const comparison = await deka.compare({
  text: "Hello world",
  source: "en",
  target: "fr",
  providers: ["google", "deepl", "lelapa"]
});

// Returns results with metrics for each`
  },
];

export function WhyDeka() {
  const [activeTab, setActiveTab] = useState("unified-api");
  const activeBenefit = benefits.find(b => b.id === activeTab) || benefits[0];

  return (
    <section id="why-deka" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Why Choose{" "}
            <span className="text-black font-extrabold">
              Deka?
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Translation shouldn't be complicated. We've built the missing layer that makes 
            working with multiple translation providers simple, fair, and powerful.
          </p>
        </motion.div>

        {/* Tab Navigation */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          viewport={{ once: true }}
          className="flex flex-wrap justify-center gap-2 mb-12"
        >
          {benefits.map((benefit) => (
            <button
              key={benefit.id}
              onClick={() => setActiveTab(benefit.id)}
              className={`px-6 py-3 text-sm font-medium rounded-lg transition-all duration-300 ${
                activeTab === benefit.id
                  ? "bg-black text-white"
                  : "bg-gray-100 text-gray-600 hover:bg-gray-200"
              }`}
            >
              {benefit.title}
            </button>
          ))}
        </motion.div>

        {/* Content Area */}
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start"
        >
          {/* Left Side - Description */}
          <div className="space-y-6">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-black rounded-xl flex items-center justify-center">
                <activeBenefit.icon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-gray-900">{activeBenefit.title}</h3>
                <p className="text-sm text-gray-500 font-medium">{activeBenefit.subtitle}</p>
              </div>
            </div>

            <p className="text-lg text-gray-600 leading-relaxed">
              {activeBenefit.description}
            </p>

            <div className="space-y-3">
              {activeBenefit.features.map((feature, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <ArrowRight className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">{feature}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Side - Code Example */}
          <div className="bg-gray-900 rounded-2xl p-6 overflow-hidden">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
            <pre className="text-sm text-gray-300 overflow-x-auto">
              <code>{activeBenefit.codeExample}</code>
            </pre>
          </div>
        </motion.div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-20 grid grid-cols-1 sm:grid-cols-3 gap-8 text-center"
        >
          <div className="space-y-2">
            <div className="text-3xl font-bold text-gray-900">5+</div>
            <div className="text-gray-600">Translation Providers</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-gray-900">50+</div>
            <div className="text-gray-600">Supported Languages</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-gray-900">100%</div>
            <div className="text-gray-600">Open Source</div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
