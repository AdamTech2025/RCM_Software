import os
import re
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Django imports
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from main.models import Patient, ClinicalNote, Diagnosis, Procedure, ProcessedDocument

# Medical data processing imports
import spacy
import pytesseract
from PIL import Image
from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.condition import Condition as FHIRCondition
from fhir.resources.procedure import Procedure as FHIRProcedure
from hl7apy.parser import parse_message

# Load environment variables
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Check if API key exists and prompt if it doesn't
if not os.environ.get("OPENAI_API_KEY"):
    print("ERROR: OPENAI_API_KEY not found in environment variables or .env file")
    api_key = input("Please enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = api_key
    print("API key set for this session. For future runs, please add it to your .env file.")

# Initialize LLM with explicit API key
llm = ChatOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model="gpt-3.5-turbo",
    temperature=0,
)

# Initialize NLP model
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    # If model not found, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
    nlp = spacy.load("en_core_web_md")

# Define standalone tool functions outside the class
@tool
def extract_from_hl7(file_path: str) -> Dict[str, Any]:
    """
    Extract patient data from an HL7 message file.
    
    Args:
        file_path: Path to the HL7 message file
        
    Returns:
        Extracted patient data
    """
    try:
        with open(file_path, 'r') as f:
            hl7_content = f.read()
        
        # Parse HL7 message
        message = parse_message(hl7_content)
        
        # Extract patient data
        patient_data = {
            'patient_id': message.pid.patient_id.value,
            'first_name': message.pid.patient_name.given_name.value,
            'last_name': message.pid.patient_name.family_name.value,
            'date_of_birth': message.pid.date_of_birth.value,
            'gender': message.pid.administrative_sex.value,
        }
        
        # Extract diagnoses if available
        diagnoses = []
        if hasattr(message, 'dg1'):
            for diag in message.dg1:
                diagnoses.append({
                    'icd_code': diag.diagnosis_code.value,
                    'description': diag.diagnosis_description.value,
                    'diagnosis_date': diag.diagnosis_date.value
                })
        
        # Extract procedures if available
        procedures = []
        if hasattr(message, 'pr1'):
            for proc in message.pr1:
                procedures.append({
                    'cpt_code': proc.procedure_code.value,
                    'description': proc.procedure_description.value,
                    'procedure_date': proc.procedure_date.value
                })
        
        return {
            'patient': patient_data,
            'diagnoses': diagnoses,
            'procedures': procedures,
            'document_type': 'HL7'
        }
    
    except Exception as e:
        return {'error': f"Failed to extract data from HL7 file: {str(e)}"}

@tool
def extract_from_fhir(file_path: str) -> Dict[str, Any]:
    """
    Extract patient data from a FHIR JSON file.
    
    Args:
        file_path: Path to the FHIR JSON file
        
    Returns:
        Extracted patient data
    """
    try:
        with open(file_path, 'r') as f:
            fhir_json = json.load(f)
        
        # Process based on resource type
        resource_type = fhir_json.get('resourceType')
        
        if resource_type == 'Patient':
            patient = FHIRPatient.parse_obj(fhir_json)
            
            # Extract patient data
            name = patient.name[0] if patient.name else None
            patient_data = {
                'patient_id': patient.id,
                'first_name': name.given[0] if name and name.given else '',
                'last_name': name.family if name and name.family else '',
                'date_of_birth': patient.birthDate.isostring() if patient.birthDate else None,
                'gender': patient.gender if patient.gender else ''
            }
            
            return {
                'patient': patient_data,
                'document_type': 'FHIR'
            }
        
        elif resource_type == 'Condition':
            condition = FHIRCondition.parse_obj(fhir_json)
            
            # Extract diagnosis data
            diagnosis = {
                'patient_id': condition.subject.reference.split('/')[-1] if condition.subject else None,
                'icd_code': condition.code.coding[0].code if condition.code and condition.code.coding else '',
                'description': condition.code.text if condition.code else '',
                'diagnosis_date': condition.onsetDateTime.isostring() if condition.onsetDateTime else None
            }
            
            return {
                'diagnosis': diagnosis,
                'document_type': 'FHIR'
            }
        
        elif resource_type == 'Procedure':
            procedure = FHIRProcedure.parse_obj(fhir_json)
            
            # Extract procedure data
            proc_data = {
                'patient_id': procedure.subject.reference.split('/')[-1] if procedure.subject else None,
                'cpt_code': procedure.code.coding[0].code if procedure.code and procedure.code.coding else '',
                'description': procedure.code.text if procedure.code else '',
                'procedure_date': procedure.performedDateTime.isostring() if procedure.performedDateTime else None
            }
            
            return {
                'procedure': proc_data,
                'document_type': 'FHIR'
            }
        
        else:
            return {'error': f"Unsupported FHIR resource type: {resource_type}"}
    
    except Exception as e:
        return {'error': f"Failed to extract data from FHIR file: {str(e)}"}

