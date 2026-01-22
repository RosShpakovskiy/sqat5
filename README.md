## INSTALLATION

### 1. Clone repo
```bash
git clone https://github.com/RosShpakovskiy/sqat5
cd sqat5
```

### 2. Python pip installation
```bash
pip install -r requirements.txt
```

### 3. Allure installation (via Scoop)
**Copy this into PowerShell**
```bash
irm get.scoop.sh | iex
scoop install allure
```
## EXECUTION

### 1. Start
```bash
pytest -v --alluredir=allure-results
```

### 2. Allure results
```bash
allure serve allure-results
```
