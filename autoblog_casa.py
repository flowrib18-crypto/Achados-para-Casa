import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import sys

# Configurações de Email (SMTP Profissional do Brevo)
SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 465
EMAIL_USER = os.environ.get("BLOG_EMAIL_USER")
EMAIL_PASS = os.environ.get("BLOG_EMAIL_PASS")
BLOGGER_EMAIL = os.environ.get("BLOGGER_PUBLISH_EMAIL")

# Catálogo Atualizado - Nicho: Casa, Cozinha e Organização
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

def generate_post_content(product):
    title = f"Review e Oferta: {product['name']}"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2>{product['name']}</h2>
        <div style="text-align: center; margin: 20px 0;">
            <img src="{product['image']}" alt="{product['name']}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
            <p style="font-size: 11px; color: #777; font-style: italic; margin-top: 5px;">* Imagem meramente ilustrativa.</p>
        </div>
        <p>Procurando por mais praticidade, conforto e organização para a sua casa? O <strong>{product['name']}</strong> é a escolha perfeita para transformar o seu ambiente com excelente custo-benefício.</p>
        <p>Feito com materiais de alta qualidade, ele garante durabilidade e um toque especial de sofisticação para o seu dia a dia.</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{product['link']}" target="_blank" style="background-color: #ff3b30; color: white; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 5px; font-size: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">🔥 Ver Oferta Especial no TikTok Shop</a>
        </div>
    </div>
    """
    return title, html_content

def send_to_blogger():
    product = random.choice(PRODUCTS)
    title, html_content = generate_post_content(product)
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = BLOGGER_EMAIL
    msg['Subject'] = title
    
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, BLOGGER_EMAIL, msg.as_string())
        server.quit()
        print(f"Post publicado com sucesso: {title}")
    except Exception as e:
        print(f"Erro ao publicar: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_to_blogger()
