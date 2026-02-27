import React from 'react';
import { ShieldAlert } from 'lucide-react';

interface TopNavProps {
    activeSection: string;
}

const navItems = [
    { id: 'overview', label: 'Overview' },
    { id: 'analytics', label: 'Claim Analysis' },
    { id: 'providers', label: 'Provider Risk' },
    { id: 'upload', label: 'Fraudulent Claim Recognization' }
];

const TopNav: React.FC<TopNavProps> = ({ activeSection }) => {
    const scrollTo = (id: string) => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">
            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-hcblue-800 rounded flex items-center justify-center">
                        <ShieldAlert className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h1 className="font-bold text-lg text-hcblue-900 leading-tight">Arogya Vigilant</h1>
                        <p className="text-[10px] text-slate-500 font-medium uppercase tracking-widest">Government of India</p>
                    </div>
                </div>

                <nav className="hidden md:flex items-center gap-8 h-full">
                    {navItems.map((item) => {
                        const isActive = activeSection === item.id;
                        return (
                            <button
                                key={item.id}
                                onClick={() => scrollTo(item.id)}
                                className={`h-full relative px-1 text-sm font-medium transition-colors ${isActive ? 'text-hcblue-800' : 'text-slate-600 hover:text-hcblue-800'
                                    }`}
                            >
                                {item.label}
                                {isActive && (
                                    <div className="absolute bottom-0 left-0 w-full h-0.5 bg-hcblue-800 rounded-t-sm" />
                                )}
                            </button>
                        );
                    })}
                </nav>

                <div className="flex items-center gap-4">
                    <span className="text-xs font-semibold text-teals-500 bg-teals-500/10 px-3 py-1.5 rounded-full border border-teals-500/20">
                        Secure Session Active
                    </span>
                </div>
            </div>
        </header>
    );
};

export default TopNav;
