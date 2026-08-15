# Yalvon360 PSX Divergence Screener v9

## Why the screenshot showed empty divergence sections
The previous implementation had several overly restrictive / mismatched conditions:

1. It tested only the two newest swing points, so a valid divergence could disappear as soon as a newer non-divergent pivot appeared.
2. Divergence magnitude filters (1.5% price and 5 RSI points) were stricter than the user's stated rules and suppressed legitimate setups.
3. A weekly/monthly divergence could be found but the personalized setup then checked the **daily** RSI pivot and daily structure, incorrectly rejecting the higher-timeframe signal.
4. Uptrend/downtrend classification used only the latest daily structure, rather than the timeframe that generated the divergence.

## v9 changes
- Searches several recent swing-pivot pairs and returns the newest qualifying mathematical divergence.
- Uses more responsive swing detection (order 5) and 120 daily bars for divergence discovery.
- Reduces invented noise filters to 0.25% price difference and 2 RSI points; the user's actual RSI zone rules remain unchanged (bullish <=50, strong <=30, bearish >=70, strong >=90).
- Computes 1D, 1W and 1M independently and carries each timeframe's structure into the result.
- Personalized bullish setup uses the same timeframe's divergence + RSI zone + downtrend structure, plus 52-week-low <=3% and green Heikin-Ashi confirmation.
- Personalized bearish setup uses the same timeframe's divergence + RSI zone + uptrend structure + red Heikin-Ashi confirmation.
- Market-wide bullish/bearish and uptrend/downtrend sections now aggregate valid hits from all three timeframes.
- Added scan summary showing universe size, usable data, skipped history and failures so an apparently empty result can be diagnosed immediately.
- Full-market background worker architecture from v8 is preserved.
