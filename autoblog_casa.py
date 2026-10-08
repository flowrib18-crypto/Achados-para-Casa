import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import sys
import time
from google import genai

# Configurações de Email (SMTP Direto do Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = os.environ.get("BLOG_EMAIL_USER")
SMTP_PASS = os.environ.get("BLOG_EMAIL_PASS")
BLOGGER_EMAIL = os.environ.get("BLOGGER_PUBLISH_EMAIL")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not SMTP_USER or not SMTP_PASS or not BLOGGER_EMAIL or not GEMINI_API_KEY:
    print("❌ ERRO: Segredos do GitHub em falta!")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

# Catálogo de Produtos Afiliados
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
        "name": "Torneira Cozinha Parede Preta Flexível Duplo Jato Cone 1/4 de Volta para Mesa Pia Bancada e Mármore",
        "link": "https://vt.tiktok.com/ZS9DVaNWaY39r-rmWt5/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8f8e03dd9f1147c0a33ac4e6e4d098a1~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    }
]

def generate_html_from_gemini(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            text = response.text.strip()
            if text.startswith("```html"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            print("✅ Artigo gerado com sucesso pela Inteligência Artificial!")
            return text.strip()
        except Exception as e:
            print(f"⚠️ Tentativa {attempt + 1} falhou (Erro: {e})")
            if attempt < max_retries - 1:
                print("🔄 A aguardar 5 segundos para tentar novamente...")
                time.sleep(5)
            else:
                print("❌ Esgotadas as tentativas com o Gemini.")
                return None

def create_post():
    # Sorteia entre: 50% Produto Afiliado, 50% Tendência / Assunto em Alta do Momento
    post_type = random.choices(['product', 'trend'], weights=[50, 50], k=1)[0]
    
    if post_type == 'product':
        product = random.choice(PRODUCTS)
        print(f"📦 Modo Produto Selecionado: {product['name']}")
        
        prompt = f"""
        Atua como especialista em SEO e Redação Web. Escreve um artigo de blog original e otimizado (400-500 palavras) em Português do Brasil sobre o produto: "{product['name']}".
        Estrutura em HTML limpo (tags `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`):
        1. Introdução cativante abordando dores do lar.
        2. Vantagens, design e custo-benefício.
        3. Dicas práticas de uso.
        4. FAQ com 2 perguntas.
        Retorna APENAS o HTML puro.
        """
        body_html = generate_html_from_gemini(prompt)
        if not body_html:
            body_html = f"<h2>{product['name']}</h2><p>Destaque imperdível para a sua casa.</p>"
            
        title = f"Review e Análise Completa: {product['name']} Vale a Pena?"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto;">
            {body_html}
            <div style="text-align: center; margin: 30px 0;">
                <img src="{product['image']}" alt="{product['name']}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
                <p style="font-size: 11px; color: #777; font-style: italic; margin-top: 8px;">* Imagem meramente ilustrativa.</p>
            </div>
            <div style="text-align: center; margin: 35px 0;">
                <a href="{product['link']}" target="_blank" style="background-color: #ff3b30; color: white; padding: 14px 28px; text-decoration: none; font-weight: bold; border-radius: 6px; font-size: 16px; box-shadow: 0 4px 8px rgba(255,59,48,0.3);">🔥 Ver Oferta Especial no TikTok Shop</a>
            </div>
        </div>
        """
    else:
        print("🔥 Modo Tendência / Assunto em Alta Selecionado")
        
        prompt = """
        Atua como um especialista em SEO e criador de conteúdos virais. Escolhe uma tendência atual, truque inovador ou assunto em alta no momento no nicho de 'Casa, Cozinha e Organização' (por exemplo, otimização de espaços compactos, minimalismo prático, hacks de limpeza rápida ou organização estética).
        Escreve um artigo de blog totalmente original, cativante e rico em palavras-chave (400-500 palavras) em Português do Brasil.
        Estrutura estritamente em HTML limpo (tags `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>`):
        1. Título atraente no início do conteúdo (dentro de `<h2>`).
        2. Introdução instigante sobre o porquê de esta tendência estar a dar que falar nas redes sociais e casas modernas.
        3. Passo a passo ou dicas práticas detalhadas com subtítulos (`<h2>` e `<h3>`).
        4. Conclusão inspiradora.
        Retorna APENAS o HTML puro.
        """
        body_html = generate_html_from_gemini(prompt)
        if not body_html:
            body_html = "<h2>Tendências para Organizar a Casa</h2><p>Descubra as novidades que estão a transformar os lares.</p>"
            
        title = "Tendências de Organização e Decoração Que Estão a Marcar Este Mês"
        
        general_link = PRODUCTS[0]["link"]
        general_image = PRODUCTS[0]["image"]
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto;">
            {body_html}
            <div style="text-align: center; margin: 30px 0;">
                <img src="{general_image}" alt="Tendências para Casa" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />
                <p style="font-size: 11px; color: #777; font-style: italic; margin-top: 8px;">* Imagem meramente ilustrativa.</p>
            </div>
            <div style="text-align: center; margin: 35px 0;">
                <a href="{general_link}" target="_blank" style="background-color: #2ea44f; color: white; padding: 14px 28px; text-decoration: none; font-weight: bold; border-radius: 6px; font-size: 16px; box-shadow: 0 4px 8px rgba(46,164,79,0.3);">✨ Explorar Produtos em Alta no TikTok Shop</a>
            </div>
        </div>
        """

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = title
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        print(f"✅ Publicado com sucesso no Blogger: {title}")
    except Exception as e:
        print(f"❌ Erro ao enviar email SMTP: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_post()