@tool
def extract_from_pdf(file_path: str) -> Dict[str, Any]:
    """
    Extract text from a PDF file using OCR if needed.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        # For simplicity, we'll use pytesseract to extract text from PDF
        # In a real implementation, you would use a PDF library like PyPDF2 or pdfminer
        # and only use OCR when needed
        
        # Convert PDF to image (simplified for demonstration)
        # In a real implementation, you would use a library like pdf2image
        image = Image.open(file_path)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(image)
        
        return {
            'content': text,
            'document_type': 'PDF'
        }
    
    except Exception as e:
        return {'error': f"Failed to extract data from PDF file: {str(e)}"}

@tool
def extract_from_text(file_path: str) -> Dict[str, Any]:
    """
    Extract information from a plain text clinical note.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Extracted text content
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        return {
            'content': content,
            'document_type': 'TEXT'
        }
    
    except Exception as e:
        return {'error': f"Failed to extract data from text file: {str(e)}"}

# Define all other tool functions here...
@tool
def process_clinical_text(text: str) -> Dict[str, Any]:
    """
    Process clinical text to extract structured information.
    
    Args:
        text: Clinical text to process
        
    Returns:
        Structured information extracted from the text
    """
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract basic entities
    entities = [
        {
            'text': ent.text,
            'label': ent.label_,
            'start': ent.start_char,
            'end': ent.end_char
        }
        for ent in doc.ents
    ]
    
    # Extract sections using regex patterns (simplified)
    sections = {}
    section_patterns = [
        (r'(?i)history of present illness:?(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', 'history_of_present_illness'),
        (r'(?i)past medical history:?(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', 'past_medical_history'),
        (r'(?i)medications:?(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', 'medications'),
        (r'(?i)assessment:?(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', 'assessment'),
        (r'(?i)plan:?(.*?)(?=\n\s*\n|\n\s*[A-Z]|$)', 'plan')
    ]
    
    for pattern, section_name in section_patterns:
        matches = re.search(pattern, text)
        if matches:
            sections[section_name] = matches.group(1).strip()
    
    return {
        'entities': entities,
        'sections': sections
    }

