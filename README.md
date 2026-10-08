# CodePilot - AI Code Autocomplete Tool

Fine-tuned CodeGPT-small-py for Python code completion.

## Project Structure

    CodeAutocomplete/
    data/processed/       train.txt, val.txt
    model/fine_tuned/     config.json, pytorch_model.bin, tokenizer files
    src/inference.py      inference helper
    app/streamlit_app.py  web UI
    logs/                 training_metrics.json
    requirements.txt
    README.md

## Run Locally (no retraining needed)

    pip install -r requirements.txt
    streamlit run app/streamlit_app.py

The model is already trained and saved in model/fine_tuned/

---

## Repository guide

### Contents

- [CodeAutocomplete_Colab.ipynb](CodeAutocomplete_Colab.ipynb)
- [README.md](README.md)
- [app](app)
- [logs](logs)
- [requirements.txt](requirements.txt)
- [src](src)

### Getting started

```bash
git clone https://github.com/Raimal-Raja/Autocode_completion_tool_deeplearning.git
cd Autocode_completion_tool_deeplearning
```

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r "requirements.txt"
```

```bash
python -m streamlit run app/streamlit_app.py
```

### Configuration and limitations

Training and inference require compatible model weights and dependencies; model generation was not exercised.

### Validation

Reviewed on 2026-10-08. Python syntax checks passed for 2 source files. Syntax validation does not establish runtime correctness or dependency compatibility.

### Contributions

Describe the issue, reproduction steps, environment, and expected behavior when proposing a change. Keep generated environments, credentials, and unnecessary build artifacts out of new commits.

### License

No top-level license file was found during this review.
