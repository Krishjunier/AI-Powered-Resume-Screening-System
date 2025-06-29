import re
import string
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import PyPDF2
import docx
import io
import json

app = Flask(__name__)

class ResumeScanner:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            lowercase=True,
            max_features=1000,
            ngram_range=(1, 2)
        )
        
        # Predefined skill categories
        self.skill_keywords = {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'nodejs',
                'express', 'laravel', 'rails', 'asp.net', 'tensorflow', 'pytorch'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sqlite', 'cassandra', 'dynamodb'
            ],
            'tools': [
                'git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp',
                'linux', 'windows', 'mac', 'jira', 'confluence', 'slack'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical', 'creative', 'adaptable', 'organized'
            ]
        }
    
    def extract_text_from_pdf(self, file_content):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, file_content):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text = self.preprocess_text(text)
        found_skills = {}
        
        for category, skills in self.skill_keywords.items():
            found_skills[category] = []
            for skill in skills:
                if skill.lower() in text:
                    found_skills[category].append(skill)
        
        return found_skills
    
    def extract_contact_info(self, text):
        """Extract contact information from resume"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        return {
            'emails': emails,
            'phones': [''.join(phone) for phone in phones]
        }
    
    def calculate_similarity(self, resume_text, job_description):
        """Calculate similarity between resume and job description using TF-IDF and cosine similarity"""
        documents = [self.preprocess_text(resume_text), self.preprocess_text(job_description)]
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similarity_score
        except Exception as e:
            return 0.0
    
    def rank_candidates(self, candidates, job_description):
        """Rank candidates based on their similarity to job description"""
        ranked_candidates = []
        
        for candidate in candidates:
            similarity_score = self.calculate_similarity(candidate['resume_text'], job_description)
            candidate['similarity_score'] = similarity_score
            candidate['percentage_match'] = round(similarity_score * 100, 2)
            ranked_candidates.append(candidate)
        
        # Sort by similarity score in descending order
        ranked_candidates.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return ranked_candidates

# Initialize the scanner
scanner = ResumeScanner()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Scanner - Smart Hiring Solution</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: float 20s infinite linear;
        }
        
        @keyframes float {
            0% { transform: translate(-50%, -50%) rotate(0deg); }
            100% { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        .header h1 {
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 15px;
            position: relative;
            z-index: 2;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
            position: relative;
            z-index: 2;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0;
            min-height: 600px;
        }
        
        .input-section {
            padding: 40px;
            background: #fafafa;
            border-right: 1px solid #e5e7eb;
        }
        
        .results-section {
            padding: 40px;
            background: white;
            overflow-y: auto;
            max-height: 700px;
        }
        
        .section-title {
            font-size: 1.5em;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .form-card {
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            margin-bottom: 25px;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }
        
        .form-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-label {
            display: block;
            font-weight: 600;
            color: #374151;
            margin-bottom: 8px;
            font-size: 0.95em;
        }
        
        .form-textarea {
            width: 100%;
            min-height: 120px;
            padding: 16px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
            transition: all 0.3s ease;
            background: #fafafa;
        }
        
        .form-textarea:focus {
            outline: none;
            border-color: #4f46e5;
            background: white;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }
        
        .file-upload-area {
            border: 2px dashed #d1d5db;
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            background: #fafafa;
            position: relative;
            overflow: hidden;
        }
        
        .file-upload-area:hover {
            border-color: #4f46e5;
            background: #f8faff;
        }
        
        .file-upload-area.dragover {
            border-color: #4f46e5;
            background: #eff6ff;
            transform: scale(1.02);
        }
        
        .file-upload-icon {
            font-size: 3em;
            color: #9ca3af;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        
        .file-upload-area:hover .file-upload-icon {
            color: #4f46e5;
            transform: scale(1.1);
        }
        
        .file-upload-text {
            font-size: 1.1em;
            color: #6b7280;
            margin-bottom: 10px;
        }
        
        .file-upload-subtext {
            font-size: 0.9em;
            color: #9ca3af;
        }
        
        .file-input {
            display: none;
        }
        
        .selected-files {
            margin-top: 15px;
            padding: 15px;
            background: #f0fdf4;
            border-radius: 8px;
            border: 1px solid #bbf7d0;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #dcfce7;
        }
        
        .file-item:last-child {
            border-bottom: none;
        }
        
        .file-icon {
            color: #16a34a;
            margin-right: 10px;
        }
        
        .scan-button {
            width: 100%;
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            border: none;
            padding: 18px 32px;
            border-radius: 12px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-top: 20px;
        }
        
        .scan-button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
        }
        
        .scan-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading-spinner {
            display: none;
            text-align: center;
            padding: 60px;
            color: #6b7280;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #e5e7eb;
            border-top: 4px solid #4f46e5;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .results-stats {
            display: flex;
            gap: 20px;
        }
        
        .stat-item {
            text-align: center;
            padding: 10px 15px;
            background: #f3f4f6;
            border-radius: 8px;
        }
        
        .stat-number {
            font-size: 1.5em;
            font-weight: 700;
            color: #4f46e5;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .candidate-card {
            background: white;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
            animation: slideIn 0.5s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }
        
        @keyframes slideIn {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .candidate-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
            border-color: #4f46e5;
        }
        
        .candidate-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .candidate-rank {
            background: linear-gradient(135deg, #f59e0b 0%, #f97316 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }
        
        .candidate-name {
            font-size: 1.3em;
            font-weight: 600;
            color: #1f2937;
            flex: 1;
            margin-left: 20px;
        }
        
        .match-score {
            text-align: right;
        }
        
        .score-number {
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }
        
        .score-label {
            font-size: 0.9em;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin: 15px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #10b981 0%, #059669 100%);
            border-radius: 4px;
            transition: width 1s ease-out;
        }
        
        .skills-section {
            margin-top: 25px;
        }
        
        .skills-title {
            font-weight: 600;
            color: #374151;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .skill-category {
            margin-bottom: 15px;
        }
        
        .category-name {
            font-size: 0.9em;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .skill-tag {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            color: #1e40af;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            border: 1px solid #bfdbfe;
            transition: all 0.3s ease;
        }
        
        .skill-tag:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
        }
        
        .contact-info {
            margin-top: 20px;
            padding: 15px;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 4px solid #4f46e5;
        }
        
        .contact-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
            color: #374151;
        }
        
        .contact-item:last-child {
            margin-bottom: 0;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #6b7280;
        }
        
        .empty-icon {
            font-size: 4em;
            margin-bottom: 20px;
            opacity: 0.5;
        }
        
        .empty-text {
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        
        .empty-subtext {
            opacity: 0.7;
        }
        
        @media (max-width: 1024px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .input-section {
                border-right: none;
                border-bottom: 1px solid #e5e7eb;
            }
            
            .header h1 {
                font-size: 2.5em;
            }
            
            .results-section {
                max-height: none;
            }
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .main-container {
                border-radius: 16px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .input-section, .results-section {
                padding: 20px;
            }
            
            .form-card {
                padding: 20px;
            }
            
            .candidate-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }
            
            .match-score {
                text-align: left;
            }
            
            .results-stats {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="header">
            <h1><i class="fas fa-robot"></i> AI Resume Scanner</h1>
            <p>Smart hiring solution powered by machine learning</p>
        </div>
        
        <div class="content-grid">
            <div class="input-section">
                <div class="section-title">
                    <i class="fas fa-clipboard-list"></i>
                    Input Requirements
                </div>
                
                <div class="form-card">
                    <div class="form-group">
                        <label class="form-label" for="jobDescription">
                            <i class="fas fa-briefcase"></i> Job Description
                        </label>
                        <textarea 
                            id="jobDescription" 
                            class="form-textarea" 
                            placeholder="Paste your detailed job description here. Include required skills, experience, and qualifications for better matching accuracy..."
                        ></textarea>
                    </div>
                </div>
                
                <div class="form-card">
                    <div class="form-group">
                        <label class="form-label">
                            <i class="fas fa-file-upload"></i> Resume Files
                        </label>
                        <div class="file-upload-area" onclick="document.getElementById('resumeFiles').click()">
                            <div class="file-upload-icon">
                                <i class="fas fa-cloud-upload-alt"></i>
                            </div>
                            <div class="file-upload-text">
                                Click to upload or drag and drop
                            </div>
                            <div class="file-upload-subtext">
                                Supports PDF and DOCX files (Max 10MB each)
                            </div>
                            <input 
                                type="file" 
                                id="resumeFiles" 
                                class="file-input" 
                                multiple 
                                accept=".pdf,.docx"
                                onchange="handleFileSelection(this)"
                            >
                        </div>
                        <div id="selectedFiles" class="selected-files" style="display: none;"></div>
                    </div>
                    
                    <button class="scan-button" onclick="scanResumes()" id="scanBtn">
                        <i class="fas fa-search"></i>
                        Analyze & Rank Candidates
                    </button>
                </div>
            </div>
            
            <div class="results-section">
                <div class="section-title">
                    <i class="fas fa-chart-bar"></i>
                    Analysis Results
                </div>
                
                <div id="emptyState" class="empty-state">
                    <div class="empty-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <div class="empty-text">Ready to analyze resumes</div>
                    <div class="empty-subtext">Upload resumes and job description to get started</div>
                </div>
                
                <div id="loadingState" class="loading-spinner" style="display: none;">
                    <div class="spinner"></div>
                    <div style="font-size: 1.1em; font-weight: 600;">Processing Resumes...</div>
                    <div style="margin-top: 10px; opacity: 0.7;">This may take a few moments</div>
                </div>
                
                <div id="resultsContainer" style="display: none;">
                    <div class="results-header">
                        <div class="section-title" style="margin-bottom: 0;">
                            <i class="fas fa-trophy"></i>
                            Candidate Rankings
                        </div>
                        <div class="results-stats">
                            <div class="stat-item">
                                <div class="stat-number" id="totalCandidates">0</div>
                                <div class="stat-label">Candidates</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-number" id="avgScore">0%</div>
                                <div class="stat-label">Avg Score</div>
                            </div>
                        </div>
                    </div>
                    <div id="candidateList"></div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let selectedFilesData = [];
        
        // Drag and drop functionality
        const fileUploadArea = document.querySelector('.file-upload-area');
        
        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });
        
        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.classList.remove('dragover');
        });
        
        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            handleFiles(files);
        });
        
        function handleFileSelection(input) {
            handleFiles(input.files);
        }
        
        function handleFiles(files) {
            selectedFilesData = Array.from(files);
            displaySelectedFiles();
        }
        
        function displaySelectedFiles() {
            const container = document.getElementById('selectedFiles');
            if (selectedFilesData.length === 0) {
                container.style.display = 'none';
                return;
            }
            
            container.style.display = 'block';
            container.innerHTML = `
                <div style="font-weight: 600; color: #059669; margin-bottom: 10px;">
                    <i class="fas fa-check-circle"></i> ${selectedFilesData.length} file(s) selected
                </div>
                ${selectedFilesData.map(file => `
                    <div class="file-item">
                        <i class="fas fa-file-pdf file-icon"></i>
                        <span>${file.name}</span>
                        <span style="margin-left: auto; color: #6b7280; font-size: 0.9em;">
                            ${(file.size / 1024 / 1024).toFixed(2)} MB
                        </span>
                    </div>
                `).join('')}
            `;
        }
        
        async function scanResumes() {
            const jobDescription = document.getElementById('jobDescription').value;
            const scanBtn = document.getElementById('scanBtn');
            
            if (!jobDescription.trim()) {
                showNotification('Please enter a job description', 'error');
                return;
            }
            
            if (selectedFilesData.length === 0) {
                showNotification('Please select at least one resume file', 'error');
                return;
            }
            
            // Show loading state
            document.getElementById('emptyState').style.display = 'none';
            document.getElementById('resultsContainer').style.display = 'none';
            document.getElementById('loadingState').style.display = 'block';
            
            scanBtn.disabled = true;
            scanBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            
            const formData = new FormData();
            formData.append('job_description', jobDescription);
            
            selectedFilesData.forEach(file => {
                formData.append('resumes', file);
            });
            
            try {
                const response = await fetch('/scan', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                displayResults(result);
            } catch (error) {
                showNotification('Error processing resumes: ' + error.message, 'error');
            } finally {
                document.getElementById('loadingState').style.display = 'none';
                scanBtn.disabled = false;
                scanBtn.innerHTML = '<i class="fas fa-search"></i> Analyze & Rank Candidates';
            }
        }
        
        function displayResults(data) {
            if (data.error) {
                showNotification('Error: ' + data.error, 'error');
                document.getElementById('emptyState').style.display = 'block';
                return;
            }
            
            document.getElementById('resultsContainer').style.display = 'block';
            
            // Update statistics
            const totalCandidates = data.ranked_candidates.length;
            const avgScore = totalCandidates > 0 ? 
                Math.round(data.ranked_candidates.reduce((sum, c) => sum + c.percentage_match, 0) / totalCandidates) : 0;
            
            document.getElementById('totalCandidates').textContent = totalCandidates;
            document.getElementById('avgScore').textContent = avgScore + '%';
            
            // Display candidates
            const candidateList = document.getElementById('candidateList');
            candidateList.innerHTML = '';
            
            data.ranked_candidates.forEach((candidate, index) => {
                const candidateCard = createCandidateCard(candidate, index + 1);
                candidateList.appendChild(candidateCard);
                
                // Animate entry with delay
                setTimeout(() => {
                    candidateCard.style.animationDelay = `${index * 0.1}s`;
                }, 100);
            });
        }
        
        function createCandidateCard(candidate, rank) {
            const card = document.createElement('div');
            card.className = 'candidate-card';
            
            // Determine rank styling
            let rankClass = 'candidate-rank';
            let rankIcon = 'fas fa-medal';
            if (rank === 1) {
                rankClass += ' rank-gold';
                rankIcon = 'fas fa-trophy';
            } else if (rank === 2) {
                rankClass += ' rank-silver';
            } else if (rank === 3) {
                rankClass += ' rank-bronze';
            }
            
            // Build skills HTML
            let skillsHtml = '';
            let hasSkills = false;
            
            Object.keys(candidate.skills).forEach(category => {
                if (candidate.skills[category].length > 0) {
                    hasSkills = true;
                    const categoryIcon = getCategoryIcon(category);
                    skillsHtml += `
                        <div class="skill-category">
                            <div class="category-name">
                                <i class="${categoryIcon}"></i> ${category.replace('_', ' ')}
                            </div>
                            <div class="skill-tags">
                                ${candidate.skills[category].map(skill => 
                                    `<span class="skill-tag">${skill}</span>`
                                ).join('')}
                            </div>
                        </div>
                    `;
                }
            });
            
            // Build contact info HTML
            let contactHtml = '';
            if (candidate.contact_info.emails.length > 0 || candidate.contact_info.phones.length > 0) {
                contactHtml = '<div class="contact-info">';
                if (candidate.contact_info.emails.length > 0) {
                    contactHtml += `
                        <div class="contact-item">
                            <i class="fas fa-envelope"></i>
                            <span>${candidate.contact_info.emails.join(', ')}</span>
                        </div>
                    `;
                }
                if (candidate.contact_info.phones.length > 0) {
                    contactHtml += `
                        <div class="contact-item">
                            <i class="fas fa-phone"></i>
                            <span>${candidate.contact_info.phones.join(', ')}</span>
                        </div>
                    `;
                }
                contactHtml += '</div>';
            }
            
            card.innerHTML = `
                <div class="candidate-header">
                    <div class="${rankClass}">
                        <i class="${rankIcon}"></i> #${rank}
                    </div>
                    <div class="candidate-name">
                        <i class="fas fa-user"></i> ${candidate.filename.replace(/\.(pdf|docx)$/i, '')}
                    </div>
                    <div class="match-score">
                        <div class="score-number">${candidate.percentage_match}%</div>
                        <div class="score-label">Match Score</div>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${candidate.percentage_match}%"></div>
                </div>
                
                ${hasSkills ? `
                    <div class="skills-section">
                        <div class="skills-title">
                            <i class="fas fa-cogs"></i> Extracted Skills
                        </div>
                        ${skillsHtml}
                    </div>
                ` : `
                    <div class="skills-section">
                        <div class="skills-title">
                            <i class="fas fa-exclamation-triangle"></i> No Specific Skills Detected
                        </div>
                        <p style="color: #6b7280; font-style: italic;">
                            Consider updating the resume with more specific skill keywords.
                        </p>
                    </div>
                `}
                
                ${contactHtml}
            `;
            
            return card;
        }
        
        function getCategoryIcon(category) {
            const icons = {
                'programming': 'fas fa-code',
                'frameworks': 'fas fa-layer-group',
                'databases': 'fas fa-database',
                'tools': 'fas fa-tools',
                'soft_skills': 'fas fa-users'
            };
            return icons[category] || 'fas fa-tag';
        }
        
        function showNotification(message, type = 'info') {
            // Create notification element
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
                max-width: 400px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            `;
            
            if (type === 'error') {
                notification.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
                notification.innerHTML = `<i class="fas fa-exclamation-circle"></i> ${message}`;
            } else if (type === 'success') {
                notification.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                notification.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
            } else {
                notification.style.background = 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)';
                notification.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
            }
            
            document.body.appendChild(notification);
            
            // Remove after 5 seconds
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 5000);
        }
        
        // Add animation styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
            
            .rank-gold {
                background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%) !important;
            }
            
            .rank-silver {
                background: linear-gradient(135deg, #e5e7eb 0%, #9ca3af 100%) !important;
                color: #374151 !important;
            }
            
            .rank-bronze {
                background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
            }
            
            .candidate-card:nth-child(1) {
                border-left: 4px solid #fbbf24;
            }
            
            .candidate-card:nth-child(2) {
                border-left: 4px solid #9ca3af;
            }
            
            .candidate-card:nth-child(3) {
                border-left: 4px solid #d97706;
            }
        `;
        document.head.appendChild(style);
        
        // Initialize tooltips and interactions
        document.addEventListener('DOMContentLoaded', function() {
            // Add keyboard shortcuts
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    scanResumes();
                }
            });
            
            // Add auto-save for job description
            const jobDescTextarea = document.getElementById('jobDescription');
            jobDescTextarea.addEventListener('input', function() {
                localStorage.setItem('jobDescription', this.value);
            });
            
            // Load saved job description
            const savedJobDesc = localStorage.getItem('jobDescription');
            if (savedJobDesc) {
                jobDescTextarea.value = savedJobDesc;
            }
        });
    </script>
</body>
</html>
"""
                

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan_resumes():
    try:
        job_description = request.form.get('job_description', '')
        if not job_description:
            return jsonify({'error': 'Job description is required'})
        
        files = request.files.getlist('resumes')
        if not files:
            return jsonify({'error': 'No resume files uploaded'})
        
        candidates = []
        
        for file in files:
            if file.filename == '':
                continue
                
            file_content = file.read()
            filename = file.filename
            
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                resume_text = scanner.extract_text_from_pdf(file_content)
            elif filename.lower().endswith('.docx'):
                resume_text = scanner.extract_text_from_docx(file_content)
            else:
                continue  # Skip unsupported file types
            
            if resume_text and not resume_text.startswith('Error'):
                # Extract skills and contact info
                skills = scanner.extract_skills(resume_text)
                contact_info = scanner.extract_contact_info(resume_text)
                
                candidate = {
                    'filename': filename,
                    'resume_text': resume_text,
                    'skills': skills,
                    'contact_info': contact_info
                }
                candidates.append(candidate)
        
        if not candidates:
            return jsonify({'error': 'No valid resumes could be processed'})
        
        # Rank candidates
        ranked_candidates = scanner.rank_candidates(candidates, job_description)
        
        # Remove resume_text from response to reduce size
        for candidate in ranked_candidates:
            del candidate['resume_text']
        
        return jsonify({
            'ranked_candidates': ranked_candidates,
            'total_candidates': len(ranked_candidates)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access"""
    try:
        data = request.json
        job_description = data.get('job_description', '')
        resume_text = data.get('resume_text', '')
        
        if not job_description or not resume_text:
            return jsonify({'error': 'Both job_description and resume_text are required'})
        
        # Analyze single resume
        skills = scanner.extract_skills(resume_text)
        contact_info = scanner.extract_contact_info(resume_text)
        similarity_score = scanner.calculate_similarity(resume_text, job_description)
        
        return jsonify({
            'similarity_score': similarity_score,
            'percentage_match': round(similarity_score * 100, 2),
            'skills': skills,
            'contact_info': contact_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("🚀 Starting AI-Powered Resume Scanner...")
    print("📊 Features:")
    print("   - PDF and DOCX resume parsing")
    print("   - TF-IDF and Cosine Similarity matching")
    print("   - Skill extraction and categorization")
    print("   - Contact information extraction")
    print("   - Candidate ranking and scoring")
    print("\n🌐 Access the web interface at: http://localhost:5000")
    print("🔗 API endpoint available at: http://localhost:5000/api/analyze")
    
    app.run(debug=True, host='0.0.0.0', port=5000)