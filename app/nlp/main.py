import spacy

nlp = spacy.load("en_core_web_sm")

def get_ner_tags(text:str) -> list[dict]:
    doc = nlp(text)
    return [{
        "name": ent.text,
        "label": ent.label_,
        "start_char": ent.start_char,
        "end_char": ent.end_char,
        "kb_id": ent.kb_id_,   # linked knowledge base id (if available)
        "lemma": ent.lemma_ if hasattr(ent, "lemma_") else None
    } for ent in doc.ents]