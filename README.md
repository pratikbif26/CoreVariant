# ⚡ CoreVariant: AI Clinical Interpretation Engine

CoreVariant is a containerized Bioinformatics application that bridges raw genomic data (VCF) with live global databases and Large Language Models (LLMs) to synthesize automated, ACMG-style clinical interpretation dossiers. 

Built to accelerate genomic triage, CoreVariant dynamically fetches live consensus data and utilizes **Llama 3.1** via Retrieval-Augmented Generation (RAG) to generate structured clinical insights, complete with professional PDF export functionality.

## 🧬 Architecture & Tech Stack
- **Frontend & UI:** Streamlit (Custom Venice-AI Dark Theme)
- **Data Parsing:** Pandas, custom VCF parsing logic
- **Live Database Integration:** MyVariant.info REST API (fetching live ClinVar & dbSNP consensus)
- **AI / LLM Engine:** Groq API (Llama-3.1-8b-instant) for RAG clinical synthesis
- **Report Generation:** `fpdf2` for automated PDF dossier rendering
- **DevOps:** Dockerized with a **Python 3.12** base image for strict dependency management and absolute reproducibility.

## 🚀 Key Features
- **Stateless Architecture:** Protects PHI by operating entirely in-memory with zero persistent database storage.
- **Dynamic API Fetching:** Eliminates the need for massive local databases by pinging MyVariant.info in real-time using HGVS coordinates.
- **Deep Clinical Profiling:** The LLM engine is rigorously prompted to extract ACMG evidence codes (PVS1, PS1, etc.), molecular mechanisms, and actionable therapeutic insights.
- **Batch Processing Pipeline:** Automatically loops through entire VCF files to triage and summarize variant pathogenicity, exporting results to CSV.
- **PDF Dossier Export:** Generates highly formatted, executive-ready PDF reports for individual variants.

## 🛠️ Local Installation & Usage (Docker)
The easiest way to run CoreVariant is via Docker, ensuring zero dependency conflicts.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/pratikbif26/CoreVariant.git](https://github.com/pratikbif26/CoreVariant.git)
   cd CoreVariant
