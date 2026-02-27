import React, { useState, useRef, useEffect } from 'react';
import { UploadCloud, FileText, CheckCircle, AlertTriangle, XCircle, Search, Shield, Cpu, Image as ImageIcon } from 'lucide-react';

type ProcessState = 'idle' | 'extracting' | 'classifying' | 'rejected' | 'preprocessing' | 'embedding' | 'scoring' | 'complete';

const DocumentInvestigation = () => {
    const [file, setFile] = useState<File | null>(null);
    const [processState, setProcessState] = useState<ProcessState>('idle');
    const [progress, setProgress] = useState(0);
    const [errorMessage, setErrorMessage] = useState('');
    const [results, setResults] = useState<any>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleDragOver = (e: React.DragEvent) => e.preventDefault();

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    };

    const handleFileSelection = (selectedFile: File) => {
        if (selectedFile.type !== 'application/pdf') {
            setFile(selectedFile);
            setProcessState('rejected');
            setErrorMessage("Strict Policy Violation: Only standard PDF documents containing medical scans are accepted.");
            return;
        }

        setFile(selectedFile);
        startPipeline();
    };

    const startPipeline = () => {
        setProcessState('extracting');
        setProgress(10);
        setResults(null);
        setErrorMessage('');

        // Simulate strict validation pipeline
        setTimeout(() => {
            setProcessState('classifying');
            setProgress(35);

            setTimeout(() => {
                // Randomly simulate a failed X-ray classification (20% chance to fail)
                const isXray = Math.random() > 0.2;
                const confidence = isXray ? 85 + Math.random() * 14 : 20 + Math.random() * 50;

                if (confidence < 80) {
                    setProcessState('rejected');
                    setErrorMessage(`Validation Failed (Confidence ${confidence.toFixed(1)}%). Invalid file type detected. Expected: Diagnostic X-Ray Image.`);
                    setProgress(100);
                    return;
                }

                setProcessState('preprocessing');
                setProgress(55);

                setTimeout(() => {
                    setProcessState('embedding');
                    setProgress(75);

                    setTimeout(() => {
                        setProcessState('scoring');
                        setProgress(90);

                        setTimeout(() => {
                            // Generate strict scores
                            const ifScore = Math.floor(Math.random() * 60) + 20; // 0-100 mapped Isolation Forest
                            const dupScore = Math.floor(Math.random() * 40); // 0-100 Duplication baseline
                            const finalRisk = Math.round((0.7 * ifScore) + (0.3 * dupScore));

                            setResults({
                                confidence: confidence.toFixed(1),
                                ifScore,
                                dupScore,
                                finalRisk,
                                pHash: `a${Math.floor(Math.random() * 1000000)}b${Math.floor(Math.random() * 10000)}c`,
                                vectorId: `EMB-2024-${Math.floor(Math.random() * 9000) + 1000}`
                            });
                            setProcessState('complete');
                            setProgress(100);
                        }, 800);
                    }, 800);
                }, 800);
            }, 1200);
        }, 1000);
    };

    const resetUpload = () => {
        setFile(null);
        setProcessState('idle');
        setResults(null);
        setProgress(0);
        setErrorMessage('');
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    return (
        <div className="w-full">
            <h2 className="text-2xl font-bold text-hcblue-900 mb-6 border-b border-slate-200 pb-2">
                Fraudulent Claim Recognization
            </h2>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* Upload Column */}
                <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm min-h-[450px] flex flex-col">
                    <div className="flex items-center gap-2 mb-6 text-sm font-semibold text-hcblue-900 uppercase tracking-wide">
                        <UploadCloud className="w-4 h-4 text-hcblue-800" />
                        1. Document Ingestion
                    </div>

                    {processState === 'idle' ? (
                        <div
                            onDragOver={handleDragOver}
                            onDrop={handleDrop}
                            onClick={() => fileInputRef.current?.click()}
                            className="flex-1 border-2 border-dashed border-slate-300 hover:border-hcblue-500 hover:bg-slate-50 transition-colors rounded-lg flex flex-col items-center justify-center cursor-pointer p-8 group"
                        >
                            <div className="bg-slate-100 p-4 rounded-full mb-4">
                                <FileText className="w-8 h-8 text-hcblue-700" />
                            </div>
                            <p className="text-base font-semibold text-slate-700 mb-2">Select Diagnostic PDF</p>
                            <p className="text-sm text-slate-500 mb-6 text-center max-w-[250px]">
                                Strictly accepts `.pdf` files containing medical imaging. Documents are parsed for X-ray arrays.
                            </p>
                            <button className="bg-hcblue-800 hover:bg-hcblue-900 text-white px-5 py-2 rounded text-sm font-medium transition-colors border border-hcblue-900">
                                Browse Directory
                            </button>
                            <input type="file" ref={fileInputRef} onChange={handleFileChange} accept=".pdf" className="hidden" />
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col">
                            <div className="bg-slate-50 border border-slate-200 p-4 rounded-lg relative mb-6">
                                <button
                                    onClick={resetUpload}
                                    className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 transition-colors"
                                >
                                    <XCircle className="w-5 h-5" />
                                </button>
                                <div className="flex items-center gap-3">
                                    <FileText className="w-6 h-6 text-hcblue-700" />
                                    <div>
                                        <p className="text-slate-800 font-medium text-sm truncate max-w-[200px]">{file?.name}</p>
                                        <p className="text-xs text-slate-500">{(file?.size! / 1024 / 1024).toFixed(2)} MB</p>
                                    </div>
                                </div>
                            </div>

                            {/* Status Pipeline Log */}
                            <div className="flex-1 border border-slate-200 rounded-lg p-5 bg-white">
                                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">System Processing Log</h4>
                                <div className="space-y-4 relative">
                                    <div className="absolute left-2.5 top-0 bottom-0 w-px bg-slate-100" />

                                    <StepLog active={processState !== 'idle'} done={['classifying', 'preprocessing', 'embedding', 'scoring', 'complete', 'rejected'].includes(processState)} icon={Search} text="Extraction Engine: Isolating Page 1 Object" />
                                    <StepLog active={['classifying', 'preprocessing', 'embedding', 'scoring', 'complete'].includes(processState)} done={['preprocessing', 'embedding', 'scoring', 'complete'].includes(processState)} error={processState === 'rejected'} icon={Shield} text={processState === 'rejected' ? 'Image Classifier: Strict Rejection (< 80% Valid)' : `Image Classifier: X-Ray Verified (> 80%)`} />

                                    {processState !== 'rejected' && (
                                        <>
                                            <StepLog active={['preprocessing', 'embedding', 'scoring', 'complete'].includes(processState)} done={['embedding', 'scoring', 'complete'].includes(processState)} icon={ImageIcon} text="Computer Vision: Grayscale -> Resize -> Normalize" />
                                            <StepLog active={['embedding', 'scoring', 'complete'].includes(processState)} done={['scoring', 'complete'].includes(processState)} icon={Cpu} text="ResNet Encoding: Generating Feature Vectors" />
                                        </>
                                    )}
                                </div>

                                {processState !== 'complete' && processState !== 'rejected' && (
                                    <div className="mt-6">
                                        <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                            <div className="h-full bg-hcblue-800 transition-all duration-300" style={{ width: `${progress}%` }} />
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                {/* Results Column */}
                <div className="bg-white border border-slate-200 rounded-lg p-6 shadow-sm min-h-[450px] flex flex-col relative overflow-hidden">
                    <div className="flex items-center gap-2 mb-6 text-sm font-semibold text-hcblue-900 uppercase tracking-wide">
                        <Shield className="w-4 h-4 text-hcblue-800" />
                        2. Strict Risk Evaluation
                    </div>

                    {!file || progress < 90 ? (
                        <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
                            <Shield className="w-12 h-12 mb-4 opacity-20" />
                            <p className="text-sm font-medium">Awaiting valid extraction pipeline completion.</p>
                        </div>
                    ) : processState === 'rejected' ? (
                        <div className="flex-1 flex flex-col items-center justify-center text-center">
                            <div className="bg-danger-700/10 p-4 rounded-full mb-4">
                                <AlertTriangle className="w-10 h-10 text-danger-700" />
                            </div>
                            <h3 className="text-lg font-bold text-slate-800 mb-2">Process Terminated</h3>
                            <p className="text-sm text-danger-700 font-medium mb-2">{errorMessage}</p>
                            <p className="text-xs text-slate-500 max-w-[250px]">Standard Operating Procedure blocks any non-diagnostic inputs from entering the risk scoring model.</p>
                        </div>
                    ) : results && (
                        <div className="flex-1 flex flex-col">
                            <div className="grid grid-cols-2 gap-4 mb-6">
                                <div className="bg-slate-50 p-3 rounded-md border border-slate-200">
                                    <span className="text-xs text-slate-500 block mb-1 font-medium">Perceptual Hash Matrix</span>
                                    <span className="text-xs font-mono text-slate-700 break-all">{results.pHash}</span>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-md border border-slate-200">
                                    <span className="text-xs text-slate-500 block mb-1 font-medium">ResNet Checksum</span>
                                    <span className="text-xs font-mono text-slate-700">{results.vectorId}</span>
                                </div>
                            </div>

                            <div className="space-y-4 flex-1">
                                <div className="flex justify-between flex-col pb-3 border-b border-slate-100">
                                    <div className="flex justify-between mb-1">
                                        <span className="text-sm font-semibold text-slate-700 flex items-center gap-1">Isolation Forest Return Score</span>
                                        <span className="text-sm font-bold text-slate-800">{results.ifScore}/100</span>
                                    </div>
                                    <span className="text-xs text-slate-500">Normalized model output based on 0.03 contamination fit.</span>
                                </div>

                                <div className="flex justify-between flex-col pb-3 border-b border-slate-100">
                                    <div className="flex justify-between mb-1">
                                        <span className="text-sm font-semibold text-slate-700 flex items-center gap-1">Image Duplication Trace</span>
                                        <span className="text-sm font-bold text-slate-800">{results.dupScore}/100</span>
                                    </div>
                                    <span className="text-xs text-slate-500">Vector distance index comparison against historical cache.</span>
                                </div>
                            </div>

                            {/* Final Score Block */}
                            <div className={`mt-6 p-5 rounded-lg border flex items-center justify-between ${results.finalRisk > 60 ? 'bg-danger-700/5 border-danger-700/20' : 'bg-teals-50 border-teals-100'}`}>
                                <div>
                                    <span className="text-xs font-bold uppercase tracking-wider block mb-1 text-slate-500">Calculated Final Risk</span>
                                    <span className="text-[10px] text-slate-400 font-mono">(0.7 * IF) + (0.3 * Dup)</span>
                                </div>
                                <div className={`text-4xl font-extrabold ${results.finalRisk > 60 ? 'text-danger-700' : 'text-teals-600'}`}>
                                    {results.finalRisk}%
                                </div>
                            </div>
                        </div>
                    )}
                </div>

            </div>
        </div>
    );
};

// Helper component for the visual logs
const StepLog = ({ active, done, error, icon: Icon, text }: any) => {
    return (
        <div className={`flex gap-3 text-sm relative z-10 ${!active ? 'opacity-30' : 'opacity-100'}`}>
            <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 border mt-0.5 bg-white
        ${error ? 'border-danger-700 text-danger-700' :
                    done ? 'border-teals-600 text-teals-600 bg-teals-50' :
                        active ? 'border-hcblue-800 text-hcblue-800' : 'border-slate-300'}
      `}>
                {error ? <XCircle className="w-3 h-3" /> : done ? <CheckCircle className="w-3 h-3" /> : <Icon className="w-3 h-3" />}
            </div>
            <div className={`pt-0.5 ${error ? 'text-danger-700 font-medium' : done ? 'text-slate-800' : active ? 'text-hcblue-900 font-medium' : 'text-slate-400'}`}>
                {text}
            </div>
        </div>
    );
};

export default DocumentInvestigation;
