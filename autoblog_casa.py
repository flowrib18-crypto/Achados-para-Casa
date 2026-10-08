import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import sys
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

# Configurar o Cliente Gemini com a nova biblioteca oficial
client = genai.Client(api_key=GEMINI_API_KEY)

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
        "name": "Torneira Cozinha Parede Preta Flexível Duplo Jato Cone 1/4 de Volta para Mesa Pia Bancada e Mármore",
        "link": "https://vt.tiktok.com/ZS9DVaNWaY39r-rmWt5/",
        "image": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8f8e03dd9f1147c0a33ac4e6e4d098a1~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my2&from=3376456192"
    }
]

def generate_seo_article_with_gemini(product_name):
    prompt = f"""
    Atua como um especialista em SEO e Redação Web. Escreve um artigo de blog completo, original, rico em palavras-chave e otimizado para motores de busca (com cerca de 400 a 500 palavras) em Português do Brasil.
    O produto em destaque é: "{product_name}" (nicho de Casa, Cozinha e Organização).
    
    O artigo deve ser estruturado exclusivamente em HTML limpo (sem blocos markdown nas pontas, apenas tags `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>` e `<strong>`) contendo:
    1. Uma introdução cativante que prenda o leitor e aborde as dores de organizar ou decorar a casa.
    2. Várias secções com subtítulos (`<h2>` e `<h3>`) detalhando as principais vantagens, materiais, design e o excelente custo-benefício do produto.
    3. Dicas práticas de utilização no dia a dia.
    4. Uma secção de Perguntas Frequentes (FAQ) com 2 perguntas e respetivas respostas.
    
    Retorna APENAS o código HTML puro do corpo do artigo.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.strip()
        
        if text.startswith("```html"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        print("✅ Artigo gerado com sucesso pela Inteligência Artificial do Gemini!")
        return text.strip()
    except Exception as e:
        print(f"⚠️ Erro detalhado ao comunicar com o Gemini: {e}")
        return f"""
        <h2>Tudo o que precisa saber sobre {product_name}</h2>
        <p>Procurando por mais praticidade, conforto e organização para o seu lar? O <strong>{product_name}</strong> chegou para revolucionar a rotina da sua casa, combinando alta tecnologia, design sofisticado e um preço imperdível.</p>
        <p>Investir em itens que facilitam o dia a dia e trazem elegância para os ambientes tornou-se essencial. Este produto destaca-se pela excelente durabilidade e acabamento premium.</p>
        <h3>Principais Vantagens e Benefícios</h3>
        <ul>
            <li><strong>Design Moderno:</strong> Adapta-se perfeitamente a qualquer estilo de decoração.</li>
            <li><strong>Praticidade Extrema:</strong> Facilita as tarefas diárias com máxima eficiência.</li>
            <li><strong>Durabilidade Superior:</strong> Fabricado com materiais resistentes de alta qualidade.</li>
        </ul>
        <h3>Por que vale a pena adquirir?</h3>
        <p>Além de otimizar o espaço e valorizar o ambiente, o custo-benefício faz desta uma das melhores escolhas do mercado atual para quem valoriza organização e bom gosto.</p>
        <h3>Perguntas Frequentes</h3>
        <p><strong>O produto é de fácil instalação ou uso?</strong> Sim, foi desenvolvido para uso prático e imediato.</p>
        <p><strong>Como posso garantir o meu com desconto?</strong> Basta aceder ao link oficial da oferta logo abaixo.</p>
        """

def send_to_blogger():
    product = random.choice(PRODUCTS)
    print(f"Produto selecionado: {product['name']}")
    
    body_html = generate_seo_article_with_gemini(product['name'])
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
        print(f"Post publicado com sucesso no Blogger: {title}")
    except Exception as e:
        print(f"Erro ao enviar email SMTP: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_to_blogger()
