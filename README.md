# shelby-uploader-cli

> Python CLI wrapper for uploading files to Shelby Protocol.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Shelby](https://img.shields.io/badge/Shelby-Protocol-c6ff00?style=flat-square&labelColor=0a0a0f)

## Requirements

- Python 3.8+
- Shelby CLI: `npm install -g @shelby-protocol/cli`

## Usage
```bash
# Upload single file
python main.py file ./report.pdf

# Upload with custom name
python main.py file ./report.pdf --name docs/q4.pdf --expiry 90

# Upload directory
python main.py dir ./datasets --prefix ml/training
```

## Output
✅ docs/q4.pdf
✅ ml/training/batch_001.parquet
❌ ml/training/corrupt.parquet
📊 2 uploaded, 1 failed

## License
MIT
