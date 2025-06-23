# PLN-Sumarizacao

Repositório destinado à atividade de PLN - Sumarização de textos em português.

## Integrantes do grupo

- Thiago Zani - [GitHub](https://github.com/zani19)
- Gabriel Briscese - [GitHub](https://github.com/Briscese)
- Jean Faria - [GitHub](https://github.com/jeejdev)

## Como rodar o projeto (Windows)

### 1. Clone o repositório

```powershell
git clone https://github.com/zani19/PLN-Sumarizacao.git
cd PLN-Sumarizacao\sumarizador-portugues
```

### 2. Crie e ative o ambiente virtual (venv)

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 4. Rode o servidor Flask

```powershell
python app.py
```

O servidor estará disponível em [http://localhost:5000](http://localhost:5000).

---

## Observações importantes

- O modelo de sumarização utilizado é o mBART-50, que é multilíngue, mas pode apresentar limitações para textos narrativos em português.
- Caso o resumo não fique satisfatório, sugerimos complementar manualmente ou explicar as limitações no relatório.
- Para dúvidas ou sugestões, consulte os integrantes do grupo.
