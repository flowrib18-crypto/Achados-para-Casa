import os
import time
import random
import smtplib
import urllib.parse
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai

# ==============================================================================
# 1. CONFIGURAÇÃO DE SEGREDOS
# ==============================================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "").replace(" ", "")
BLOGGER_EMAIL = os.environ.get("BLOGGER_EMAIL")

if not GEMINI_API_KEY:
    raise ValueError("ERRO: GEMINI_API_KEY não foi encontrada nas variáveis de ambiente.")

print(">>> Configurando API do Gemini...", flush=True)
genai.configure(api_key=GEMINI_API_KEY)

# ==============================================================================
# 2. CATÁLOGO DE PRODUTOS DE CASA, COZINHA E ORGANIZAÇÃO
# ==============================================================================
PRODUTOS = [
    {
        "nome": "Mini Processador Elétrico Moedor de Alimentos USB",
        "link": "https://vt.tiktok.com/exemplomultiuso1/",
        "kw_imagem": "mini food processor kitchen"
    },
    {
        "nome": "Mop Spray com Reservatório e Pano de Microfibra",
        "link": "https://vt.tiktok.com/exemplomultiuso2/",
        "kw_imagem": "spray mop floor cleaning"
    },
    {
        "nome": "Organizador de Geladeira acrílico transparente multiuso",
        "link": "https://vt.tiktok.com/exemplomultiuso3/",
        "kw_imagem": "fridge organizer clear bins"
    },
    {
        "nome": "Escorredor de Pratos Rolante de Inox para Pia",
        "link": "https://vt.tiktok.com/exemplomultiuso4/",
        "kw_imagem": "roll up dish drying rack"
    },
    {
        "nome": "Mini Seladora de Embalagens a Vácuo portátil",
        "link": "https://vt.tiktok.com/exemplomultiuso5/",
        "kw_imagem": "mini bag sealer plastic"
    },
    {
        "nome": "Descascador e Fatiador de Legumes Giratório 3 em 1",
        "link": "https://vt.tiktok.com/exemplomultiuso6/",
        "kw_imagem": "vegetable peeler slicer"
    },
    {
        "nome": "Suporte Adesivo Multiuso para Vassouras e Rodos de Parede",
        "link": "https://vt.tiktok.com/exemplomultiuso7/",
        "kw_imagem": "mop broom wall holder"
    },
    {
        "nome": "Fita Dupla Face Nano Gel Transparente Lavável Fixação Forte",
        "link": "https://vt.tiktok.com/exemplomultiuso8/",
        "kw_imagem": "nano tape double sided"
    },
    {
        "nome": "Varal de Chão Dobrável com Abas em Aço",
        "link": "https://vt.tiktok.com/exemplomultiuso9/",
        "kw_imagem": "folding clothes drying rack"
    },
    {
        "nome": "Dispenser para Detergente com Suporte de Esponja 2 em 1",
        "link": "https://vt.tiktok.com/exemplomultiuso10/",
        "kw_imagem": "soap dispenser sponge holder"
    },
    {
        "nome": "Tapete Antiderrapante para Pia e Banheiro em PVC",
        "link": "https://vt.tiktok.com/exemplomultiuso11/",
        "kw_imagem": "non slip bath mat"
    },
    {
        "nome": "Lixeira de Pia com Tampa Basculante Compacta",
        "link": "https://vt.tiktok.com/exemplomultiuso12/",
        "kw_imagem": "small kitchen trash can"
    },
    {
        "nome": "Organizador de Armário Suspenso para Prateleira",
        "link": "https://vt.tiktok.com/exemplomultiuso13/",
        "kw_imagem": "hanging cabinet organizer"
    },
    {
        "nome": "Garrafa Squeeze Motivacional com Marcador de Tempo 2L",
        "link": "https://vt.tiktok.com/exemplomultiuso14/",
        "kw_imagem": "motivation water bottle"
    },
    {
        "nome": "Escova de Limpeza Elétrica Sem Fio com Cabeças Trocáveis",
        "link": "https://vt.tiktok.com/exemplomultiuso15/",
        "kw_imagem": "electric cleaning brush scrub"
    }
]

# ==============================================================================
# 2.1 LÓGICA DE ROTAÇÃO DIÁRIA
# ==============================================================================
agora = datetime.now()
dia_do_ano = agora.timetuple().tm_yday
hora_servidor = agora.hour

