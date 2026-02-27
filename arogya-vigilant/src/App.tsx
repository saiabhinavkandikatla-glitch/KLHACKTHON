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
    const [dashboardData, setDashboardData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const response = await fetch('http://localhost:8000/dashboard');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setDashboardData(data);
                setLoading(false);
            } catch (e: any) {
                console.error("Failed to fetch dashboard data", e);
                setError(e.message || "Failed to load dashboard data");
                setLoading(false);
            }
        };
        fetchDashboardData();
    }, []);

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

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center bg-offwhite flex-col gap-4">
                <div className="w-16 h-16 border-4 border-hcblue-200 border-t-hcblue-800 rounded-full animate-spin"></div>
                <h2 className="text-xl font-semibold text-hcblue-900">Loading AI Fraud Analysis...</h2>
                <p className="text-slate-500">Processing claim engines and compiling risk reports</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex h-screen items-center justify-center bg-offwhite flex-col gap-4">
                <div className="bg-white p-8 rounded-lg shadow-md border border-danger-200  max-w-lg text-center">
                    <h2 className="text-xl font-semibold text-danger-700 mb-2">System Error</h2>
                    <p className="text-slate-600 mb-4">{error}</p>
                    <button
                        onClick={() => window.location.reload()}
                        className="bg-hcblue-800 text-white px-4 py-2 rounded font-medium hover:bg-hcblue-900"
                    >
                        Retry Connection
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-offwhite min-h-screen text-slate-800 flex flex-col font-sans">
            <TopNav activeSection={activeSection} />

            <main className="flex-1 w-full">
                <HeroSection data={dashboardData?.hero} />

                <div className="max-w-7xl mx-auto px-6 space-y-16 pb-32">
                    <section id="overview" className="scroll-mt-24">
                        <Overview data={dashboardData?.overview} />
                    </section>

                    <section id="analytics" className="scroll-mt-24">
                        <Analytics data={dashboardData?.analytics} />
                    </section>

                    <section id="providers" className="scroll-mt-24">
                        <ProviderRanking data={dashboardData?.providers} />
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
