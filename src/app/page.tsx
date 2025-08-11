'use client';

import { useState, useEffect } from 'react';

export default function TipCalculator() {
  const [billAmount, setBillAmount] = useState<string>('');
  const [tipPercentage, setTipPercentage] = useState<number>(18);
  const [customTipPercentage, setCustomTipPercentage] = useState<string>('');
  const [numberOfPeople, setNumberOfPeople] = useState<number>(1);
  const [tipAmount, setTipAmount] = useState<number>(0);
  const [totalAmount, setTotalAmount] = useState<number>(0);
  const [perPersonAmount, setPerPersonAmount] = useState<number>(0);

  const presetTips = [15, 18, 20, 22, 25];

  useEffect(() => {
    if (billAmount && !isNaN(parseFloat(billAmount))) {
      const bill = parseFloat(billAmount);
      const currentTipPercentage = customTipPercentage ? parseFloat(customTipPercentage) : tipPercentage;
      
      if (!isNaN(currentTipPercentage)) {
        const tip = (bill * currentTipPercentage) / 100;
        const total = bill + tip;
        const perPerson = total / numberOfPeople;
        
        setTipAmount(tip);
        setTotalAmount(total);
        setPerPersonAmount(perPerson);
      }
    } else {
      setTipAmount(0);
      setTotalAmount(0);
      setPerPersonAmount(0);
    }
  }, [billAmount, tipPercentage, customTipPercentage, numberOfPeople]);

  const handlePresetTip = (percentage: number) => {
    setTipPercentage(percentage);
    setCustomTipPercentage('');
  };

  const handleCustomTipChange = (value: string) => {
    setCustomTipPercentage(value);
    if (value === '') {
      setTipPercentage(18);
    }
  };

  const clearAll = () => {
    setBillAmount('');
    setTipPercentage(18);
    setCustomTipPercentage('');
    setNumberOfPeople(1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-md mx-auto bg-white rounded-2xl shadow-xl p-6">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">💰 Tip Calculator</h1>
          <p className="text-gray-600">Calculate tips and split bills easily</p>
        </div>

        <div className="space-y-6">
          {/* Bill Amount Input */}
          <div>
            <label htmlFor="billAmount" className="block text-sm font-medium text-gray-700 mb-2">
              Bill Amount
            </label>
            <div className="relative">
              <span className="absolute left-3 top-3 text-gray-500 text-lg">$</span>
              <input
                id="billAmount"
                type="number"
                step="0.01"
                min="0"
                placeholder="0.00"
                value={billAmount}
                onChange={(e) => setBillAmount(e.target.value)}
                className="w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-lg text-gray-900 bg-white"
              />
            </div>
          </div>

          {/* Tip Percentage */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Tip Percentage
            </label>
            <div className="grid grid-cols-5 gap-2 mb-3">
              {presetTips.map((percentage) => (
                <button
                  key={percentage}
                  onClick={() => handlePresetTip(percentage)}
                  className={`py-2 px-3 rounded-lg font-medium transition-all ${
                    tipPercentage === percentage && !customTipPercentage
                      ? 'bg-blue-500 text-white shadow-lg'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {percentage}%
                </button>
              ))}
            </div>
            <input
              type="number"
              step="0.1"
              min="0"
              max="100"
              placeholder="Custom %"
              value={customTipPercentage}
              onChange={(e) => handleCustomTipChange(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 bg-white"
            />
          </div>

          {/* Number of People */}
          <div>
            <label htmlFor="numberOfPeople" className="block text-sm font-medium text-gray-700 mb-2">
              Number of People
            </label>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setNumberOfPeople(Math.max(1, numberOfPeople - 1))}
                className="w-10 h-10 bg-gray-200 hover:bg-gray-300 rounded-full flex items-center justify-center font-bold text-gray-700"
              >
                -
              </button>
              <input
                id="numberOfPeople"
                type="number"
                min="1"
                value={numberOfPeople}
                onChange={(e) => setNumberOfPeople(Math.max(1, parseInt(e.target.value) || 1))}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-center text-lg text-gray-900 bg-white"
              />
              <button
                onClick={() => setNumberOfPeople(numberOfPeople + 1)}
                className="w-10 h-10 bg-gray-200 hover:bg-gray-300 rounded-full flex items-center justify-center font-bold text-gray-700"
              >
                +
              </button>
            </div>
          </div>

          {/* Results */}
          <div className="bg-gray-50 rounded-lg p-4 space-y-3">
            <h3 className="text-lg font-semibold text-gray-800 mb-3">Summary</h3>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Tip Amount:</span>
              <span className="text-lg font-semibold text-green-600">
                ${tipAmount.toFixed(2)}
              </span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total Amount:</span>
              <span className="text-lg font-semibold text-blue-600">
                ${totalAmount.toFixed(2)}
              </span>
            </div>
            
            <div className="flex justify-between items-center border-t pt-3">
              <span className="text-gray-600">Per Person:</span>
              <span className="text-xl font-bold text-purple-600">
                ${perPersonAmount.toFixed(2)}
              </span>
            </div>
          </div>

          {/* Clear Button */}
          <button
            onClick={clearAll}
            className="w-full py-3 bg-gray-500 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors"
          >
            Clear All
          </button>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Perfect for restaurants, cafes, and group dining! 🍽️</p>
        </div>
      </div>

      {/* Structured Data for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Tip Calculator",
            "description": "Calculate tips and split bills effortlessly with customizable percentages",
            "url": process.env.NODE_ENV === 'production' ? 'https://your-domain.vercel.app' : 'http://localhost:3000',
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "Web Browser",
            "offers": {
              "@type": "Offer",
              "price": "0",
              "priceCurrency": "USD"
            }
          })
        }}
      />
    </div>
  );
}