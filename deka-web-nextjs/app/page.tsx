import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { HeroOptionC } from "@/components/hero/HeroOptionC";
import { WhyDeka } from "@/components/sections/WhyDeka";
import { Features } from "@/components/sections/Features";
import { CTA } from "@/components/sections/CTA";

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Header />

      <main>
        {/* Hero Option C - LiteLLM-style Flow */}
        <HeroOptionC />

        {/* Why Deka Section */}
        <WhyDeka />

        {/* Features Section */}
        <Features />

        {/* CTA Section */}
        <CTA />
      </main>

      <Footer />
    </div>
  );
}
