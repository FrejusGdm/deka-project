"use client";

import { motion } from "framer-motion";

interface ProviderBadgeProps {
  name: string;
  logo?: string;
  color?: string;
  delay?: number;
}

export function ProviderBadge({ name, logo, color = "bg-gray-100", delay = 0 }: ProviderBadgeProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay }}
      className={`inline-flex items-center px-3 py-1.5 rounded-full text-sm font-medium ${color} text-gray-800 border border-gray-200`}
    >
      {logo && (
        <div className="w-4 h-4 mr-2 rounded-full bg-gray-300 flex items-center justify-center">
          <span className="text-xs font-bold">{name.charAt(0)}</span>
        </div>
      )}
      {name}
    </motion.div>
  );
}
