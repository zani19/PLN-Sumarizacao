from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
from unicodedata import normalize

# Modelo multilíngue treinado para sumarização em vários idiomas
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def preprocessar_texto(texto):
    texto = normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto = re.sub(r'[^\w\s.,;?!]', ' ', texto).strip()
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def validar_texto(texto):
    palavras = texto.split()
    if len(palavras) < 100:
        return False, "Mínimo de 100 palavras necessárias"
    return True, texto

def processar_texto(texto):
    texto = preprocessar_texto(texto)
    valido, resultado = validar_texto(texto)
    if not valido:
        return {'erro': resultado}

    entrada = "summarize: " + texto
    inputs = tokenizer(entrada, return_tensors="pt", max_length=1024, truncation=True)

    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=80,
        max_length=200,
        early_stopping=True
    )

    resumo = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return {
        'texto_original': texto,
        'resumo': resumo,
        'palavras_original': len(texto.split()),
        'palavras_resumo': len(resumo.split())
    }