turno = 0 if hora_servidor < 15 else 1
indice_produto = ((dia_do_ano * 2) + turno) % len(PRODUTO if 'PRODUTO' in locals() else PRODUTOS)
produto_do_dia = PRODUTOS[indice_produto]

PRODUTO_NOME = produto_do_dia["nome"]
TIKTOK_SHOP_LINK = produto_do_dia["link"]
KW_IMAGEM = urllib.parse.quote(produto_do_dia.get("kw_imagem", "home organization kitchen"))

URL_IMAGEM_ILUSTRATIVA = f"https://loremflickr.com/800/500/{KW_IMAGEM}"

print(f">>> Produto do dia: {PRODUTO_NOME}", flush=True)
print(f">>> Link Afiliado: {TIKTOK_SHOP_LINK}", flush=True)

# ==============================================================================
# 3. PROMPT DE GERAÇÃO
# ==============================================================================
prompt = f"""
Crie um artigo completo de review para blog de achados de casa, cozinha e organização em formato HTML avaliando o produto '{PRODUTO_NOME}'.

Instruções obrigatórias de estrutura HTML:
1. Título principal chamativo em <h1> focado em praticidade para o lar, otimização de espaço e facilidade no dia a dia.
2. Logo após o <h1>, insira a seguinte imagem:
   <div style="text-align: center; margin: 20px 0;">
     <img src="{URL_IMAGEM_ILUSTRATIVA}" alt="{PRODUTO_NOME}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" />
     <p style="font-size: 12px; color: #777777; margin-top: 6px; font-style: italic;">* Imagem meramente ilustrativa. Confira a foto e detalhes exatos do produto na página oficial do vendedor.</p>
   </div>
3. Introdução envolvente sobre como transformar a rotina doméstica e manter a casa organizada sem esforço.
4. Seção 'Principais Benefícios e Praticidade no Dia a Dia' em lista <ul> com itens <li>.
5. Seção 'Por Que Este Achadinho Está a Fazer Sucesso'.
6. No final do artigo, insira o botão CTA HTML:
   <div style="text-align: center; margin: 35px 0;">
     <a href="{TIKTOK_SHOP_LINK}" target="_blank" rel="sponsored nofollow" style="background-color: #ff0050; color: white; padding: 16px 32px; font-size: 18px; font-weight: bold; text-decoration: none; border-radius: 8px; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
       👉 VER OFERTA E COMPRAR NO TIKTOK SHOP
     </a>
   </div>

Responda APENAS com o código HTML puro pronto para publicação, sem marcadores de código markdown (```html).
"""

# ==============================================================================
# 3.1 GERADOR DE CONTEÚDO IA (FALLBACK MULTI-MODELO)
# ==============================================================================
modelos_disponiveis = [
    'gemini-3.8-flash',
    'gemini-3.7-flash',
    'gemini-3.6-flash',
    'gemini-3.5-flash',
    'gemini-2.5-flash'
]

response = None

for nome_modelo in modelos_disponiveis:
    try:
        print(f">>> Tentando gerar artigo com o modelo: {nome_modelo}...", flush=True)
        model = genai.GenerativeModel(nome_modelo)
        response = model.generate_content(prompt)
        print(f">>> Sucesso com o modelo: {nome_modelo}!", flush=True)
        break
    except Exception as e:
        print(f">>> Modelo {nome_modelo} falhou ({e}). Tentando o próximo modelo...", flush=True)
        time.sleep(5)

if not response:
    raise RuntimeError("ERRO: Todos os modelos do Gemini falharam ou atingiram a cota diária.")

conteudo_html = response.text.replace("```html", "").replace("```", "").strip()

# ==============================================================================
# 4. DISPARO DE E-MAIL PARA PUBLICAR NO BLOGGER
# ==============================================================================
msg = MIMEMultipart()
msg['From'] = GMAIL_USER
msg['To'] = BLOGGER_EMAIL
msg['Subject'] = f"Achados para Casa: {PRODUTO_NOME}"

msg.attach(MIMEText(conteudo_html, 'html'))

print(f">>> Enviando e-mail de publicação para {BLOGGER_EMAIL}...", flush=True)
try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, BLOGGER_EMAIL, msg.as_string())
    server.close()
    print(f">>> SUCESSO! Post de Casa '{PRODUTO_NOME}' enviado para publicação!", flush=True)
except Exception as e:
    print(f">>> ERRO ao enviar e-mail: {e}", flush=True)
    raise e
