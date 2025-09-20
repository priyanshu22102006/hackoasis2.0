import { useState } from "react";
import { motion } from "framer-motion";

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [reason, setReason] = useState("");
  const [counters, setCounters] = useState({
    total: 0,
    verified: 0,
    suspicious: 0,
    timeSaved: 0,
  });

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file!");

    // Dummy API simulation
    const dummyResponse = Math.random() > 0.5
      ? { status: "Verified", reason: "Signature detected" }
      : { status: "Suspicious", reason: "Signature missing" };

    setStatus(dummyResponse.status);
    setReason(dummyResponse.reason);

    setCounters(prev => ({
      total: prev.total + 1,
      verified: prev.verified + (dummyResponse.status === "Verified" ? 1 : 0),
      suspicious: prev.suspicious + (dummyResponse.status === "Suspicious" ? 1 : 0),
      timeSaved: prev.timeSaved + 5, // 5 min saved per doc
    }));
  };

  return (
    <div className="min-h-screen bg-black text-white p-6">
      {/* Header */}
      <header className="text-center mb-8">
        <h1 className="text-4xl font-extrabold text-neon-blue drop-shadow-[0_0_10px_#00FFFF]">
          AI Document Verifier
        </h1>
        <p className="text-gray-400 mt-2">Black + Neon Dashboard</p>
      </header>

      {/* Upload Box */}
      <div className="max-w-xl mx-auto">
        <div className="border-2 border-dashed border-neon-green p-10 rounded-2xl text-center cursor-pointer hover:shadow-[0_0_20px_#00ffea] transition">
          <input type="file" onChange={handleFileChange} className="mb-4"/>
          <p className="text-xl font-bold text-neon-green">Drag & Drop Certificate</p>
          <p className="text-sm text-gray-400">or click to upload</p>
        </div>
        <button
          onClick={handleUpload}
          className="mt-4 w-full bg-neon-blue text-black font-bold py-2 rounded-xl hover:shadow-[0_0_20px_#00FFFF] transition"
        >
          Verify Document
        </button>

        {/* Result Card */}
        {status && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className={`p-6 rounded-xl text-black font-bold text-center mt-6 shadow-[0_0_15px_#00ffea] ${
              status === "Verified" ? "bg-neon-green" :
              status === "Suspicious" ? "bg-neon-pink" : "bg-yellow-400"
            }`}
          >
            <h2>Status: {status}</h2>
            <p className="mt-2 font-normal">{reason}</p>
          </motion.div>
        )}
      </div>

      {/* Dashboard */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-10 max-w-4xl mx-auto">
        <div className="p-4 rounded-xl text-center bg-black border border-neon-green shadow-[0_0_10px_#39FF14]">
          <h3 className="text-2xl font-bold text-neon-green">{counters.total}</h3>
          <p className="text-gray-400">Total Docs</p>
        </div>
        <div className="p-4 rounded-xl text-center bg-black border border-neon-blue shadow-[0_0_10px_#00FFFF]">
          <h3 className="text-2xl font-bold text-neon-blue">{counters.verified}</h3>
          <p className="text-gray-400">Verified</p>
        </div>
        <div className="p-4 rounded-xl text-center bg-black border border-neon-pink shadow-[0_0_10px_#FF10F0]">
          <h3 className="text-2xl font-bold text-neon-pink">{counters.suspicious}</h3>
          <p className="text-gray-400">Suspicious</p>
        </div>
        <div className="p-4 rounded-xl text-center bg-black border border-yellow-400 shadow-[0_0_10px_#FFD700]">
          <h3 className="text-2xl font-bold text-yellow-400">{counters.timeSaved} min</h3>
          <p className="text-gray-400">Time Saved</p>
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-10 text-center text-gray-500 border-t border-neon-blue pt-4">
        Built for HOSA02 Challenge — 2025
      </footer>
    </div>
  );
}

export default App;