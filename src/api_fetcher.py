import requests

def fetch_variant_from_api(chrom, pos, ref, alt):
    """Fetches live clinical data from MyVariant.info API using HGVS coordinates."""
    # 1. Clean inputs to strip any invisible spaces or newlines from the VCF
    chrom = str(chrom).strip()
    pos = str(pos).strip()
    ref = str(ref).strip()
    alt = str(alt).strip()
    
    if not chrom.startswith('chr'):
        chrom = f"chr{chrom}"
        
    # Construct exact HGVS ID
    hgvs_id = f"{chrom}:g.{pos}{ref}>{alt}"
    
    # 2. Use the direct /variant/ endpoint instead of the fuzzy /query/ endpoint
    url = f"https://myvariant.info/v1/variant/{hgvs_id}?fields=clinvar,dbsnp"
    
    try:
        response = requests.get(url, timeout=10)
        
        # 3. Handle the direct object response
        if response.status_code == 200:
            data = response.json()
            
            if data and not data.get("error"):
                clinvar = data.get("clinvar", {})
                
                # Extract Gene
                gene = "Unknown Gene"
                if "gene" in clinvar:
                    gene = clinvar["gene"].get("symbol", "Unknown Gene")
                elif "dbsnp" in data and "gene" in data["dbsnp"]:
                    gene = data["dbsnp"]["gene"].get("symbol", "Unknown Gene")
                    
                # Extract Classification
                classification = "Uncertain significance"
                if "rcv" in clinvar:
                    rcv = clinvar["rcv"]
                    if isinstance(rcv, list) and len(rcv) > 0:
                        classification = rcv[0].get("clinical_significance", classification)
                    elif isinstance(rcv, dict):
                        classification = rcv.get("clinical_significance", classification)
                        
                # Format Evidence
                evidence = (
                    f"Live Database Query for {hgvs_id}:\n"
                    f"- Sourced dynamically from MyVariant/ClinVar.\n"
                    f"- Documented clinical significance: {classification}.\n"
                    f"- Gene locus: {gene}."
                )
                
                return {
                    "metadata": {"gene": gene, "classification": str(classification).title()},
                    "evidence": evidence
                }
    except Exception as e:
        print(f"API Fetch Error: {e}")
        
    return None
