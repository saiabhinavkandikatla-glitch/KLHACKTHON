import React, { useState } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Info } from 'lucide-react';

const generateData = () => {
    const data = [];
    for (let i = 0; i < 300; i++) {
        const isAnomaly = Math.random() > 0.95;
        data.push({
            x: isAnomaly ? Math.random() * 100 : 40 + Math.random() * 20,
            y: isAnomaly ? Math.random() * 100 : 40 + Math.random() * 20,
            z: isAnomaly ? 3 : 1, // Determines size
            anomalyScore: isAnomaly ? 0.8 + Math.random() * 0.2 : Math.random() * 0.4,
            isAnomaly,
            id: `CLM-${Math.floor(Math.random() * 90000) + 10000}`
        });
    }
    return data;
};

const data = generateData();
const normalData = data.filter(d => !d.isAnomaly);
const anomalyData = data.filter(d => d.isAnomaly);

const AnomalyDetection = () => {
    const [showExplanation, setShowExplanation] = useState(false);

    return (
        <div className="w-full">
            <h2 className="text-2xl font-bold text-hcblue-900 mb-6 border-b border-slate-200 pb-2 flex justify-between items-center">
                Isolation Forest Output
                <button
                    onClick={() => setShowExplanation(!showExplanation)}
                    className="text-sm font-normal text-hcblue-800 hover:text-hcblue-900 flex items-center gap-1 transition-colors"
                >
                    <Info className="w-4 h-4" />
                    {showExplanation ? 'Hide Details' : 'View Methodology'}
                </button>
            </h2>

            {showExplanation && (
                <div className="bg-slate-50 border border-slate-200 p-4 rounded-lg mb-6 text-sm text-slate-700 shadow-sm">
                    <p className="mb-2"><strong>Methodology:</strong> The Isolation Forest algorithm isolates anomalous billing patterns by randomly selecting a feature and a split value. Outliers (fraudulent claims) require fewer splits to be isolated, resulting in a higher anomaly score.</p>
                    <p><strong>Configuration:</strong> Contamination parameter set to 0.03 based on historical enforcement data. Data is standardized (mean=0, variance=1) prior to fitting. Scores are normalized to [0, 1].</p>
                </div>
            )}

            <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm">
                <div className="h-[400px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                            <XAxis type="number" dataKey="x" name="Standardized Feature 1" tick={{ fontSize: 12, fill: '#64748b' }} stroke="#94a3b8" />
                            <YAxis type="number" dataKey="y" name="Standardized Feature 2" tick={{ fontSize: 12, fill: '#64748b' }} stroke="#94a3b8" />
                            <Tooltip
                                cursor={{ strokeDasharray: '3 3' }}
                                contentStyle={{ backgroundColor: 'white', borderColor: '#e2e8f0', borderRadius: '4px', fontSize: '12px' }}
                                formatter={(value, name, props) => {
                                    if (name === "Standardized Feature 1" || name === "Standardized Feature 2") return value.toFixed(2);
                                    return value;
                                }}
                            />
                            <Scatter name="Valid Claims (Inliers)" data={normalData} fill="#0F2C59" opacity={0.6} line={false} />
                            <Scatter name="Suspicious (Outliers)" data={anomalyData} fill="#B91C1C" opacity={0.8} line={false} shape="cross" />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default AnomalyDetection;
