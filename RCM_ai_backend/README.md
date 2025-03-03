# Medical Data Collector Agent

This project implements a medical data collector agent using Crew AI for extracting, processing, and standardizing medical data from various sources.

## Features

- **Data Extraction**: Extract patient data from HL7, FHIR, PDF, and text files
- **NLP Processing**: Process unstructured clinical text to extract medical entities
- **Data Standardization**: Standardize and clean medical data for consistency
- **Database Integration**: Store processed data in a Django database

## Requirements

- Python 3.8+
- Django
- CrewAI
- LangChain
- OpenAI API key
- Spacy
- Tesseract OCR (for PDF processing)
- Other dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Download Spacy model:
   ```
   python -m spacy download en_core_web_md
   ```

5. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your API keys and configuration.

6. Run Django migrations:
   ```
   cd src/web
   python manage.py migrate
   ```

## Usage

### Running the Data Collector Agent

You can run the data collector agent using the provided script:

```
cd src/web/agents
python run_data_collector.py --file <path-to-file> --verbose
```

Or to process an entire directory:

```
python run_data_collector.py --dir <path-to-directory> --output results.json
```

### Command Line Arguments

- `--file`: Path to a single file to process
- `--dir`: Path to a directory of files to process
- `--output`: Path to save the output JSON
- `--verbose`: Enable verbose output

## Data Flow

1. **Data Extraction**: The extraction agent identifies the document type and extracts raw data
2. **NLP Processing**: The NLP agent processes unstructured text to extract medical entities
3. **Data Standardization**: The standardization agent maps terms to standard codes and normalizes abbreviations
4. **Database Storage**: The processed data is saved to the Django database

## Project Structure

- `src/web/agents/data_collector.py`: Main implementation of the data collector agent
- `src/web/agents/run_data_collector.py`: Script to run the data collector agent
- `src/web/main/models.py`: Django models for storing medical data
- `src/data/`: Directory for medical data files

## Example

```python
from src.web.agents.data_collector import DataCollectorCrew, process_file

# Initialize the crew
crew = DataCollectorCrew()

# Process a sample file
result = process_file('path/to/clinical_note.txt')
print(result)
```

## License

[MIT License](LICENSE) 