"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import {
  Code,
  DollarSign,
  Globe,
  Github
} from "lucide-react";

const buildingFeatures = [
  {
    icon: Code,
    title: "One API, Many Providers",
    description: "Stop juggling multiple APIs, authentication methods, and documentation. Access Google, DeepL, and African language providers through a single, unified interface.",
    status: "In Development"
  },
  {
    icon: DollarSign,
    title: "Fair Pricing",
    description: "Simple, transparent pricing model: provider cost + 10%. No hidden fees, no markup surprises. You pay exactly what the translation costs, plus a small service fee.",
    status: "In Development"
  },
  {
    icon: Globe,
    title: "Under-resourced Languages",
    description: "First-class support for underserved languages, especially African languages through providers like Lelapa AI and Kaya AI. Every language deserves great translation.",
    status: "In Development"
  },
  {
    icon: Github,
    title: "Open Source",
    description: "Community-driven, transparent development. Built in the open with contributions welcome. No vendor lock-in, no black boxes - just honest, open translation infrastructure.",
    status: "Coming Soon"
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
            What We&apos;re{" "}
            <span className="text-black font-extrabold">
              Building
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            We&apos;re creating the missing layer for translation APIs. Here&apos;s what we&apos;re working on
            to make multilingual development simple and fair.
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
              Want to follow our progress?
            </h3>
            <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
              We&apos;re building in the open. Star our repository to get updates on development,
              contribute ideas, or just follow along as we create the future of translation APIs.
            </p>
            <a
              href="https://github.com/yourusername/deka"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 bg-black text-white px-6 py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors"
            >
              <Github className="w-5 h-5" />
              <span>Follow on GitHub</span>
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
