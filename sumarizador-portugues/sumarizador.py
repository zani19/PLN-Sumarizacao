from transformers import MBartForConditionalGeneration, MBart50Tokenizer
import re
from unicodedata import normalize

# Configuração do modelo mBART para sumarização em português
model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer = MBart50Tokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)

def preprocessar_texto(texto):
    """Pré-processamento robusto para textos em português"""
    # Remove números de versículo e referências bíblicas
    texto = re.sub(r'^\d+|\b[A-Za-z]+\s\d+:\d+-\d+\b', '', texto)
    # Normalização de caracteres
    texto = normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    # Remove caracteres especiais indesejados
    return re.sub(r'[^\w\sáéíóúãõâêôçÁÉÍÓÚÃÕÂÊÔÇ.,;?!]', ' ', texto).strip()

def validar_texto(texto):
    """Validação com contagem precisa de tokens"""
    palavras = texto.split()
    num_palavras = len(palavras)
    
    if num_palavras < 100:
        return False, "Mínimo de 100 palavras necessárias"
    # Removido o limite máximo de palavras
    return True, texto

def dividir_em_chunks(texto, max_tokens=1024):
    """Divide o texto em chunks baseados em tokens"""
    tokens = tokenizer.tokenize(texto)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.convert_tokens_to_string(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks

def dividir_em_paragrafos(texto):
    return [p.strip() for p in texto.split('\n\n') if p.strip()]

def processar_texto(texto):
    """Processamento completo com tratamento de erros"""
    try:
        texto = preprocessar_texto(texto)
        valido, msg = validar_texto(texto)
        if not valido:
            return {'erro': msg}
        paragrafos = dividir_em_paragrafos(texto)
        resumos = []
        lang_code = "pt_XX"
        if lang_code not in tokenizer.lang_code_to_id:
            return {'erro': f"Idioma '{lang_code}' não disponível no tokenizer. Idiomas disponíveis: {list(tokenizer.lang_code_to_id.keys())}"}
        for paragrafo in paragrafos:
            tokenizer.src_lang = lang_code
            inputs = tokenizer(paragrafo, return_tensors="pt", max_length=512, truncation=True)
            summary_ids = model.generate(
                inputs["input_ids"],
                num_beams=8,
                min_length=30,
                max_length=60,
                length_penalty=1.2,
                early_stopping=True,
                forced_bos_token_id=tokenizer.lang_code_to_id[lang_code]
            )
            resumo = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            resumos.append(resumo)
        # Resumir o resumo final
        texto_resumido = ' '.join(resumos)
        inputs = tokenizer(texto_resumido, return_tensors="pt", max_length=512, truncation=True)
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=8,
            min_length=30,
            max_length=60,
            length_penalty=1.2,
            early_stopping=True,
            forced_bos_token_id=tokenizer.lang_code_to_id[lang_code]
        )
        resumo_final = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {
            'texto_original': texto,
            'resumo': resumo_final,
            'palavras_original': len(texto.split()),
            'palavras_resumo': len(resumo_final.split())
        }
    except Exception as e:
        return {'erro': f"Erro ao processar o texto: {str(e)}"}