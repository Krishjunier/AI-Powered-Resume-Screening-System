# AI Resume Scanner 🤖

A powerful AI-driven resume screening and candidate ranking system that helps HR professionals and recruiters efficiently evaluate candidates by automatically analyzing resumes against job descriptions.

![AI Resume Scanner](https://img.shields.io/badge/AI-Resume%20Scanner-blue)
![Python](https://img.shields.io/badge/Python-3.7+-green)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-red)
![Machine Learning](https://img.shields.io/badge/ML-TF--IDF%20%7C%20Cosine%20Similarity-orange)

## ✨ Features

### 🎯 Core Functionality
- **Smart Resume Parsing**: Automatically extracts text from PDF and DOCX files
- **AI-Powered Matching**: Uses TF-IDF vectorization and cosine similarity for accurate job-resume matching
- **Candidate Ranking**: Ranks candidates based on relevance to job requirements
- **Skill Extraction**: Automatically identifies and categorizes technical and soft skills
- **Contact Information**: Extracts emails and phone numbers from resumes

### 🔧 Technical Skills Detection
- **Programming Languages**: Python, Java, JavaScript, C++, C#, PHP, Ruby, Go, Swift, Kotlin, etc.
- **Frameworks**: React, Angular, Vue, Django, Flask, Spring, Node.js, Express, Laravel, etc.
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, Oracle, etc.
- **Tools & Platforms**: Git, Docker, Kubernetes, Jenkins, AWS, Azure, GCP, Linux, etc.
- **Soft Skills**: Leadership, Communication, Teamwork, Problem Solving, etc.

### 🎨 User Interface
- **Modern Web Interface**: Beautiful, responsive design with drag-and-drop file upload
- **Real-time Analysis**: Live progress tracking and instant results
- **Visual Scoring**: Progress bars and match percentages for easy evaluation
- **Mobile Responsive**: Works seamlessly on desktop, tablet, and mobile devices

### 📊 Analytics & Insights
- **Match Scoring**: Percentage-based compatibility scores
- **Skill Visualization**: Categorized skill tags for quick assessment
- **Candidate Statistics**: Summary metrics and ranking insights
- **Export Ready**: Easy-to-share results format

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.7+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-resume-scanner.git
cd ai-resume-scanner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

4. **Access the application**
- Web Interface: http://localhost:5000
- API Endpoint: http://localhost:5000/api/analyze

## 📦 Dependencies

```txt
Flask==2.3.3
scikit-learn==1.3.0
numpy==1.24.3
PyPDF2==3.0.1
python-docx==0.8.11
```

## 🔧 Installation Guide

### Method 1: Using pip

```bash
# Install required packages
pip install flask scikit-learn numpy PyPDF2 python-docx

# Run the application
python main.py
```

### Method 2: Using requirements.txt

Create a `requirements.txt` file:
```txt
Flask==2.3.3
scikit-learn==1.3.0
numpy==1.24.3
PyPDF2==3.0.1
python-docx==0.8.11
```

Then install:
```bash
pip install -r requirements.txt
python main.py
```

### Method 3: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv resume_scanner_env

# Activate virtual environment
# On Windows:
resume_scanner_env\Scripts\activate
# On macOS/Linux:
source resume_scanner_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 💻 Usage

### Web Interface

1. **Upload Job Description**
   - Paste your detailed job description in the text area
   - Include required skills, experience, and qualifications for better matching

2. **Upload Resume Files**
   - Drag and drop PDF or DOCX files
   - Or click to browse and select files
   - Supports multiple file uploads

3. **Analyze & Rank**
   - Click "Analyze & Rank Candidates" button
   - Wait for processing (usually takes a few seconds)
   - View ranked results with match scores

### API Usage

#### Analyze Single Resume

```python
import requests

url = "http://localhost:5000/api/analyze"
data = {
    "job_description": "We are looking for a Python developer with Django experience...",
    "resume_text": "Experienced software developer with 5 years of Python and Django..."
}

response = requests.post(url, json=data)
result = response.json()

print(f"Match Score: {result['percentage_match']}%")
print(f"Skills Found: {result['skills']}")
```

#### Response Format

```json
{
    "similarity_score": 0.75,
    "percentage_match": 75.0,
    "skills": {
        "programming": ["python", "java"],
        "frameworks": ["django", "flask"],
        "databases": ["mysql", "postgresql"],
        "tools": ["git", "docker"],
        "soft_skills": ["leadership", "teamwork"]
    },
    "contact_info": {
        "emails": ["john.doe@email.com"],
        "phones": ["123-456-7890"]
    }
}
```

## 🏗️ Architecture

### Core Components

1. **ResumeScanner Class**
   - Text extraction from PDF/DOCX files
   - Text preprocessing and cleaning
   - Skill extraction using keyword matching
   - Contact information extraction using regex
   - TF-IDF vectorization and similarity calculation

2. **Flask Web Application**
   - RESTful API endpoints
   - File upload handling
   - Modern responsive web interface
   - Real-time processing feedback

3. **Machine Learning Pipeline**
   - TF-IDF Vectorization for text analysis
   - Cosine Similarity for matching scores
   - Skill categorization and extraction
   - Candidate ranking algorithms

### File Structure

```
ai-resume-scanner/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/                # Static files (if any)
├── templates/             # HTML templates (if separated)
└── uploads/               # Temporary file storage
```

## 🎯 How It Works

### 1. Text Extraction
- **PDF Processing**: Uses PyPDF2 to extract text from PDF files
- **DOCX Processing**: Uses python-docx to extract text from Word documents
- **Text Cleaning**: Removes special characters, normalizes whitespace

### 2. Skill Identification
- **Keyword Matching**: Searches for predefined skill keywords in resume text
- **Categorization**: Groups skills into categories (programming, frameworks, databases, tools, soft skills)
- **Case Insensitive**: Handles various formatting and capitalization

### 3. Similarity Scoring
- **TF-IDF Vectorization**: Converts text documents into numerical vectors
- **Cosine Similarity**: Calculates similarity between job description and resume vectors
- **Percentage Scoring**: Converts similarity scores to intuitive percentages

### 4. Candidate Ranking
- **Score-Based Sorting**: Ranks candidates by similarity scores
- **Tie Breaking**: Handles equal scores appropriately
- **Performance Metrics**: Provides statistics and insights

## 🛠️ Customization

### Adding New Skills

Edit the `skill_keywords` dictionary in the `ResumeScanner` class:

```python
self.skill_keywords = {
    'programming': ['python', 'java', 'your_new_language'],
    'frameworks': ['react', 'angular', 'your_new_framework'],
    # Add more categories as needed
    'your_category': ['skill1', 'skill2', 'skill3']
}
```

### Modifying TF-IDF Parameters

Adjust the TfidfVectorizer settings:

```python
self.vectorizer = TfidfVectorizer(
    stop_words='english',
    lowercase=True,
    max_features=2000,      # Increase for more features
    ngram_range=(1, 3),     # Include trigrams
    min_df=2,               # Minimum document frequency
    max_df=0.95             # Maximum document frequency
)
```

### Customizing UI Theme

The application uses a modern gradient theme. You can customize colors by modifying the CSS variables in the HTML template:

```css
:root {
    --primary-color: #4f46e5;
    --secondary-color: #7c3aed;
    --accent-color: #10b981;
    --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## 📊 Performance Considerations

### Optimization Tips

1. **File Size Limits**: Implement file size restrictions for better performance
2. **Batch Processing**: Process multiple resumes in parallel for large datasets
3. **Caching**: Cache TF-IDF vectors for frequently used job descriptions
4. **Memory Management**: Clear temporary files and variables after processing

### Scalability

For production use, consider:
- **Database Integration**: Store results in a database for persistence
- **Queue System**: Use Celery or similar for background processing
- **Load Balancing**: Deploy multiple instances for high traffic
- **Cloud Storage**: Use AWS S3 or similar for file storage

## 🔐 Security Considerations

- **File Validation**: Validate uploaded files to prevent malicious uploads
- **Input Sanitization**: Sanitize all user inputs to prevent XSS attacks
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Authentication**: Add user authentication for production use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-resume-scanner.git

# Create virtual environment
python -m venv dev_env
source dev_env/bin/activate  # On Windows: dev_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **scikit-learn** for machine learning capabilities
- **Flask** for the web framework
- **PyPDF2** for PDF processing
- **python-docx** for Word document processing
- **Font Awesome** for icons
- **Modern CSS** for responsive design

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/ai-resume-scanner/issues) page
2. Create a new issue with detailed information
3. Provide sample files (anonymized) if possible
4. Include error messages and system information

## 🚧 Roadmap

### Upcoming Features

- [ ] **Advanced NLP**: Integration with spaCy or NLTK for better text analysis
- [ ] **Machine Learning Models**: Train custom models for better accuracy
- [ ] **Bulk Processing**: Handle hundreds of resumes simultaneously
- [ ] **Export Options**: PDF reports, Excel exports
- [ ] **Integration APIs**: Connect with ATS systems
- [ ] **Advanced Filtering**: Filter by experience, education, location
- [ ] **Duplicate Detection**: Identify and handle duplicate resumes
- [ ] **Analytics Dashboard**: Comprehensive hiring analytics

### Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Enhanced UI and mobile responsiveness
- **v1.2.0**: API improvements and better error handling

---

Made with ❤️ for HR professionals and recruiters worldwide.

**Star ⭐ this repository if you find it helpful!**
