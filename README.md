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
