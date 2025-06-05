"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { Zap, Target, Globe, Code, ArrowRight } from "lucide-react";

const benefits = [
  {
    id: "model-selection",
    icon: Target,
    title: "AI Model Selection",
    subtitle: "Choose specific models",
    description: "First translation SDK with AI model selection. Choose GPT-4 for quality, Claude 3.5 Sonnet for nuance, or Gemini 2.0 Flash for speed. Optimize for your exact needs.",
    features: [
      "15+ AI models available",
      "OpenAI, Anthropic, Gemini support",
      "Speed vs quality optimization",
      "Future-proof model validation"
    ],
    codeExample: `// Choose specific AI models
import deka

// High quality with GPT-4
result = deka.translate("Hello", "french", provider="openai/gpt-4")

// Fast with Claude Haiku
result = deka.translate("Hello", "spanish", provider="anthropic/claude-3-haiku")

// Latest with Gemini 2.0
result = deka.translate("Hello", "german", provider="google-gemini/gemini-2.0-flash")`
  },
  {
    id: "african-languages",
    icon: Globe,
    title: "African Language Support",
    subtitle: "11 African languages ready",
    description: "Dedicated GhanaNLP integration provides authentic translations for Ghanaian and African languages. Real translations tested and working for Twi, Ga, Ewe, Yoruba, and more.",
    features: [
      "11 African languages supported",
      "GhanaNLP provider integration",
      "Authentic cultural translations",
      "Ghanaian language specialization"
    ],
    codeExample: `# Real African language translations
import deka
deka.configure({'ghananlp_api_key': 'your-key'})

# Twi (Ghana)
result = deka.translate("Thank you", "twi", provider="ghananlp")
print(result.text)  # "Meda wo ase"

# Yoruba (Nigeria)
result = deka.translate("Good morning", "yoruba", provider="ghananlp")
print(result.text)  # "Ẹ káàárọ̀"`
  },
  {
    id: "unified-api",
    icon: Code,
    title: "Unified Python SDK",
    subtitle: "One interface for all providers",
    description: "Single Python SDK for 6 translation providers. No more juggling multiple APIs, authentication methods, and documentation. Install once, use everywhere.",
    features: [
      "6 providers: Google, DeepL, OpenAI, Anthropic, Gemini, GhanaNLP",
      "Unified authentication system",
      "Consistent response format",
      "Available on PyPI right now"
    ],
    codeExample: `# One SDK, multiple providers
import deka

# Configure once
deka.configure({
    'openai_api_key': 'your-key',
    'ghananlp_api_key': 'your-key'
})

# Use any provider
result = deka.translate("Hello", "french", provider="google")
result = deka.translate("Hello", "twi", provider="ghananlp")
result = deka.translate("Hello", "spanish", provider="openai/gpt-4")`
  },
  {
    id: "comparison",
    icon: Zap,
    title: "Provider Comparison",
    subtitle: "Compare quality and speed",
    description: "Built-in comparison across providers and models. See side-by-side results with performance metrics. Choose the best translation for your needs.",
    features: [
      "Multi-provider comparison",
      "Model performance metrics",
      "Response time tracking",
      "Async concurrent execution"
    ],
    codeExample: `# Compare providers and models
comparison = deka.compare("Hello world", "french", providers=[
    "google",
    "openai/gpt-4",
    "anthropic/claude-3-5-sonnet",
    "ghananlp"
])

for result in comparison.results:
    model = result.metadata.get('model', 'default')
    print(f"{result.provider} ({model}): {result.text}")
    print(f"  Response time: {result.response_time_ms}ms")

# Find fastest provider
print(f"Fastest: {comparison.fastest_provider}")`
  },
];

export function WhyDeka() {
  const [activeTab, setActiveTab] = useState("model-selection");
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
            Deka is live on PyPI! The most advanced Python translation SDK with model selection,
            African language support, and provider comparison built-in.
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
            <div className="text-3xl font-bold text-gray-900">6</div>
            <div className="text-gray-600">Translation Providers</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-gray-900">15+</div>
            <div className="text-gray-600">AI Models Available</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-gray-900">11</div>
            <div className="text-gray-600">African Languages</div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
