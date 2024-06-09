from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForMaskedLM, AutoTokenizer
import os
import git
import logging
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the directory where models will be stored
models_dir = "D:/laragon/www/omnimodel/models"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_model():
    repo_url = request.form.get("repo_url")
    model_name = request.form.get("model_name")

    if not repo_url or not model_name:
        return jsonify({"error": "Repository URL and model name are required."}), 400

    model_path = os.path.join(models_dir, model_name)

    try:
        if not os.path.exists(model_path):
            logging.info(f"Cloning from {repo_url} into {model_path}")
            git.Repo.clone_from(repo_url, model_path)
            return (
                jsonify({"message": f"Model {model_name} downloaded successfully!"}),
                200,
            )
        else:
            logging.error(f"Model directory {model_name} already exists.")
            return (
                jsonify({"error": f"Model directory {model_name} already exists."}),
                400,
            )
    except Exception as e:
        logging.error(f"Error downloading model {model_name}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/download_small_model", methods=["POST"])
def download_small_model():
    model_name = request.json.get("model_name", "distilbert-base-uncased")
    model_path = os.path.join(models_dir, model_name)

    try:
        if not os.path.exists(model_path):
            logging.info(f"Downloading {model_name} model to {model_path}")
            model = AutoModelForMaskedLM.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model.save_pretrained(model_path)
            tokenizer.save_pretrained(model_path)
            return (
                jsonify({"message": f"Model {model_name} downloaded successfully!"}),
                200,
            )
        else:
            logging.error(f"Model directory {model_name} already exists.")
            return (
                jsonify({"error": f"Model directory {model_name} already exists."}),
                400,
            )
    except Exception as e:
        logging.error(f"Error downloading model {model_name}: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    app.run(host="0.0.0.0", port=5000)
