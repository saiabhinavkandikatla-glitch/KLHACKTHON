import React from 'react';
import { Activity, ShieldCheck, AlertCircle, Clock } from 'lucide-react';

const defaultLogEntries = [
    { id: 1, time: '10:42 AM', type: 'info', message: 'Batch PDF OCR ingestion completed (420 records).' },
    { id: 2, time: '10:38 AM', type: 'warning', message: 'Duplicate signature detected from Provider #0442.' },
    { id: 3, time: '10:15 AM', type: 'alert', message: 'Isolation Forest flagged 14 claims > 0.82 Anomaly Score.' },
    { id: 4, time: '09:00 AM', type: 'info', message: 'System initialization and embedding model loaded.' },
];

const Overview = ({ data }: { data?: any }) => {
    const claimsProcessed = data?.claimsProcessed?.toLocaleString() || "145,289";
    const totalValue = data?.totalValue || "₹84.2 Cr";
    const activeAlerts = data?.activeAlerts?.toLocaleString() || "4,192";
    const preventedSavings = data?.preventedSavings || "₹12.4 Cr";
    const logEntries = data?.logs || defaultLogEntries;

    return (
        <div className="w-full">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-hcblue-900 flex items-center gap-2">
                    System Overview
                </h2>
                <span className="text-sm font-medium text-slate-500 bg-slate-100 px-3 py-1 rounded-full">
                    Last refreshed: Just now
                </span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 grid grid-cols-2 gap-4">
                    <div className="bg-white border border-slate-200 p-5 rounded-lg shadow-sm">
                        <div className="text-sm text-slate-500 font-medium tracking-wide mb-1">Total Claim Value Adjudicated</div>
                        <div className="text-2xl font-bold text-hcblue-800">{totalValue}</div>
                        <div className="text-xs text-slate-400 mt-2">FY 2024-25 Q1</div>
                    </div>

                    <div className="bg-white border border-slate-200 p-5 rounded-lg shadow-sm">
                        <div className="text-sm text-slate-500 font-medium tracking-wide mb-1">Claims Processed</div>
                        <div className="text-2xl font-bold text-hcblue-800">{claimsProcessed}</div>
                        <div className="text-xs text-teals-600 mt-2 font-medium">↑ +12.4% vs last month</div>
                    </div>

                    <div className="bg-white border border-slate-200 p-5 rounded-lg shadow-sm">
                        <div className="text-sm text-slate-500 font-medium tracking-wide mb-1">Active High-Risk Alerts</div>
                        <div className="text-2xl font-bold text-danger-700">{activeAlerts}</div>
                        <div className="text-xs text-danger-700 mt-2 font-medium">Requires investigation</div>
                    </div>

                    <div className="bg-white border border-slate-200 p-5 rounded-lg shadow-sm">
                        <div className="text-sm text-slate-500 font-medium tracking-wide mb-1">Estimated Savings (Prevented)</div>
                        <div className="text-2xl font-bold text-teals-600">{preventedSavings}</div>
                        <div className="text-xs text-slate-400 mt-2">Based on blocked transactions</div>
                    </div>
                </div>

                {/* System Activity Log */}
                <div className="bg-white border border-slate-200 rounded-lg shadow-sm flex flex-col h-full">
                    <div className="border-b border-slate-100 p-4 font-semibold text-hcblue-900 flex items-center gap-2">
                        <Activity className="w-4 h-4 text-slate-400" />
                        Live Security Log
                    </div>
                    <div className="p-4 flex-1 overflow-y-auto">
                        <div className="space-y-4">
                            {logEntries.map((log: any) => (
                                <div key={log.id} className="flex gap-3 text-sm border-l-2 pl-3 pb-2 border-slate-100 last:pb-0 relative">
                                    <div className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 flex items-center justify-center
                                        ${log.type === 'alert' ? 'border-danger-700 text-danger-700' :
                                            log.type === 'warning' ? 'border-amber-500 text-amber-500' :
                                                'border-teals-500 text-teals-500'}`}
                                    >
                                        <div className={`w-1.5 h-1.5 rounded-full 
                                            ${log.type === 'alert' ? 'bg-danger-700' :
                                                log.type === 'warning' ? 'bg-amber-500' :
                                                    'bg-teals-500'}`} />
                                    </div>
                                    <div className="flex-1">
                                        <div className="text-slate-400 text-xs mb-0.5 font-medium">{log.time}</div>
                                        <div className="text-slate-700">{log.message}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Overview;
