import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import sys
import google.generativeai as genai

# Configurações de Email (Brevo SMTP)
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("BLOG_EMAIL_USER")       # Login SMTP técnico do Brevo
SMTP_PASS = os.environ.get("BLOG_EMAIL_PASS")       # Chave SMTP do Brevo
BLOGGER_EMAIL = os.environ.get("BLOGGER_PUBLISH_EMAIL")
VERIFIED_SENDER = "comercebem@gmail.com"            # Email verificado no Brevo
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Validação prévia dos segredos do GitHub
if not SMTP_USER or not SMTP_PASS or not BLOGGER_EMAIL or not GEMINI_API_KEY:
    print("❌ ERRO: Segredos do GitHub em falta (verifique SMTP_USER, SMTP_PASS, BLOGGER_PUBLISH_EMAIL, GEMINI_API_KEY)!")
    sys.exit(1)

# Configurar o Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Catálogo - Nicho: Casa, Cozinha e Organização
PRODUCTS = [
    {
        "name": "Luminária De Mesa Cabeceira Touch",
        "link": "https://vt.tiktok.com/...", 
        "image": "https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/c5520bca5460470989f3c10b38a8b820~tplv-o3syd03w52-resize-webp:800:800.webp?dr=15584&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    },
    {
        "name": "Lençol Com Babado Helena 3 Peças 400 Fios Toque de Algodão",
        "link": "https://vt.tiktok.com/ZS9DV5KvJfUY6-87jXx/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/e80c2735205f48908a13bee29309f6b0~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    },
    {
        "name": "Colcha Lençol Casal Queen Helena 3 Peças Com Bababo Luxo Conforto Live",
        "link": "https://vt.tiktok.com/ZS9DVaJFXMusA-y6nOC/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/a20c88283bac41c08e9f38c714423dc5~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    },
    {
        "name": "Kit Jogo de Lençol Micropercal Tecido 400 Fios Lindas Fronhas Estampadas Com Zíper",
        "link": "https://vt.tiktok.com/ZS9DVaeAceBA8-r2PBP/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/0dfc825bb0984a4cb765eb15611d5794~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    },
    {
        "name": "Lençol + 2 Fronhas Casal|Queen|King e Solteiro +1 Fronha",
        "link": "https://vt.tiktok.com/ZS9DVaR4Rjmnf-V8eOj/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6f56e9f9d90942068cd0340eb164612b~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    },
    {
        "name": "Torneira Cozinha Parede Preta Flexível Duplo Jato Cone 1/4 de Volta para Mesa Pia Bancada e Mármore",
        "link": "https://vt.tiktok.com/ZS9DVaNWaY39r-rmWt5/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8f8e03dd9f1147c0a33ac4e6e4d098a1~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    },
    {
        "name": "Kit 2 Travesseiros Premium Soft 50x70cm Alto e Firme Antialérgico Conforto Lavável Macio",
        "link": "https://vt.tiktok.com/ZS9DVaNWg9gfW-bFK0u/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/238e874f78094af6bc774ddd05f68688~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    }
]

def generate_seo_article_with_gemini(product_name):
    """Usa o Gemini para gerar um artigo completo e otimizado para SEO de 350 a 450 palavras."""
    prompt = f"""
    Escreva um artigo de blog completo, original e otimizado para SEO (com entre 350 e 450 palavras) em Português do Brasil para o nicho de Casa, Cozinha e Organização.
    O produto em destaque é: "{product_name}".
    
    O artigo deve ser estruturado em HTML limpo (sem blocos markdown complexos, apenas tags `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>` e `<strong>`) contendo:
    1. Uma introdução cativante que desperte o interesse e fale sobre as necessidades de quem quer organizar ou decorar a casa.
    2. Seções detalhadas sobre as principais vantagens, design, utilidade e custo-benefício deste produto.
    3. Uma seção de Perguntas Frequentes (FAQ) com 2 perguntas curtas e respostas úteis para atrair tráfego orgânico do Google.
    
    Retorne APENAS o código HTML do corpo do artigo.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Remove eventuais blocos de código markdown gerados pela IA
        if text.startswith("```html"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
    except Exception as e:
        print(f"Erro ao gerar com Gemini: {e}. Usando conteúdo padrão.")
        return f"""
        <h2>Descubra as vantagens do {product_name}</h2>
        <p>Procurando por mais praticidade, conforto e organização para a sua casa? O <strong>{product_name}</strong> é a escolha perfeita para transformar o seu ambiente com excelente custo-benefício.</p>
        <p>Feito com materiais de alta qualidade, ele garante durabilidade e um toque especial de sofisticação para o seu dia a dia.</p>
        <h3>Por que escolher este produto?</h3>
        <ul>
            <li>Design moderno que se adapta a qualquer decoração.</li>
            <li>Fácil instalação e manuseio no dia a dia.</li>
            <li>Excelente durabilidade e resistência comprovada.</li>
        </ul>
        """

def send_to_blogger():
    product = random.choice(PRODUCTS)
    print(f"Produto selecionado: {product['name']}")
    
    # Gera o texto completo via Inteligência Artificial
    body_html = generate_seo_article_with_gemini(product['name'])
    
    title = f"Review e Análise Completa: {product['name']} Vale a Pena?"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        {body_html}
        <div style="text-align: center; margin: 25px 0;">
            <img src="{product['image']}" alt="{product['name']}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
            <p style="font-size: 11px; color: #777; font-style: italic; margin-top: 5px;">* Imagem meramente ilustrativa.</p>
        </div>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{product['link']}" target="_blank" style="background-color: #ff3b30; color: white; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">🔥 Ver Oferta Especial no TikTok Shop</a>
        </div>
    </div>
    """
    
    msg = MIMEMultipart()
    msg['From'] = VERIFIED_SENDER
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = title
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(VERIFIED_SENDER, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        print(f"Post gerado por IA e publicado com sucesso: {title}")
    except Exception as e:
        print(f"Erro ao publicar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_to_blogger()
