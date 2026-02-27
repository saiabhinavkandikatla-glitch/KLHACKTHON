import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend } from 'recharts';

const timelineData = [
    { month: 'Jan', processed: 4000, flagged: 240, saved: 2400 },
    { month: 'Feb', processed: 3000, flagged: 139, saved: 2210 },
    { month: 'Mar', processed: 2000, flagged: 980, saved: 2290 },
    { month: 'Apr', processed: 2780, flagged: 390, saved: 2000 },
    { month: 'May', processed: 1890, flagged: 480, saved: 2181 },
    { month: 'Jun', processed: 2390, flagged: 380, saved: 2500 },
    { month: 'Jul', processed: 3490, flagged: 430, saved: 2100 },
];

const regionData = [
    { region: 'North', legitimate: 4000, fraudulent: 400 },
    { region: 'South', legitimate: 3000, fraudulent: 139 },
    { region: 'East', legitimate: 2000, fraudulent: 980 },
    { region: 'West', legitimate: 2780, fraudulent: 390 },
    { region: 'Central', legitimate: 1890, fraudulent: 480 },
];

const Analytics = () => {
    return (
        <div className="w-full">
            <h2 className="text-2xl font-bold text-hcblue-900 mb-6 border-b border-slate-200 pb-2">
                Claim Analytics & Models
            </h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="font-semibold text-hcblue-900">Claim Processing Volume Trend</h3>
                    </div>
                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={timelineData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorProcessed" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#0F2C59" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#0F2C59" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorFlagged" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#B91C1C" stopOpacity={0.1} />
                                        <stop offset="95%" stopColor="#B91C1C" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="month" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `${val / 1000}k`} />
                                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '6px', color: '#1e293b' }}
                                    itemStyle={{ fontSize: '12px', fontWeight: 500 }}
                                />
                                <Area type="monotone" dataKey="processed" name="Total Claims" stroke="#0F2C59" strokeWidth={2} fillOpacity={1} fill="url(#colorProcessed)" />
                                <Area type="monotone" dataKey="flagged" name="High Risk Claims" stroke="#B91C1C" strokeWidth={2} fillOpacity={1} fill="url(#colorFlagged)" />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="font-semibold text-hcblue-900">Regional Risk Distribution (Sample)</h3>
                    </div>
                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={regionData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
                                <XAxis dataKey="region" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '6px', color: '#1e293b' }}
                                    cursor={{ fill: '#f1f5f9' }}
                                />
                                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                                <Bar dataKey="legitimate" name="Valid Claims" stackId="a" fill="#008080" />
                                <Bar dataKey="fraudulent" name="Fraudulent Claims" stackId="a" fill="#B91C1C" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Analytics;
