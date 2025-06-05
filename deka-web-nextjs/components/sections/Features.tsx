"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import {
  Code,
  Target,
  Globe,
  Zap,
  Github
} from "lucide-react";

const buildingFeatures = [
  {
    icon: Target,
    title: "Model Selection",
    description: "First translation SDK with AI model selection. Choose specific models like GPT-4, Claude 3.5 Sonnet, or Gemini 2.0 Flash. Optimize for speed, quality, or cost.",
    status: "✅ Live"
  },
  {
    icon: Globe,
    title: "African Languages",
    description: "Dedicated support for 11 African languages via GhanaNLP integration. Authentic translations for Twi, Ga, Ewe, Yoruba, Kikuyu, and more Ghanaian and African languages.",
    status: "✅ Live"
  },
  {
    icon: Code,
    title: "6 Providers Ready",
    description: "Google Translate, DeepL, OpenAI (5 models), Anthropic (5 models), Google Gemini (5 models), and GhanaNLP. All through a single, unified Python interface.",
    status: "✅ Live"
  },
  {
    icon: Zap,
    title: "Future-Proof Design",
    description: "Permissive model validation means you can try new models as soon as providers release them. No waiting for SDK updates - just use the latest models immediately.",
    status: "✅ Live"
  }
];

export function Features() {
  return (
    <section id="features" className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            What We&apos;ve{" "}
            <span className="text-black font-extrabold">
              Built
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Deka is live on PyPI! Here&apos;s what you can use right now to make
            multilingual development simple and powerful.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {buildingFeatures.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="group"
              >
                <Card className="p-8 h-full bg-white border-2 border-gray-200 hover:border-gray-300 hover:shadow-lg transition-all duration-300">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center group-hover:bg-gray-200 transition-colors">
                        <Icon className="w-6 h-6 text-gray-700" />
                      </div>
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="text-xl font-bold text-gray-900">
                          {feature.title}
                        </h3>
                        <span className="inline-block px-3 py-1 bg-gray-100 text-gray-600 text-xs font-medium rounded-full">
                          {feature.status}
                        </span>
                      </div>

                      <p className="text-gray-600 leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center mt-16"
        >
          <div className="bg-gray-50 border-2 border-gray-200 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Ready to get started?
            </h3>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              Deka is available on PyPI right now. Install it, configure your API keys,
              and start translating with model selection and African language support.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <div className="bg-black text-white px-6 py-3 rounded-lg font-mono text-sm">
                pip install deka
              </div>
              <a
                href="https://github.com/FrejusGdm/deka-project"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-2 bg-white border-2 border-gray-300 text-gray-900 px-6 py-3 rounded-lg font-medium hover:bg-gray-50 transition-colors"
              >
                <Github className="w-5 h-5" />
                <span>View on GitHub</span>
              </a>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
