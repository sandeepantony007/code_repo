# Loafly Order Pipeline

## Create a virtual environment

Windows

```bash
python -m venv .venv
```

Activate

Command Prompt

```bash
.venv\Scripts\activate
```

PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create your environment file

```bash
copy env.example .env
```

Edit `.env`

```text
LOAFLY_API_KEY=your-api-key
```

Run

"""#Created run_pipeline.py outside the package and importing the package ti yse the ETL pipelines"""
```bash
python run_pipeline.py
```
