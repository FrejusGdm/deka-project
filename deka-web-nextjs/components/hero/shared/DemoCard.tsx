"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

interface DemoCardProps {
  title: string;
  content: string;
  metadata?: {
    latency?: string;
    cost?: string;
    confidence?: string;
  };
  delay?: number;
  className?: string;
}

export function DemoCard({ title, content, metadata, delay = 0, className = "" }: DemoCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
      className={className}
    >
      <Card className="p-4 border border-gray-200 hover:border-gray-300 transition-colors">
        <div className="space-y-3">
          {/* Provider/Language Header */}
          <div className="flex items-center justify-between">
            <h3 className="font-medium text-gray-900">{title}</h3>
            {metadata?.confidence && (
              <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full">
                {metadata.confidence}
              </span>
            )}
          </div>

          {/* Translation Content */}
          <div className="text-gray-700 text-sm leading-relaxed">
            {content}
          </div>

          {/* Metadata */}
          {metadata && (metadata.latency || metadata.cost) && (
            <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-gray-100">
              {metadata.latency && (
                <span>⚡ {metadata.latency}</span>
              )}
              {metadata.cost && (
                <span>💰 {metadata.cost}</span>
              )}
            </div>
          )}
        </div>
      </Card>
    </motion.div>
  );
}
