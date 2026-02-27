import React, { useState } from 'react';
import { ShieldAlert, ArrowUpDown, ExternalLink } from 'lucide-react';

const defaultProviderData = [
    { id: 'HOSP-29004', name: 'Metro Health Cardiology', location: 'Delhi', cases: 1420, avgClaim: '₹84,500', baseRisk: 88, dupRisk: 94 },
    { id: 'HOSP-11092', name: 'Sunrise Orthopedics', location: 'Mumbai', cases: 890, avgClaim: '₹112,000', baseRisk: 84, dupRisk: 85 },
    { id: 'HOSP-55018', name: 'LifeCare General', location: 'Bangalore', cases: 3100, avgClaim: '₹24,000', baseRisk: 81, dupRisk: 70 },
    { id: 'HOSP-88211', name: 'Apex Oncology Center', location: 'Chennai', cases: 420, avgClaim: '₹210,000', baseRisk: 78, dupRisk: 65 },
    { id: 'HOSP-33904', name: 'City Hospital Group', location: 'Pune', cases: 5600, avgClaim: '₹18,500', baseRisk: 22, dupRisk: 10 },
];

const calculateUnifiedScore = (baseScore: number, dupScore: number) => {
    return Math.round((0.7 * baseScore) + (0.3 * dupScore));
};

const ProviderRanking = ({ data }: { data?: any }) => {
    const [sortField, setSortField] = useState('unifiedRisk');

    const providerData = data || defaultProviderData;

    const processedData = providerData.map((p: any) => ({
        ...p,
        unifiedRisk: calculateUnifiedScore(p.baseRisk, p.dupRisk)
    })).sort((a: any, b: any) => b.unifiedRisk - a.unifiedRisk);

    return (
        <div className="w-full">
            <div className="flex justify-between items-center mb-6 border-b border-slate-200 pb-2">
                <h2 className="text-2xl font-bold text-hcblue-900">
                    High-Risk Provider Index (Unified)
                </h2>
                <div className="text-sm text-slate-500">
                    Formula: (0.7 × Isolation Forest) + (0.3 × Image Duplication)
                </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="border-b border-slate-200 bg-slate-50">
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Provider ID</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Location</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Volume</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Avg Claim</th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right cursor-pointer hover:bg-slate-100 transition-colors group">
                                    <div className="flex items-center justify-end gap-1">
                                        Isolation Forest <ArrowUpDown className="w-3 h-3 text-slate-400 group-hover:text-hcblue-800" />
                                    </div>
                                </th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right cursor-pointer hover:bg-slate-100 transition-colors group">
                                    <div className="flex items-center justify-end gap-1">
                                        Unified Index <ArrowUpDown className="w-3 h-3 text-slate-400 group-hover:text-hcblue-800" />
                                    </div>
                                </th>
                                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-center">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {processedData.map((provider: any) => (
                                <tr key={provider.id} className="hover:bg-slate-50 transition-colors">
                                    <td className="px-6 py-4">
                                        <span className="font-mono text-sm font-semibold text-hcblue-900 bg-slate-100 px-2 py-1 rounded inline-block">
                                            {provider.id}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-slate-500 text-sm">
                                        {provider.location}
                                    </td>
                                    <td className="px-6 py-4 text-right font-medium text-slate-700 text-sm">
                                        {provider.cases.toLocaleString()}
                                    </td>
                                    <td className="px-6 py-4 text-right text-slate-500 text-sm">
                                        {provider.avgClaim}
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <span className="text-slate-600 font-mono text-sm">{provider.baseRisk}%</span>
                                    </td>
                                    <td className="px-6 py-4 text-right">
                                        <div className="flex items-center justify-end gap-2">
                                            {provider.unifiedRisk >= 80 && (
                                                <ShieldAlert className="w-4 h-4 text-danger-700" />
                                            )}
                                            <span className={`font-bold font-mono text-base ${provider.unifiedRisk >= 80 ? 'text-danger-700' : provider.unifiedRisk >= 60 ? 'text-amber-600' : 'text-teals-600'}`}>
                                                {provider.unifiedRisk}%
                                            </span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-center">
                                        <button className="text-hcblue-800 hover:text-hcblue-900 bg-hcblue-50 hover:bg-hcblue-100 px-3 py-1.5 rounded text-sm font-medium transition-colors inline-flex items-center gap-1 border border-hcblue-200">
                                            Audit <ExternalLink className="w-3 h-3" />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default ProviderRanking;
