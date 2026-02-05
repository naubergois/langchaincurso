"""
Scraper para extração de notícias do portal do TCU.
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import time
from tcu_models import NoticiaBasica, NoticiaCompleta


class TCUScraper:
    """Classe para extração de notícias do portal TCU."""
    
    BASE_URL = "https://portal.tcu.gov.br"
    NOTICIAS_URL = f"{BASE_URL}/imprensa/noticias/"
    
    def __init__(self, delay: float = 1.0):
        """
        Inicializa o scraper.
        
        Args:
            delay: Tempo de espera entre requisições (em segundos)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def listar_noticias(self, quantidade: int = 10) -> List[NoticiaBasica]:
        """
        Lista as notícias mais recentes.
        
        Args:
            quantidade: Número de notícias a extrair
            
        Returns:
            Lista de NoticiaBasica
        """
        print(f"📰 Extraindo lista de {quantidade} notícias do TCU...")
        
        try:
            response = self.session.get(self.NOTICIAS_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            noticias = []
            
            # Procurar por todos os links de notícias
            # O padrão é: /imprensa/noticias/[slug]
            links = soup.find_all('a', href=lambda x: x and '/imprensa/noticias/' in x and x != '/imprensa/noticias/')
            
            # Remover duplicatas mantendo a ordem
            urls_vistas = set()
            links_unicos = []
            for link in links:
                url = link['href']
                if not url.startswith('http'):
                    url = self.BASE_URL + url
                if url not in urls_vistas:
                    urls_vistas.add(url)
                    links_unicos.append((link, url))
            
            # Processar os links únicos
            for link, url in links_unicos[:quantidade]:
                try:
                    # Extrair título do link
                    titulo = link.get_text(strip=True)
                    
                    # Tentar encontrar data e resumo no contexto do link
                    # A estrutura geralmente é: data + título + resumo em um mesmo bloco
                    parent = link.parent
                    if parent:
                        texto_completo = parent.get_text(strip=True)
                        
                        # Tentar extrair data (formato DD/MM/YYYY)
                        import re
                        data_match = re.search(r'\d{2}/\d{2}/\d{4}', texto_completo)
                        data = data_match.group(0) if data_match else "Data não disponível"
                        
                        # O resumo geralmente vem depois do título
                        # Remover data e título para pegar o resumo
                        resumo = texto_completo
                        if data_match:
                            resumo = resumo.replace(data, '', 1)
                        resumo = resumo.replace(titulo, '', 1).strip()
                        
                        # Limitar tamanho do resumo
                        if len(resumo) > 200:
                            resumo = resumo[:200] + "..."
                        
                        if not resumo or len(resumo) < 10:
                            resumo = None
                    else:
                        data = "Data não disponível"
                        resumo = None
                    
                    # Limpar título (pode conter data no início)
                    import re
                    titulo = re.sub(r'^\d{2}/\d{2}/\d{4}\s*', '', titulo)
                    
                    if not titulo or len(titulo) < 5:
                        continue
                    
                    noticia = NoticiaBasica(
                        titulo=titulo,
                        data=data,
                        url=url,
                        resumo=resumo
                    )
                    
                    noticias.append(noticia)
                    print(f"  ✓ {titulo[:60]}...")
                    
                except Exception as e:
                    print(f"  ⚠️  Erro ao processar link: {e}")
                    continue
            
            print(f"✅ {len(noticias)} notícias extraídas com sucesso!\n")
            return noticias
            
        except Exception as e:
            print(f"❌ Erro ao listar notícias: {e}")
            return []
    
    def extrair_noticia(self, url: str) -> Optional[NoticiaCompleta]:
        """
        Extrai o conteúdo completo de uma notícia.
        
        Args:
            url: URL da notícia
            
        Returns:
            NoticiaCompleta ou None se houver erro
        """
        try:
            time.sleep(self.delay)  # Respeitar delay entre requisições
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrair título
            titulo_elem = soup.find('h1')
            titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sem título"
            
            # Extrair data
            data_elem = soup.find('time')
            if not data_elem:
                data_elem = soup.find('span', class_=['data', 'date'])
            data = data_elem.get_text(strip=True) if data_elem else "Data não disponível"
            
            # Extrair autor
            autor_elem = soup.find('span', class_=['autor', 'author'])
            if not autor_elem:
                autor_elem = soup.find(string=lambda x: x and 'Por' in x)
            autor = autor_elem.get_text(strip=True) if autor_elem else None
            
            # Extrair resumo/lead
            resumo_elem = soup.find('p', class_=['lead', 'resumo', 'subtitle'])
            if not resumo_elem:
                # Pegar primeiro parágrafo após o título
                resumo_elem = soup.find('p')
            resumo = resumo_elem.get_text(strip=True) if resumo_elem else None
            
            # Extrair conteúdo completo
            # Procurar pelo container principal de conteúdo
            conteudo_container = soup.find('div', class_=['conteudo', 'content', 'article-body'])
            if not conteudo_container:
                conteudo_container = soup.find('article')
            
            if conteudo_container:
                paragrafos = conteudo_container.find_all('p')
                conteudo = '\n\n'.join([p.get_text(strip=True) for p in paragrafos if p.get_text(strip=True)])
            else:
                conteudo = "Conteúdo não disponível"
            
            # Extrair temas/tags
            temas = []
            temas_container = soup.find('div', class_=['temas', 'tags', 'categorias'])
            if temas_container:
                tema_links = temas_container.find_all('a')
                temas = [link.get_text(strip=True) for link in tema_links]
            
            noticia = NoticiaCompleta(
                titulo=titulo,
                data=data,
                url=url,
                resumo=resumo,
                conteudo=conteudo,
                temas=temas,
                autor=autor
            )
            
            return noticia
            
        except Exception as e:
            print(f"  ❌ Erro ao extrair notícia {url}: {e}")
            return None
    
    def extrair_noticias_completas(self, quantidade: int = 5) -> List[NoticiaCompleta]:
        """
        Extrai notícias completas (lista + conteúdo).
        
        Args:
            quantidade: Número de notícias a extrair
            
        Returns:
            Lista de NoticiaCompleta
        """
        # Primeiro, listar as notícias
        noticias_basicas = self.listar_noticias(quantidade)
        
        # Depois, extrair conteúdo completo de cada uma
        noticias_completas = []
        
        print(f"📖 Extraindo conteúdo completo de {len(noticias_basicas)} notícias...\n")
        
        for i, noticia_basica in enumerate(noticias_basicas, 1):
            print(f"[{i}/{len(noticias_basicas)}] {noticia_basica.titulo[:60]}...")
            
            noticia_completa = self.extrair_noticia(noticia_basica.url)
            
            if noticia_completa:
                noticias_completas.append(noticia_completa)
                print(f"  ✓ Conteúdo extraído ({len(noticia_completa.conteudo)} caracteres)\n")
            else:
                print(f"  ⚠️  Falha na extração\n")
        
        print(f"✅ {len(noticias_completas)} notícias completas extraídas!\n")
        return noticias_completas
