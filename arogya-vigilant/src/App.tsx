import React, { useState, useEffect } from 'react';
import TopNav from './components/TopNav';
import HeroSection from './components/HeroSection';
import Overview from './components/Overview';
import Analytics from './components/Analytics';
import ProviderRanking from './components/ProviderRanking';
import AnomalyDetection from './components/AnomalyDetection';
import DocumentInvestigation from './components/DocumentInvestigation';

function App() {
    const [activeSection, setActiveSection] = useState('overview');

    useEffect(() => {
        const handleScroll = () => {
            const sections = ['overview', 'analytics', 'providers', 'upload'];

            let current = '';
            for (const section of sections) {
                const element = document.getElementById(section);
                if (element) {
                    const rect = element.getBoundingClientRect();
                    if (rect.top <= 150) {
                        current = section;
                    }
                }
            }
            if (current && current !== activeSection) {
                setActiveSection(current);
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, [activeSection]);

    return (
        <div className="bg-offwhite min-h-screen text-slate-800 flex flex-col font-sans">
            <TopNav activeSection={activeSection} />

            <main className="flex-1 w-full">
                <HeroSection />

                <div className="max-w-7xl mx-auto px-6 space-y-16 pb-32">
                    <section id="overview" className="scroll-mt-24">
                        <Overview />
                    </section>

                    <section id="analytics" className="scroll-mt-24">
                        <Analytics />
                    </section>

                    <section id="providers" className="scroll-mt-24">
                        <ProviderRanking />
                    </section>

                    <section id="upload" className="scroll-mt-24">
                        <DocumentInvestigation />
                    </section>
                </div>
            </main>
        </div>
    );
}

export default App;
