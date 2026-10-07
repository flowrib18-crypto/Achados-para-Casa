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
# 2. CATÁLOGO REAL DE PRODUTOS DE CASA, COZINHA E ORGANIZAÇÃO (COM IMAGENS CORRIGIDAS)
# ==============================================================================
PRODUTOS = [
    {
        "nome": "Kit Panos Multiuso Microfibra Gigante 60x80 Limpa Tudo Super Absorvente",
        "link": "https://vt.tiktok.com/ZS9DVa3EApja1-nfVbk/",
        "imagem_url": "https://images.unsplash.com/photo-1563453392212-326f5e854473?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Mini Ar Condicionado Climatizador Umidificador Ventilador Água Com LED Portátil",
        "link": "https://vt.tiktok.com/ZS9DVaKJ1umxE-UHx9W/",
        "imagem_url": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Escorredor de Louças Pratos 13 Pratos 2 Andares com Porta Talher Modelo Premium",
        "link": "https://vt.tiktok.com/ZS9DVaKwB15qr-TEaTI/",
        "imagem_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Câmera Lâmpada Wi-Fi IP Inteligente 8177QJ Branca Segurança 1080p Full HD Pix-Link",
        "link": "https://vt.tiktok.com/ZS9DVmeakMLJH-8DAf9/",
        "imagem_url": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Escova de Limpeza Elétrica Ajustável para Janela, Banheiro e Cozinha 9 em 1 Recarregável",
        "link": "https://vt.tiktok.com/ZS9DVmJW3UMxg-1X2J5/",
        "imagem_url": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Jogo Toalha de Banho Super Luxo 4Pçs 100% Algodão Alta Absorção",
        "link": "https://vt.tiktok.com/ZS9DVme6ftpPw-mv1pz/",
        "imagem_url": "https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Kit até 30 Marmitas Potes 800ml com Travas Laterais Colorido BPA FREE",
        "link": "https://vt.tiktok.com/ZS9DVmNxuKAVr-oyWt7/",
        "imagem_url": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Mop Giratório 14 Litros Esfregão 360 Balde Inox com Cabo Ajustável",
        "link": "https://vt.tiktok.com/ZS9DVmFYNCQMH-LghoN/",
        "imagem_url": "https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Varal de Chão 3 Andares Dobrável com Abas para Roupas",
        "link": "https://vt.tiktok.com/ZS9DVm2Jj9628-F23ko/",
        "imagem_url": "https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Travesseiro Cervical Ortopédico Confortável Alivia Dores na Coluna",
        "link": "https://vt.tiktok.com/ZS9DVmjhnuqCH-wfiUR/",
        "imagem_url": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Cortador de Legumes 16 em 1 Multifuncional com 8 Lâminas Ajustáveis",
        "link": "https://vt.tiktok.com/ZS9DVmMhpQGtP-U7HVG/",
        "imagem_url": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Escova de Limpeza Elétrica Ajustável 9 em 1 Recarregável (Versão 2)",
        "link": "https://vt.tiktok.com/ZS9DVmMjTUVNU-vGBkP/",
        "imagem_url": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Protetor de Colchão Casal com Manta Impermeável Ultrassônico e Elástico",
        "link": "https://vt.tiktok.com/ZS9DVmBAFxN8R-K7mOX/",
        "imagem_url": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Percarbonato de Sódio 100% Puro Ativo Auto Flocante Tira Manchas Roupas Brancas",
        "link": "https://vt.tiktok.com/ZS9DVmBWeeENt-CC5PO/",
        "imagem_url": "https://images.unsplash.com/photo-1585670149079-5c74eff05b4b?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Kit 5 Lençóis QUEEN Estampados Avulsos com Elástico",
        "link": "https://vt.tiktok.com/ZS9DVmSaMgcv9-PZJbS/",
        "imagem_url": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?auto=format&fit=crop&w=800&q=80"
    },
    {
        "nome": "Coberdrom Casal Queen Size Sherpa Cobertor Edredom de Inverno Pele de Carneiro",
        "link": "https://vt.tiktok.com/ZS9DVmPhvUArW-DxBkv/",
        "imagem_url": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=800&q=80"
    }
]

# ==============================================================================
# 2.1 LÓGICA DE ROTAÇÃO DIÁRIA
# ==============================================================================
agora = datetime.now()
dia_do_ano = agora.timetuple().tm_yday
hora_servidor = agora.hour

turno = 0 if hora_servidor < 15 else 1
indice_produto = ((dia_do_ano * 2) + turno) % len(PRODUTOS)
produto_do_dia = PRODUTOS[indice_produto]

PRODUTO_NOME = produto_do_dia["nome"]
TIKTOK_SHOP_LINK = produto_do_dia["link"]
URL_IMAGEM_ILUSTRATIVA = produto_do_dia["imagem_url"]

print(f">>> Produto do dia: {PRODUTO_NOME}", flush=True)
print(f">>> Link Afiliado: {TIKTOK_SHOP_LINK}", flush=True)

# ==============================================================================
# 3. PROMPT DE GERAÇÃO
# ==============================================================================
prompt = f"""
Crie um artigo completo de review para blog de achados de casa, cozinha e organização em formato HTML avaliando o produto '{PRODUTO_NOME}'.

Instruções obrigatórias de estrutura HTML:
1. Título principal chamativo em <h1> focado em praticidade para o lar, otimização de espaço e facilidade no dia a dia.
2. Logo após o <h1>, insira obrigatoriamente a seguinte tag de imagem HTML com estilo centralizado e limpo:
   <div style="text-align: center; margin: 20px 0;">
     <img src="{URL_IMAGEM_ILUSTRATIVA}" alt="{PRODUTO_NOME}" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.15);" />
     <p style="font-size: 12px; color: #777777; margin-top: 6px; font-style: italic;">* Imagem meramente ilustrativa. Confira a foto e detalhes exatos do produto na página oficial do vendedor.</p>
   </div>
3. Introdução envolvente sobre como transformar a rotina doméstica e manter a casa organizada sem esforço.
4. Seção 'Principais Benefícios e Praticidade no Dia a Dia' em lista <ul> com itens <li>.
5. Seção 'Por Que Este Achadinho Está a Fazer Sucesso'.
6. No final do artigo, insira o botão CTA HTML com o link de afiliado oficial:
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
