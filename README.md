# OHLC CSV Check

A small command-line tool for catching bad candle rows before importing an OHLC CSV into a backtest or research notebook. It runs locally with Python 3.11+ and uses only the standard library.

```console
python ohlc_check.py examples/sample.csv
python -m unittest -v
```

Use a comma-delimited UTF-8 file with unique headers that include `timestamp,open,high,low,close`. Additional columns are accepted. Timestamps must be ISO 8601 with an explicit offset or `Z`. Prices must be finite numbers, with both open and close between low and high. The checker flags duplicate instants, chronological reversals and rows with the wrong number of fields. The included example is synthetic.

Exit codes are `0` for a pass, `1` for validation findings, and `2` for a read or CSV parsing error. Passing validation establishes basic file consistency. Session calendars, candle interval gaps and feed accuracy are outside these checks.

## بالعراقي

الأداة تفحص ملف الشموع قبل الباك تست. تطلع رقم السطر إذا الوقت مكرر أو الترتيب غلط أو قيم الأسعار غير متسقة. تشتغل محلياً وملف المثال بياناته اصطناعية.
