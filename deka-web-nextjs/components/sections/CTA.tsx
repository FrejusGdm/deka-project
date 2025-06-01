"use client";

import { motion } from "framer-motion";
import { Github, BookOpen, ArrowRight, Star } from "lucide-react";
import Link from "next/link";

export function CTA() {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-6">
            Ready to{" "}
            <span className="text-black font-extrabold">
              Get Started?
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Join the open source community building the future of translation APIs. 
            Start translating in minutes, not hours.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* GitHub CTA */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
          >
            <Link
              href="https://github.com/your-username/deka"
              target="_blank"
              rel="noopener noreferrer"
              className="group block"
            >
              <div className="bg-gray-900 text-white rounded-2xl p-8 hover:bg-gray-800 transition-colors h-full">
                <div className="flex items-center space-x-3 mb-4">
                  <Github className="w-8 h-8" />
                  <h3 className="text-2xl font-bold">Star on GitHub</h3>
                </div>
                
                <p className="text-gray-300 mb-6 leading-relaxed">
                  Explore the source code, contribute to the project, and help us build 
                  the best translation API for everyone.
                </p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 text-sm text-gray-400">
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4" />
                      <span>Open Source</span>
                    </div>
                    <div>MIT License</div>
                  </div>
                  
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </Link>
          </motion.div>

          {/* Documentation CTA */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <Link
              href="/docs/getting-started"
              className="group block"
            >
              <div className="bg-blue-50 border-2 border-blue-200 rounded-2xl p-8 hover:border-blue-300 transition-colors h-full">
                <div className="flex items-center space-x-3 mb-4">
                  <BookOpen className="w-8 h-8 text-blue-600" />
                  <h3 className="text-2xl font-bold text-gray-900">Read the Docs</h3>
                </div>
                
                <p className="text-gray-600 mb-6 leading-relaxed">
                  Get started with our comprehensive documentation, API reference, 
                  and step-by-step integration guides.
                </p>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <div>Quick Start</div>
                    <div>API Reference</div>
                    <div>Examples</div>
                  </div>
                  
                  <ArrowRight className="w-5 h-5 text-blue-600 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            </Link>
          </motion.div>
        </div>

        {/* Quick Start Code Example */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          viewport={{ once: true }}
          className="mt-16 max-w-3xl mx-auto"
        >
          <div className="text-center mb-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Get started in seconds
            </h3>
            <p className="text-gray-600">
              Simple REST API that works with any programming language
            </p>
          </div>

          <div className="bg-gray-900 rounded-xl p-6 overflow-x-auto">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="text-gray-400 text-sm ml-2">Quick Start</span>
            </div>
            
            <pre className="text-green-400 text-sm font-mono leading-relaxed">
{`curl -X POST https://api.deka.dev/translate \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "Hello, world!",
    "source": "en",
    "target": "yo",
    "provider": "auto"
  }'`}
            </pre>
          </div>
        </motion.div>

        {/* Community Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <p className="text-gray-500 mb-4">Trusted by developers worldwide</p>
          <div className="flex justify-center items-center space-x-8 text-sm text-gray-400">
            <div>🌟 Open Source</div>
            <div>🚀 Fast & Reliable</div>
            <div>🌍 Global Community</div>
            <div>💰 Fair Pricing</div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
