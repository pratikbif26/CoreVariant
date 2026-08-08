from groq import Groq

def generate_acmg_report(variant_id, retrieved_data, api_key):
    """Synthesizes deep genomic context into an exhaustive ACMG dossier using Llama 3.1."""
    if not api_key:
        return "⚠️ Error: Groq API key is missing. Please authenticate in the sidebar."
        
    try:
        client = Groq(api_key=api_key)
        
        system_prompt = (
            "You are a Senior Board-Certified Clinical Genomicist leading the CoreVariant AI engine. "
            "Draft an exhaustive, high-rigor ACMG Clinical Interpretation Report for the target variant. "
            "You MUST synthesize molecular mechanisms, protein structural impact, clinical significance, "
            "ACMG/AMP evidence criteria tags (e.g., PVS1, PS1, PM2, PP3), and actionable therapeutic insights. "
            "Maintain an authoritative, concise medical genetics tone."
        )
        
        user_prompt = (
            f"### TARGET VARIANT METADATA\n"
            f"- Variant HGVS ID: {variant_id}\n"
            f"- Locus / Gene: {retrieved_data['metadata']['gene']}\n"
            f"- Database Consensus Class: {retrieved_data['metadata']['classification']}\n"
            f"- Live Retrieved Evidence:\n{retrieved_data['evidence']}\n\n"
            f"### REQUIRED STRUCTURE\n"
            f"Format your response in crisp Markdown using these exact headers:\n\n"
            f"## 1. Executive Summary & ACMG Criteria\n"
            f"- State formal classification (Pathogenic / Likely Pathogenic / VUS / Benign).\n"
            f"- List applicable ACMG evidence codes (e.g., **PVS1**, **PS1**, **PM2**, **PP3**) with short justifications.\n\n"
            f"## 2. Molecular Mechanism & Structural Impact\n"
            f"- Detail domain disruption, catalytic site alterations, frameshifts, or conformational shifts.\n\n"
            f"## 3. Clinical Phenotype & Disease Spectrum\n"
            f"- Outline associated syndromes, inheritance pattern, penetrance, and disease spectrum.\n\n"
            f"## 4. Therapeutic & Actionable Insights\n"
            f"- Identify targeted therapies, clinical trial indications, FDA-approved drugs, or management protocols.\n\n"
            f"## 5. Database Evidence & Literature Summary\n"
            f"- Synthesize ClinVar, dbSNP, and genomic literature citations."
        )
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.1
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error communicating with CoreVariant LLM API: {str(e)}"
