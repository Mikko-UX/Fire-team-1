import { useRef, useState } from "react";
import { VehicleCombat } from "./components/VehicleCombat";
import { InfantryCombat } from "./components/InfantryCombat";

export default function App() {
  const contentRef = useRef<HTMLDivElement>(null);
  const [activeTab, setActiveTab] = useState<"vehicle" | "infantry">("vehicle");
  const [isDragging, setIsDragging] = useState(false);
  const [startDragY, setStartDragY] = useState(0);
  const [startScrollTop, setStartScrollTop] = useState(0);

  const handleDragStart = (clientY: number) => {
    const el = contentRef.current;
    if (!el) return;
    setIsDragging(true);
    setStartDragY(clientY);
    setStartScrollTop(el.scrollTop);
  };

  const handleDragMove = (clientY: number) => {
    const el = contentRef.current;
    if (!isDragging || !el) return;
    const delta = clientY - startDragY;
    el.scrollTop = startScrollTop - delta;
  };

  const handleDragEnd = () => {
    setIsDragging(false);
  };

  return (
    <div className="min-h-screen bg-[#2c3e50] flex flex-col max-w-md mx-auto">
      {/* App Title */}
      <div className="bg-[#1a252f] py-3 text-center border-b-2 border-[#34495e]">
        <h1 className="text-white font-bold text-lg tracking-wider">FIRE TEAM CALCULATOR</h1>
        <p className="text-gray-400 text-xs">Board Game Companion v6.5</p>
      </div>
      
      {/* Header Tabs */}
      <div role="tablist" aria-label="Combat mode tabs" className="bg-[#34495e] p-2 flex gap-2 sticky top-0 z-10 shadow-lg">
        <button
          role="tab"
          aria-selected={activeTab === "vehicle"}
          onClick={() => setActiveTab("vehicle")}
          className={`flex-1 py-4 rounded-md font-bold text-sm transition-all ${
            activeTab === "vehicle"
              ? "bg-[#3498db] text-black shadow-lg"
              : "bg-[#95a5a6] text-white"
          }`}
        >
          VEHICLE COMBAT
        </button>
        <button
          role="tab"
          aria-selected={activeTab === "infantry"}
          onClick={() => setActiveTab("infantry")}
          className={`flex-1 py-4 rounded-md font-bold text-sm transition-all ${
            activeTab === "infantry"
              ? "bg-[#2ecc71] text-black shadow-lg"
              : "bg-[#95a5a6] text-white"
          }`}
        >
          INFANTRY COMBAT
        </button>
      </div>

      {/* Content */}
      <div
        ref={contentRef}
        role="region"
        aria-live="polite"
        className={`flex-1 overflow-auto touch-pan-y ${isDragging ? "cursor-grabbing" : "cursor-auto"}`}
        onMouseDown={(e) => handleDragStart(e.clientY)}
        onMouseMove={(e) => handleDragMove(e.clientY)}
        onMouseUp={handleDragEnd}
        onMouseLeave={handleDragEnd}
        onTouchStart={(e) => handleDragStart(e.touches[0].clientY)}
        onTouchMove={(e) => handleDragMove(e.touches[0].clientY)}
        onTouchEnd={handleDragEnd}
      >
        {activeTab === "vehicle" ? <VehicleCombat /> : <InfantryCombat />}
      </div>
    </div>
  );
}