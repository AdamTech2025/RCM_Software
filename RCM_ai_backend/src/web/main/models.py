from django.db import models

# Create your models here.
class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

class ClinicalNote(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='clinical_notes')
    encounter_date = models.DateTimeField()
    note_text = models.TextField()
    provider_name = models.CharField(max_length=100)
    note_type = models.CharField(max_length=50)  # e.g., Progress Note, Discharge Summary
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.note_type} - {self.patient} - {self.encounter_date}"

class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='diagnoses', null=True, blank=True)
    icd_code = models.CharField(max_length=20)
    description = models.TextField()
    diagnosis_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.icd_code} - {self.description}"

class Procedure(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='procedures')
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='procedures', null=True, blank=True)
    cpt_code = models.CharField(max_length=20)
    description = models.TextField()
    procedure_date = models.DateField()
    provider_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.cpt_code} - {self.description}"

class ProcessedDocument(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50)  # e.g., HL7, FHIR, PDF
    file_path = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    processing_errors = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.document_type} - {self.patient} - {self.created_at}"
