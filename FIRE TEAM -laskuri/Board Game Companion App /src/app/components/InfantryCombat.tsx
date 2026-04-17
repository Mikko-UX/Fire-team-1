import { useState } from "react";
import { infantryFireTableLookup } from "../data/infantry-table";

export function InfantryCombat() {
  const [firepower, setFirepower] = useState("");
  const [leadership, setLeadership] = useState(0);
  const [fear, setFear] = useState(0);

  // Terrain modifiers
  const [targetInDefilade, setTargetInDefilade] = useState(false);
  const [targetCautious, setTargetCautious] = useState(false);
  const [targetInWoodBuildings, setTargetInWoodBuildings] = useState(false);
  const [targetInStoneBuildings, setTargetInStoneBuildings] = useState(false);
  const [targetInWoodsDirectFire, setTargetInWoodsDirectFire] = useState(false);
  const [targetInWoodsIndirectFire, setTargetInWoodsIndirectFire] =
    useState(false);
  const [targetInCover, setTargetInCover] = useState(false);
  const [targetIsVehicle, setTargetIsVehicle] = useState(false);
  const [targetEntrenchedDirectFire, setTargetEntrenchedDirectFire] =
    useState(false);
  const [targetEntrenchedIndirectFire, setTargetEntrenchedIndirectFire] =
    useState(false);

  const [result, setResult] = useState<any>(null);

  const calculateModifiers = () => {
    let total = 0;
    if (targetInDefilade) total += 2;
    if (targetCautious) total += 3;
    if (targetInWoodBuildings) total += 3;
    if (targetInStoneBuildings) total += 4;
    if (targetInWoodsDirectFire) total += 2;
    if (targetInWoodsIndirectFire) total += 1;
    if (targetInCover) total += 1;
    if (targetIsVehicle) total -= 2;
    if (targetEntrenchedDirectFire) total += 2;
    if (targetEntrenchedIndirectFire) total += 3;
    return total;
  };

  const handleRollDice = () => {
    if (!firepower) {
      alert("Please enter firepower");
      return;
    }

    const dieRoll = Math.floor(Math.random() * 10) + 1; // D10: 1-10
    const modifiers = calculateModifiers() - leadership + fear;

    const lookupResult = infantryFireTableLookup(
      parseInt(firepower),
      dieRoll,
      modifiers
    );

    setResult({
      ...lookupResult,
      actualDieRoll: dieRoll,
      totalModifiers: modifiers,
    });
  };

  const getResultEmoji = (resultCode: string) => {
    switch (resultCode) {
      case "E":
        return "🔥";
      case "F":
        return "⚠️";
      case "2":
        return "⚠️⚠️";
      case "1":
        return "⚠️";
      case "0":
        return "✅";
      default:
        return "";
    }
  };

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Firepower Input */}
      <div className="bg-[#C8E6C9] rounded-lg p-4 shadow-lg">
        <h3 className="text-center font-bold mb-4 text-black">
          FIREPOWER
        </h3>
        <p className="text-center text-sm mb-2 text-black">
          Enter Firepower (determines column B-T)
        </p>
        <input
          type="number"
          value={firepower}
          onChange={(e) => setFirepower(e.target.value)}
          className="w-full p-3 rounded border-2 text-black text-center text-xl font-bold"
          placeholder="Enter firepower..."
        />
      </div>

      {/* Die Roll + Modifiers */}
      <div className="bg-[#A5D6A7] rounded-lg p-4 shadow-lg">
        <h3 className="text-center font-bold mb-4 text-black">
          DIE ROLL + MODIFIERS
        </h3>
        <p className="text-center text-sm mb-4 text-black italic">
          Modified die roll determines row (1-14)
        </p>

        {/* Leadership */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">
            Leadership (subtract)
          </p>
          <div className="flex justify-center gap-4">
            {[0, -1, -2, -3].map((val) => (
              <label
                key={val}
                className="flex items-center gap-1 cursor-pointer"
              >
                <input
                  type="radio"
                  name="leadership"
                  checked={leadership === Math.abs(val)}
                  onChange={() => setLeadership(Math.abs(val))}
                  className="w-4 h-4"
                />
                <span className="text-black">{val}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Fear */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">Fear (add)</p>
          <div className="flex justify-center gap-4">
            {[0, 1, 2].map((val) => (
              <label
                key={val}
                className="flex items-center gap-1 cursor-pointer"
              >
                <input
                  type="radio"
                  name="fear"
                  checked={fear === val}
                  onChange={() => setFear(val)}
                  className="w-4 h-4"
                />
                <span className="text-black">+{val}</span>
              </label>
            ))}
          </div>
        </div>
      </div>

      {/* Terrain Modifiers */}
      <div className="bg-[#A5D6A7] rounded-lg p-4 shadow-lg">
        <h3 className="text-center font-bold mb-4 text-black">
          TERRAIN MODIFIERS
        </h3>
        <div className="space-y-2">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetInDefilade}
              onChange={(e) => setTargetInDefilade(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">Target in defilade (+2)</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetCautious}
              onChange={(e) => setTargetCautious(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target is cautious moving (+3)
            </span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetInWoodBuildings}
              onChange={(e) => setTargetInWoodBuildings(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target in wood buildings (+3)
            </span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetInStoneBuildings}
              onChange={(e) => setTargetInStoneBuildings(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target in stone buildings (+4)
            </span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetInWoodsDirectFire}
              onChange={(e) => setTargetInWoodsDirectFire(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target in woods vs. direct fire (+2)
            </span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetInWoodsIndirectFire}
              onChange={(e) =>
                setTargetInWoodsIndirectFire(e.target.checked)
              }
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target in woods vs. indirect fire (+1)
            </span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetInCover}
              onChange={(e) => setTargetInCover(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">Target in cover (+1)</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetIsVehicle}
              onChange={(e) => setTargetIsVehicle(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm text-black">Target is a vehicle (-2)</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetEntrenchedDirectFire}
              onChange={(e) =>
                setTargetEntrenchedDirectFire(e.target.checked)
              }
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target entrenched vs. direct fire (+2)
            </span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={targetEntrenchedIndirectFire}
              onChange={(e) =>
                setTargetEntrenchedIndirectFire(e.target.checked)
              }
              className="w-4 h-4"
            />
            <span className="text-sm text-black">
              Target entrenched vs. indirect fire (+3)
            </span>
          </label>
        </div>
      </div>

      {/* Roll Dice Button */}
      <button
        onClick={handleRollDice}
        className="w-full bg-white text-black font-bold py-4 rounded-lg shadow-lg border-4 border-[#34495e] hover:bg-gray-100 transition-colors active:scale-95 transform"
      >
        🎲 ROLL DICE
      </button>

      {/* Results */}
      {result && (
        <div className="bg-yellow-300 rounded-lg p-6 shadow-lg border-4 border-black">
          <h3 className="font-bold text-xl mb-4 text-black text-center">
            INFANTRY FIRE TABLE RESULT
          </h3>

          <div className="space-y-3 text-black">
            <div className="bg-black/10 p-3 rounded">
              <p className="text-sm">
                <strong>FIREPOWER → COLUMN</strong>
              </p>
              <p className="ml-4">Firepower: {result.firepower_input}</p>
              <p className="ml-4">
                → Column: <strong>{result.column_letter}</strong>
              </p>
            </div>

            <div className="bg-black/10 p-3 rounded">
              <p className="text-sm">
                <strong>DIE ROLL + MODIFIERS → ROW</strong>
              </p>
              <p className="ml-4">Die Roll (D10): {result.actualDieRoll}</p>
              <p className="ml-4 text-sm">
                <strong>Modifiers:</strong>
              </p>
              <p className="ml-8 text-xs">Terrain: +{calculateModifiers()}</p>
              <p className="ml-8 text-xs">Leadership: -{leadership}</p>
              <p className="ml-8 text-xs">Fear: +{fear}</p>
              <p className="ml-4">
                <strong>Total Modifiers: {result.totalModifiers >= 0 ? "+" : ""}
                {result.totalModifiers}</strong>
              </p>
              <p className="ml-4">
                Modified Die Roll: {result.actualDieRoll} {result.totalModifiers >= 0 ? "+" : ""}
                {result.totalModifiers} = {result.modified_roll}
              </p>
              <p className="ml-4">
                → Row: {result.modified_roll} (limited 1-14)
              </p>
            </div>

            <div className="bg-black/10 p-3 rounded">
              <p className="text-sm">
                <strong>TABLE LOOKUP</strong>
              </p>
              <p className="ml-4">
                Table coordinate:{" "}
                <strong className="text-lg">{result.table_coord}</strong>
              </p>
              <p className="ml-4">(Column {result.column_letter}, Row{" "}
              {result.modified_roll})</p>
            </div>

            <div className="mt-6 pt-4 border-t-4 border-black">
              <div className="bg-white p-4 rounded-lg border-4 border-black">
                <p className="text-3xl font-bold text-center mb-2">
                  {getResultEmoji(result.result)} RESULT: {result.result}
                </p>
                <p className="text-center font-bold text-lg">
                  {result.decoded}
                </p>
              </div>
            </div>

            {result.result === "F" && (
              <div className="mt-4 bg-red-100 p-4 rounded border-2 border-red-500">
                <p className="font-bold text-center mb-2">
                  ⚠️ FLIP + OFFICER CHECK
                </p>
                <p className="text-sm">
                  Add 1 fear marker to the target unit.
                  <br />
                  <br />
                  Unit is not flipped, not eliminated.
                </p>
              </div>
            )}

            {result.result === "E" && (
              <div className="mt-4 bg-red-200 p-4 rounded border-2 border-red-700">
                <p className="font-bold text-center text-xl mb-2">
                  💀 ALL ELIMINATED! 💀
                </p>
                <p className="text-sm text-center">
                  The entire unit is completely destroyed!
                  <br />
                  Remove the unit from play.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}