@tool
def extract_medical_entities(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract medical entities from clinical text.
    
    Args:
        text: Clinical text to process
        
    Returns:
        Extracted medical entities
    """
    # Process the text with spaCy
    doc = nlp(text)
    
    # Extract diagnoses using pattern matching (simplified)
    diagnoses = []
    diagnosis_patterns = [
        r'(?i)diagnosis:?\s*(.*?)(?=\n|$)',
        r'(?i)assessment:?\s*(.*?)(?=\n|$)',
        r'(?i)impression:?\s*(.*?)(?=\n|$)',
        r'(?i)dx:?\s*(.*?)(?=\n|$)'
    ]
    
    for pattern in diagnosis_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            diagnoses.append({
                'description': match.group(1).strip(),
                'icd_code': None  # To be filled by standardization agent
            })
    
    # Extract procedures using pattern matching (simplified)
    procedures = []
    procedure_patterns = [
        r'(?i)procedure:?\s*(.*?)(?=\n|$)',
        r'(?i)operation:?\s*(.*?)(?=\n|$)',
        r'(?i)performed:?\s*(.*?)(?=\n|$)'
    ]
    
    for pattern in procedure_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            procedures.append({
                'description': match.group(1).strip(),
                'cpt_code': None  # To be filled by standardization agent
            })
    
    return {
        'diagnoses': diagnoses,
        'procedures': procedures
    }

@tool
def normalize_medical_terms(terms: List[str]) -> List[Dict[str, str]]:
    """
    Normalize medical terms and abbreviations.
    
    Args:
        terms: List of medical terms to normalize
        
    Returns:
        Normalized terms
    """
    # Common medical abbreviations (simplified)
    abbreviations = {
        'HTN': 'Hypertension',
        'DM': 'Diabetes Mellitus',
        'COPD': 'Chronic Obstructive Pulmonary Disease',
        'CHF': 'Congestive Heart Failure',
        'CAD': 'Coronary Artery Disease',
        'MI': 'Myocardial Infarction',
        'CVA': 'Cerebrovascular Accident',
        'UTI': 'Urinary Tract Infection',
        'URI': 'Upper Respiratory Infection',
        'LBP': 'Low Back Pain'
    }
    
    normalized_terms = []
    for term in terms:
        normalized = term
        
        # Check if term is an abbreviation
        if term.upper() in abbreviations:
            normalized = abbreviations[term.upper()]
        
        normalized_terms.append({
            'original': term,
            'normalized': normalized
        })
    
    return normalized_terms

@tool
def standardize_diagnosis_codes(diagnoses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Standardize diagnosis descriptions to ICD-10 codes.
    
    Args:
        diagnoses: List of diagnoses to standardize
        
    Returns:
        Standardized diagnoses with ICD-10 codes
    """
    # Simplified mapping of common diagnoses to ICD-10 codes
    icd10_mapping = {
        'hypertension': 'I10',
        'diabetes': 'E11.9',
        'diabetes mellitus': 'E11.9',
        'type 2 diabetes': 'E11.9',
        'asthma': 'J45.909',
        'pneumonia': 'J18.9',
        'urinary tract infection': 'N39.0',
        'uti': 'N39.0',
        'acute bronchitis': 'J20.9',
        'bronchitis': 'J20.9',
        'depression': 'F32.9',
        'anxiety': 'F41.9',
        'gerd': 'K21.9',
        'gastroesophageal reflux disease': 'K21.9',
        'congestive heart failure': 'I50.9',
        'chf': 'I50.9',
        'coronary artery disease': 'I25.10',
        'cad': 'I25.10'
    }
    
    standardized_diagnoses = []
    for diagnosis in diagnoses:
        description = diagnosis['description'].lower()
        icd_code = None
        
        # Check for exact matches
        for term, code in icd10_mapping.items():
            if term in description:
                icd_code = code
                break
        
        standardized_diagnoses.append({
            'description': diagnosis['description'],
            'icd_code': icd_code or diagnosis.get('icd_code')
        })
    
    return standardized_diagnoses

@tool
def standardize_procedure_codes(procedures: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Standardize procedure descriptions to CPT codes.
    
    Args:
        procedures: List of procedures to standardize
        
    Returns:
        Standardized procedures with CPT codes
    """
    # Simplified mapping of common procedures to CPT codes
    cpt_mapping = {
        'office visit': '99213',
        'chest x-ray': '71045',
        'echocardiogram': '93306',
        'colonoscopy': '45378',
        'upper endoscopy': '43235',
        'mri brain': '70553',
        'ct scan abdomen': '74177',
        'complete blood count': '85025',
        'cbc': '85025',
        'comprehensive metabolic panel': '80053',
        'cmp': '80053',
        'lipid panel': '80061',
        'flu vaccine': '90688',
        'influenza vaccine': '90688'
    }
    
    standardized_procedures = []
    for procedure in procedures:
        description = procedure['description'].lower()
        cpt_code = None
        
        # Check for exact matches
        for term, code in cpt_mapping.items():
            if term in description:
                cpt_code = code
                break
        
        standardized_procedures.append({
            'description': procedure['description'],
            'cpt_code': cpt_code or procedure.get('cpt_code')
        })
    
    return standardized_procedures

@tool
def normalize_abbreviations(text: str) -> str:
    """
    Normalize medical abbreviations in text.
    
    Args:
        text: Text containing medical abbreviations
        
    Returns:
        Text with expanded abbreviations
    """
    # Common medical abbreviations
    abbreviations = {
        'HTN': 'Hypertension',
        'DM': 'Diabetes Mellitus',
        'COPD': 'Chronic Obstructive Pulmonary Disease',
        'CHF': 'Congestive Heart Failure',
        'CAD': 'Coronary Artery Disease',
        'MI': 'Myocardial Infarction',
        'CVA': 'Cerebrovascular Accident',
        'UTI': 'Urinary Tract Infection',
        'URI': 'Upper Respiratory Infection',
        'LBP': 'Low Back Pain',
        'Hx': 'History',
        'Dx': 'Diagnosis',
        'Tx': 'Treatment',
        'Fx': 'Fracture',
        'Sx': 'Symptoms',
        'Pt': 'Patient',
        'yo': 'year old',
        'y/o': 'year old',
        'b/l': 'bilateral',
        'w/': 'with',
        'w/o': 'without',
        's/p': 'status post',
        'c/o': 'complains of',
        'h/o': 'history of'
    }
    
    normalized_text = text
    for abbr, expansion in abbreviations.items():
        # Replace abbreviations with word boundaries
        pattern = r'\b' + re.escape(abbr) + r'\b'
        normalized_text = re.sub(pattern, expansion, normalized_text, flags=re.IGNORECASE)
    
    return normalized_text

@tool
def remove_duplicates(data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Remove duplicate entries from the data.
    
    Args:
        data: Data containing potential duplicates
        
    Returns:
        Data with duplicates removed
    """
    result = {}
    
    for key, items in data.items():
        if not items:
            result[key] = []
            continue
        
        # Convert to DataFrame for easier deduplication
        df = pd.DataFrame(items)
        
        # Drop duplicates
        df_deduped = df.drop_duplicates()
        
        # Convert back to list of dictionaries
        result[key] = df_deduped.to_dict('records')
    
    return result

# Now update your DataCollectorCrew class to use these standalone functions
class DataCollectorCrew:
    """
    A crew of agents for medical data collection and processing.
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the DataCollectorCrew.
        
        Args:
            data_dir: Directory containing medical data files
        """
        self.data_dir = data_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
        self.setup_agents()
        self.setup_crew()
    
    def setup_agents(self):
        """Set up the agents for the crew."""
        
        # Data Extraction Agent
        self.extraction_agent = Agent(
            role="Medical Data Extraction Specialist",
            goal="Extract structured data from various medical document formats",
            backstory="""You are an expert in extracting medical information from various 
            document formats including HL7, FHIR, PDFs, and clinical notes. You have years 
            of experience working with healthcare data systems and understand medical 
            terminology and coding standards.""",
            verbose=True,
            allow_delegation=True,
            tools=[
                extract_from_hl7,
                extract_from_fhir,
                extract_from_pdf,
                extract_from_text
            ],
            llm=llm
        )
        
        # NLP Processing Agent
        self.nlp_agent = Agent(
            role="Medical NLP Specialist",
            goal="Process unstructured clinical text to extract medical entities",
            backstory="""You are a specialist in natural language processing for healthcare. 
            You can identify medical terms, diagnoses, procedures, medications, and other 
            relevant information from unstructured clinical notes and reports.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                process_clinical_text,
                extract_medical_entities,
                normalize_medical_terms
            ],
            llm=llm
        )
        
        # Data Standardization Agent
        self.standardization_agent = Agent(
            role="Medical Data Standardization Specialist",
            goal="Standardize and clean medical data for consistency",
            backstory="""You are an expert in medical terminologies and coding systems 
            including ICD-10, CPT, SNOMED CT, and LOINC. You ensure that all medical 
            data is properly coded, normalized, and follows healthcare data standards.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                standardize_diagnosis_codes,
                standardize_procedure_codes,
                normalize_abbreviations,
                remove_duplicates
            ],
            llm=llm
        )
    
    def setup_crew(self):
        """Set up the crew with the agents and their tasks."""
        
        # Define tasks
        extraction_task = Task(
            description="""
            Extract patient data from various medical document formats.
            1. Identify the document type (HL7, FHIR, PDF, text)
            2. Extract patient demographics, encounter details, and clinical information
            3. Convert the extracted data into a structured format
            """,
            agent=self.extraction_agent,
            expected_output="Structured patient data extracted from medical documents"
        )
        
        nlp_task = Task(
            description="""
            Process unstructured clinical text to extract medical entities.
            1. Analyze clinical notes and reports
            2. Identify diagnoses, procedures, medications, and other medical entities
            3. Extract relationships between medical entities
            """,
            agent=self.nlp_agent,
            expected_output="Medical entities extracted from clinical text"
        )
        
        standardization_task = Task(
            description="""
            Standardize and clean the extracted medical data.
            1. Map diagnoses to standard ICD-10 codes
            2. Map procedures to standard CPT codes
            3. Normalize medical abbreviations and terms
            4. Remove duplicate entries and fix formatting issues
            """,
            agent=self.standardization_agent,
            expected_output="Standardized and cleaned medical data"
        )
        
        # Create the crew
        self.crew = Crew(
            agents=[self.extraction_agent, self.nlp_agent, self.standardization_agent],
            tasks=[extraction_task, nlp_task, standardization_task],
            verbose=True,
            process=Process.sequential
        )
    
    def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the data collection and processing crew.
        
        Args:
            input_data: Optional input data to process
            
        Returns:
            Processed and standardized medical data
        """
        if input_data:
            result = self.crew.kickoff(inputs=input_data)
        else:
            result = self.crew.kickoff()
        
        return result

def process_file(file_path: str) -> Dict[str, Any]:
    """
    Process a medical data file using the DataCollectorCrew.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        Processing results as a structured JSON object
    """
    # Initialize the crew
    crew = DataCollectorCrew()
    
    # Run the crew on the file
    result = crew.run({'file_path': file_path})
    
    # Convert CrewOutput to a structured dictionary
    structured_data = extract_structured_data(result)
    
    # Save the processed data to the database
    db_result = save_to_database(structured_data)
    
    return structured_data

def extract_structured_data(result) -> Dict[str, Any]:
    """
    Extract and structure data from the crew result.
    
    Args:
        result: Result from the crew run
        
    Returns:
        Structured data in the required format
    """
    # Initialize the structured data with empty values
    structured_data = {
        "patient": {
            "name": "",
            "mrn": "",
            "dob": "",
            "gender": ""
        },
        "visit": {
            "date": "",
            "provider": {
                "name": "",
                "specialty": "",
                "license": ""
            }
        },
        "diagnoses": [],
        "procedures": [],
        "medications": [],
        "diagnostic_studies": {},
        "treatment_plan": [],
        "billing": {
            "icd_10_codes": [],
            "cpt_codes": []
        },
        "signature": {
            "provider": "",
            "date_signed": ""
        }
    }
    
    # Try to extract data from the result
    try:
        # Convert result to string for regex parsing
        result_str = str(result)
        
        # Extract diagnoses
        diagnoses = extract_diagnoses(result_str)
        if diagnoses:
            structured_data["diagnoses"] = diagnoses
            # Add ICD codes to billing
            for diagnosis in diagnoses:
                if "code" in diagnosis and diagnosis["code"] and diagnosis["code"] not in structured_data["billing"]["icd_10_codes"]:
                    structured_data["billing"]["icd_10_codes"].append(diagnosis["code"])
        
        # Extract medications
        medications = extract_medications(result_str)
        if medications:
            structured_data["medications"] = medications
        
        # Extract procedures
        procedures = extract_procedures(result_str)
        if procedures:
            structured_data["procedures"] = procedures
            # Add CPT codes to billing
            for procedure in procedures:
                if "code" in procedure and procedure["code"] and procedure["code"] not in structured_data["billing"]["cpt_codes"]:
                    structured_data["billing"]["cpt_codes"].append(procedure["code"])
        
    except Exception as e:
        print(f"Error extracting structured data: {str(e)}")
    
    return structured_data

def save_to_database(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Save processed data to the database.
    
    Args:
        data: Processed structured data to save
        
    Returns:
        Result of the database operation
    """
    try:
        # Database saving logic here
        # ...
        
        return {
            "status": "success",
            "message": "Data saved to database successfully"
        }
    except Exception as e:
        return {
            "error": f"Failed to save data to database: {str(e)}"
        }

def process_directory(directory_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Process all medical data files in a directory using the DataCollectorCrew.
    
    Args:
        directory_path: Path to the directory containing files to process
        
    Returns:
        Processing results for all files
    """
    results = {
        "processed_files": [],
        "errors": []
    }
    
    try:
        # Get all files in the directory
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        
        # Process each file
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            print(f"Processing file: {file_path}")
            
            try:
                # Process the file
                result = process_file(file_path)
                
                # Add to results
                results["processed_files"].append({
                    "file_name": file_name,
                    "file_path": file_path,
                    "result": result
                })
                
            except Exception as e:
                # Log the error
                error_message = f"Error processing file {file_path}: {str(e)}"
                print(error_message)
                
                # Add to errors
                results["errors"].append({
                    "file_name": file_name,
                    "file_path": file_path,
                    "error": str(e)
                })
    
    except Exception as e:
        # Log the error
        error_message = f"Error processing directory {directory_path}: {str(e)}"
        print(error_message)
        
        # Add to errors
        results["errors"].append({
            "directory_path": directory_path,
            "error": str(e)
        })
    
    return results

if __name__ == "__main__":
    # Example usage
    crew = DataCollectorCrew()
    
    # Process a sample file
    sample_file = os.path.join(crew.data_dir, 'sample.txt')
    
    # Create a sample file if it doesn't exist
    if not os.path.exists(sample_file):
        with open(sample_file, 'w') as f:
            f.write("""
            Patient: John Doe
            DOB: 01/15/1965
            Gender: Male
            
            History of Present Illness:
            Patient presents with complaints of chest pain for the past 3 days. Pain is described as pressure-like, 
            radiating to the left arm. Associated with shortness of breath and diaphoresis. 
            Patient has a history of HTN and DM.
            
            Assessment:
            1. Acute coronary syndrome
            2. Hypertension
            3. Type 2 Diabetes Mellitus
            
            Plan:
            1. Admit to hospital
            2. Cardiac enzymes
            3. ECG
            4. Cardiology consult
            """)
    
    result = process_file(sample_file)
    print(json.dumps(result, indent=2))
