import React from 'react';
import { ShieldCheck, Users, AlertTriangle } from 'lucide-react';

const HeroSection = () => {
    return (
        <div className="bg-white border-b border-slate-200 pt-16 pb-12 mb-12">
            <div className="max-w-7xl mx-auto px-6">
                <div className="max-w-3xl mb-12">
                    <h2 className="text-4xl font-extrabold text-hcblue-900 tracking-tight mb-4">
                        AI-Powered Fraud Intelligence
                    </h2>
                    <p className="text-lg text-slate-600 leading-relaxed">
                        Protecting public healthcare funds through continuous deep-learning analysis,
                        proactively identifying anomalous billing patterns and isolating high-risk networks
                        within the Ayushman Bharat ecosystem.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-offwhite border border-slate-200 rounded-lg p-6 flex flex-col">
                        <div className="flex items-center gap-3 mb-4 text-slate-500 font-medium text-sm uppercase tracking-wider">
                            <ShieldCheck className="w-5 h-5 text-hcblue-800" />
                            Total Claims Analyzed
                        </div>
                        <div className="text-3xl font-bold text-hcblue-900 mt-auto">145,289</div>
                    </div>

                    <div className="bg-offwhite border border-slate-200 rounded-lg p-6 flex flex-col">
                        <div className="flex items-center gap-3 mb-4 text-slate-500 font-medium text-sm uppercase tracking-wider">
                            <AlertTriangle className="w-5 h-5 text-danger-700" />
                            Suspicious Claims
                        </div>
                        <div className="text-3xl font-bold text-danger-700 mt-auto">12.1%</div>
                    </div>

                    <div className="bg-offwhite border border-slate-200 rounded-lg p-6 flex flex-col">
                        <div className="flex items-center gap-3 mb-4 text-slate-500 font-medium text-sm uppercase tracking-wider">
                            <Users className="w-5 h-5 text-teals-600" />
                            High-Risk Providers
                        </div>
                        <div className="text-3xl font-bold text-teals-600 mt-auto">341</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HeroSection;
