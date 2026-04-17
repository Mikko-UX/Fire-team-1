import { useState } from "react";
import { Side, getWeaponsBySide, getWeaponByName } from "../data/weapons";
import { calculateKillNumber } from "../data/kill-table";
import { RadioGroup, RadioGroupItem } from "./ui/radio-group";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";

const FLAGS = {
  US: "🇺🇸",
  Soviet: "🇷🇺",
  FIN: "🇫🇮",
};

export function VehicleCombat() {
  const [shooterCountry, setShooterCountry] = useState<Side>("US");
  const [targetCountry, setTargetCountry] = useState<Side>("Soviet");
  const [shooterWeapon, setShooterWeapon] = useState("");
  const [targetWeapon, setTargetWeapon] = useState("");
  const [targetSide, setTargetSide] = useState<"Front" | "Flank">("Front");
  const [range, setRange] = useState("");
  const [leadership, setLeadership] = useState(0);
  const [fear, setFear] = useState(0);

  // Shooter modifiers
  const [shooterCautious, setShooterCautious] = useState(false);
  const [shooterChangeFacing, setShooterChangeFacing] = useState(false);
  const [shooterOpportunity, setShooterOpportunity] = useState(false);
  const [shooterOutOfSmoke, setShooterOutOfSmoke] = useState(false);
  const [shooterNight, setShooterNight] = useState(false);
  const [shooterFiringRamp, setShooterFiringRamp] = useState(false);

  // Target modifiers
  const [targetInBuildings, setTargetInBuildings] = useState(false);
  const [targetInSmoke, setTargetInSmoke] = useState(false);
  const [targetInWoods, setTargetInWoods] = useState(false);
  const [targetDefilade, setTargetDefilade] = useState(false);
  const [targetCautious, setTargetCautious] = useState(false);

  const [result, setResult] = useState<any>(null);
  const [diceRoll, setDiceRoll] = useState<number | null>(null);

  const shooterWeapons = getWeaponsBySide(shooterCountry);
  const targetWeapons = getWeaponsBySide(targetCountry);

  const calculateShooterModifiers = () => {
    let total = 0;
    if (shooterCautious) total += 4;
    if (shooterChangeFacing) total += 2;
    if (shooterOpportunity) total += 1;
    if (shooterOutOfSmoke) total += 4;
    if (shooterNight) total += 2;
    if (shooterFiringRamp) total -= 1;
    return total;
  };

  const calculateTargetModifiers = () => {
    let total = 0;
    if (targetInBuildings) total += 2;
    if (targetInSmoke) total += 3;
    if (targetInWoods) total += 2;
    if (targetDefilade) total += 1;
    if (targetCautious) total += 1;
    return total;
  };

  const handleCalculate = () => {
    if (!shooterWeapon || !targetWeapon || !range) {
      alert("Please select weapons and enter range");
      return;
    }

    const shooter = getWeaponByName(shooterWeapon);
    const target = getWeaponByName(targetWeapon);

    if (!shooter || !target) return;

    const shooterMods = calculateShooterModifiers();
    const targetMods = calculateTargetModifiers();
    const totalShifts = shooterMods + targetMods;

    const killResult = calculateKillNumber(
      shooter,
      target,
      targetSide,
      parseInt(range),
      totalShifts,
      leadership,
      fear
    );

    setResult(killResult);
  };

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Shooter Section */}
      <div className="bg-[#D3D3D3] rounded-lg p-4 shadow-lg">
        <h2 className="text-center font-bold mb-4 text-black">
          AMPUJA (SHOOTER)
        </h2>

        {/* Country Selection */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">
            Select country
          </p>
          <div className="flex justify-center gap-4">
            {(["US", "Soviet", "FIN"] as Side[]).map((country) => (
              <label key={country} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="shooterCountry"
                  checked={shooterCountry === country}
                  onChange={() => {
                    setShooterCountry(country);
                    setShooterWeapon("");
                  }}
                  className="w-4 h-4"
                />
                <span className="text-black">
                  {FLAGS[country]} {country}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Weapon Selection */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">Weapon</p>
          <select
            value={shooterWeapon}
            onChange={(e) => setShooterWeapon(e.target.value)}
            className="w-full p-2 rounded border-2 border-blue-500 text-black"
          >
            <option value="">Select weapon...</option>
            {shooterWeapons.map((w) => (
              <option key={w.name} value={w.name}>
                {w.name}
              </option>
            ))}
          </select>
        </div>

        {/* Leadership */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">Leadership</p>
          <div className="flex justify-center gap-4">
            {[0, 1, 2, 3].map((val) => (
              <label key={val} className="flex items-center gap-1 cursor-pointer">
                <input
                  type="radio"
                  name="leadership"
                  checked={leadership === val}
                  onChange={() => setLeadership(val)}
                  className="w-4 h-4"
                />
                <span className="text-black">+{val}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Fear */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">Fear</p>
          <div className="flex justify-center gap-4">
            {[0, 1, 2].map((val) => (
              <label key={val} className="flex items-center gap-1 cursor-pointer">
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

        {/* Range */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">
            Range (hexes)
          </p>
          <input
            type="number"
            value={range}
            onChange={(e) => setRange(e.target.value)}
            className="w-full p-2 rounded border-2 text-black text-center text-lg"
            placeholder="66"
          />
        </div>

        {/* Shooter Modifiers */}
        <div className="bg-[#E8E8E8] rounded p-3 mt-4">
          <p className="text-center font-bold mb-3 text-black">
            Shooter Modifiers (Column Shift)
          </p>
          <div className="space-y-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={shooterCautious}
                onChange={(e) => setShooterCautious(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">Cautious move (+4)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={shooterChangeFacing}
                onChange={(e) => setShooterChangeFacing(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">Change facing (+2)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={shooterOpportunity}
                onChange={(e) => setShooterOpportunity(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">Opportunity fire (+1)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={shooterOutOfSmoke}
                onChange={(e) => setShooterOutOfSmoke(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">Out of smoke (+4)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={shooterNight}
                onChange={(e) => setShooterNight(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">Night (+2)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={shooterFiringRamp}
                onChange={(e) => setShooterFiringRamp(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">In firing ramp (-1)</span>
            </label>
          </div>
        </div>
      </div>

      {/* Target Section */}
      <div className="bg-[#D3D3D3] rounded-lg p-4 shadow-lg">
        <h2 className="text-center font-bold mb-4 text-black">
          KOHDE (TARGET)
        </h2>

        {/* Country Selection */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">
            Select country
          </p>
          <div className="flex justify-center gap-4">
            {(["US", "Soviet", "FIN"] as Side[]).map((country) => (
              <label key={country} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="targetCountry"
                  checked={targetCountry === country}
                  onChange={() => {
                    setTargetCountry(country);
                    setTargetWeapon("");
                  }}
                  className="w-4 h-4"
                />
                <span className="text-black">
                  {FLAGS[country]} {country}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Target Weapon */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">
            Kohde (Target)
          </p>
          <select
            value={targetWeapon}
            onChange={(e) => setTargetWeapon(e.target.value)}
            className="w-full p-2 rounded border-2 border-blue-500 text-black"
          >
            <option value="">Select target...</option>
            {targetWeapons.map((w) => (
              <option key={w.name} value={w.name}>
                {w.name}
              </option>
            ))}
          </select>
        </div>

        {/* Hit Location */}
        <div className="mb-4">
          <p className="text-center font-bold mb-2 text-black">
            Hit location
          </p>
          <div className="flex justify-center gap-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="targetSide"
                checked={targetSide === "Front"}
                onChange={() => setTargetSide("Front")}
                className="w-4 h-4"
              />
              <span className="text-black">Etu (Front)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="targetSide"
                checked={targetSide === "Flank"}
                onChange={() => setTargetSide("Flank")}
                className="w-4 h-4"
              />
              <span className="text-black">Kylki (Flank)</span>
            </label>
          </div>
        </div>

        {/* Target Modifiers */}
        <div className="bg-[#E8E8E8] rounded p-3 mt-4">
          <p className="text-center font-bold mb-3 text-black">
            Target Modifiers (Column Shift)
          </p>
          <div className="space-y-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={targetInBuildings}
                onChange={(e) => setTargetInBuildings(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">In buildings (+2)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={targetInSmoke}
                onChange={(e) => setTargetInSmoke(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">In smoke (+3)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={targetInWoods}
                onChange={(e) => setTargetInWoods(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">In woods (+2)</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={targetDefilade}
                onChange={(e) => setTargetDefilade(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">
                Defilade/fire ramp (+1)
              </span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={targetCautious}
                onChange={(e) => setTargetCautious(e.target.checked)}
                className="w-4 h-4"
              />
              <span className="text-sm text-black">Cautious move (+1)</span>
            </label>
          </div>
        </div>
      </div>

      {/* Calculate Button */}
      <button
        onClick={handleCalculate}
        className="w-full bg-white text-black font-bold py-4 rounded-lg shadow-lg border-4 border-[#34495e] hover:bg-gray-100 transition-colors active:scale-95 transform"
      >
        🎯 CALCULATE KILL NUMBER
      </button>

      {/* Results */}
      {result && (
        <>
          <div className="bg-yellow-300 rounded-lg p-6 shadow-lg border-4 border-black">
            <h3 className="font-bold text-xl mb-4 text-black text-center">
              VEHICLE COMBAT RESULT
            </h3>
            <div className="space-y-2 text-black">
              <p>
                <strong>Weapon:</strong> {shooterWeapon}
              </p>
              <p>
                <strong>Target:</strong> {targetWeapon} ({targetSide})
              </p>
              <p>
                <strong>Ammo:</strong> {result.ammo}
              </p>
              <p>
                <strong>Range:</strong> {range} hexes
              </p>
              <p>
                <strong>Differential:</strong> Firepower {result.firepower} -
                Armor {result.armor} = {result.differential}
              </p>
              <p>
                <strong>Base Column:</strong> {result.base_col || "N/A"}
              </p>
              <p>
                <strong>Column Shift Modifiers:</strong> +
                {calculateShooterModifiers() + calculateTargetModifiers()}
              </p>
              <p>
                <strong>Leadership:</strong> -{leadership}
              </p>
              <p>
                <strong>Fear:</strong> +{fear}
              </p>
              <p>
                <strong>Final Column:</strong> {result.final_col || "N/A"}
              </p>
              <div className="mt-4 pt-4 border-t-4 border-black">
                <p className="text-3xl font-bold text-center mb-2">
                  {result.kill_number !== null
                    ? `KILL NUMBER: ${result.kill_number}`
                    : "KILL NUMBER: N/A"}
                </p>
              </div>
            </div>
          </div>

          {result.kill_number !== null && (
            <>
              <button
                onClick={() => setDiceRoll(Math.floor(Math.random() * 10) + 1)}
                className="w-full bg-white text-black font-bold py-4 rounded-lg shadow-lg border-4 border-[#34495e] hover:bg-gray-100 transition-colors active:scale-95 transform"
              >
                🎲 ROLL DICE
              </button>

              {diceRoll !== null && (
                <div className="bg-yellow-300 rounded-lg p-6 shadow-lg border-4 border-black">
                  <h3 className="font-bold text-xl mb-4 text-black text-center">
                    DICE ROLL RESULT
                  </h3>
                  <div className="space-y-3 text-black">
                    <p className="text-center">
                      <strong>Die Roll (D10):</strong> {diceRoll}
                    </p>
                    <p className="text-center">
                      <strong>Kill Number:</strong> {result.kill_number}
                    </p>
                    <div className="mt-4 pt-4 border-t-4 border-black">
                      <p className="text-2xl font-bold text-center">
                        {diceRoll <= result.kill_number
                          ? "✅ HIT - TARGET DESTROYED!"
                          : "❌ MISS - NO EFFECT"}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </>
          )}
        </>
      )}
    </div>
  );
}