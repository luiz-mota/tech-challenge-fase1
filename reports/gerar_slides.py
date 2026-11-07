"""
Gera a apresentação PowerPoint do projeto NPS Preditivo.
Executar: python reports/gerar_slides.py
Saída:    reports/apresentacao_nps.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import os

# ---------------------------------------------------------------------------
# Paleta de cores
# ---------------------------------------------------------------------------
AZUL_ESCURO  = RGBColor(0x1A, 0x35, 0x5E)   # fundo capa / títulos
AZUL_CLARO   = RGBColor(0x27, 0x74, 0xC0)   # destaque / subtítulos
VERMELHO     = RGBColor(0xC0, 0x39, 0x2B)   # alerta / problema
VERDE        = RGBColor(0x1E, 0x8B, 0x4C)   # positivo / recomendação
AMARELO      = RGBColor(0xF3, 0x9C, 0x12)   # atenção / neutro
CINZA_FUNDO  = RGBColor(0xF4, 0xF6, 0xF9)   # fundo slides internos
CINZA_TEXTO  = RGBColor(0x2C, 0x3E, 0x50)   # texto principal
BRANCO       = RGBColor(0xFF, 0xFF, 0xFF)

SLIDE_W = Inches(13.33)
SLIDE_H = Inches(7.5)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def nova_apresentacao():
    prs = Presentation()
    prs.slide_width  = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def fundo_solido(slide, cor: RGBColor):
    """Preenche o fundo do slide com cor sólida."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = cor


def adicionar_caixa(slide, left, top, width, height,
                    texto="", tamanho=24, cor_texto=CINZA_TEXTO,
                    negrito=False, alinhamento=PP_ALIGN.LEFT,
                    cor_fundo=None, transparente=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf    = txBox.text_frame
    tf.word_wrap = True

    if cor_fundo and not transparente:
        txBox.fill.solid()
        txBox.fill.fore_color.rgb = cor_fundo

    p  = tf.paragraphs[0]
    p.alignment = alinhamento
    run = p.add_run()
    run.text = texto
    run.font.size   = Pt(tamanho)
    run.font.color.rgb = cor_texto
    run.font.bold   = negrito
    return txBox


def adicionar_titulo_slide(slide, titulo, subtitulo=None):
    """Barra superior escura com título branco."""
    barra = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(0), Inches(0), SLIDE_W, Inches(1.4)
    )
    barra.fill.solid()
    barra.fill.fore_color.rgb = AZUL_ESCURO
    barra.line.fill.background()

    adicionar_caixa(slide,
        left=Inches(0.4), top=Inches(0.1),
        width=Inches(12.5), height=Inches(0.8),
        texto=titulo, tamanho=32,
        cor_texto=BRANCO, negrito=True,
        alinhamento=PP_ALIGN.LEFT)

    if subtitulo:
        adicionar_caixa(slide,
            left=Inches(0.4), top=Inches(0.9),
            width=Inches(12.5), height=Inches(0.45),
            texto=subtitulo, tamanho=16,
            cor_texto=RGBColor(0xAD, 0xC6, 0xE5),
            alinhamento=PP_ALIGN.LEFT)


def adicionar_bullets(slide, bullets: list[tuple],
                      left, top, width, height, tamanho=20):
    """
    bullets: lista de (texto, cor_icone, recuo)
    recuo 0 = principal, 1 = sub-item
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf    = txBox.text_frame
    tf.word_wrap = True

    for i, (texto, cor, recuo) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(6 if recuo == 0 else 2)
        p.level = recuo

        run = p.add_run()
        icone = "▶  " if recuo == 0 else "    •  "
        run.text = icone + texto
        run.font.size  = Pt(tamanho if recuo == 0 else tamanho - 2)
        run.font.color.rgb = cor if recuo == 0 else CINZA_TEXTO
        run.font.bold  = (recuo == 0)


def adicionar_imagem_se_existir(slide, caminho, left, top, width, height):
    if os.path.exists(caminho):
        slide.shapes.add_picture(caminho, left, top, width, height)
    else:
        # placeholder cinza com aviso
        ph = slide.shapes.add_shape(1, left, top, width, height)
        ph.fill.solid()
        ph.fill.fore_color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
        ph.line.color.rgb = RGBColor(0xAA, 0xAA, 0xAA)
        adicionar_caixa(slide, left, top + height // 3, width, Inches(0.5),
                        "[gráfico não encontrado]", 14,
                        CINZA_TEXTO, alinhamento=PP_ALIGN.CENTER)


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------

def slide_capa(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    fundo_solido(slide, AZUL_ESCURO)

    # Linha decorativa colorida
    linha = slide.shapes.add_shape(1,
        Inches(0), Inches(3.5), SLIDE_W, Inches(0.06))
    linha.fill.solid()
    linha.fill.fore_color.rgb = AZUL_CLARO
    linha.line.fill.background()

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(1.2),
        width=Inches(11), height=Inches(1.2),
        texto="NPS Preditivo — E-commerce Nacional",
        tamanho=40, cor_texto=BRANCO, negrito=True,
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(2.5),
        width=Inches(11), height=Inches(0.7),
        texto="O que está destruindo a satisfação dos nossos clientes — e o que fazer agora",
        tamanho=20, cor_texto=RGBColor(0xAD, 0xC6, 0xE5),
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(4.0),
        width=Inches(11), height=Inches(0.5),
        texto="Tech Challenge Fase 1  |  PosTech FIAP  |  Ciência de Dados & IA",
        tamanho=14, cor_texto=RGBColor(0x78, 0x9A, 0xBF),
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(4.6),
        width=Inches(11), height=Inches(0.5),
        texto="Base: 2.500 pedidos  |  Período: série histórica única  |  2026",
        tamanho=13, cor_texto=RGBColor(0x78, 0x9A, 0xBF),
        alinhamento=PP_ALIGN.CENTER)


def slide_contexto(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "1. Contexto do Problema",
                           "Por que precisamos entender o NPS agora?")

    bullets = [
        ("O NPS da empresa é −80", VERMELHO, 0),
        ("Para cada cliente satisfeito, há 19 insatisfeitos", CINZA_TEXTO, 1),
        ("84,4% dos clientes são detratores — abaixo de qualquer benchmark de mercado", CINZA_TEXTO, 1),

        ("O NPS só é medido depois que o cliente vai embora", VERMELHO, 0),
        ("Não há como agir preventivamente: o problema já aconteceu", CINZA_TEXTO, 1),
        ("Sem previsão = sem prioridade = ciclo de perda de clientes", CINZA_TEXTO, 1),

        ("Este estudo identifica as causas raiz e propõe ações concretas", AZUL_CLARO, 0),
        ("Análise de 2.500 pedidos com 18 variáveis operacionais", CINZA_TEXTO, 1),
    ]
    adicionar_bullets(slide, bullets,
        left=Inches(0.6), top=Inches(1.6),
        width=Inches(12), height=Inches(5.5))


def slide_pergunta(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, AZUL_ESCURO)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(1.5),
        width=Inches(11), height=Inches(1.0),
        texto="A pergunta central deste projeto:",
        tamanho=22, cor_texto=RGBColor(0xAD, 0xC6, 0xE5),
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(2.6),
        width=Inches(11), height=Inches(1.8),
        texto='"Quais fatores operacionais\nrealmente destroem — ou elevam —\na satisfação dos nossos clientes?"',
        tamanho=30, cor_texto=BRANCO, negrito=True,
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(4.8),
        width=Inches(11), height=Inches(0.6),
        texto="Resposta: 3 drivers explicam quase tudo.",
        tamanho=18, cor_texto=AMARELO,
        alinhamento=PP_ALIGN.CENTER)


def slide_achado1(prs, caminho_grafico):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "Achado 1 — Atraso na Entrega Destrói o NPS",
                           "O maior driver negativo identificado na análise")

    bullets = [
        ("Correlação de −0,60 com o NPS: o fator mais forte encontrado", VERMELHO, 0),
        ("A cada dia de atraso, a nota do cliente cai de forma consistente", CINZA_TEXTO, 1),

        ("Ponto de ruptura em 3 dias de atraso", VERMELHO, 0),
        ("Antes: NPS ainda positivo. Depois: colapso para zona de detratores", CINZA_TEXTO, 1),
        ("Com 7+ dias de atraso, o NPS médio cai para menos de 2 (em 10)", CINZA_TEXTO, 1),

        ("O prazo prometido importa mais do que o prazo real", AZUL_CLARO, 0),
        ("'Tempo total de entrega' não tem impacto — só o atraso em relação ao prometido", CINZA_TEXTO, 1),
    ]
    adicionar_bullets(slide, bullets,
        left=Inches(0.5), top=Inches(1.6),
        width=Inches(6.5), height=Inches(5.5), tamanho=18)

    adicionar_imagem_se_existir(slide, caminho_grafico,
        left=Inches(7.1), top=Inches(1.5),
        width=Inches(5.8), height=Inches(5.7))


def slide_achado2(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "Achado 2 — Reclamações Destroem a Recompra",
                           "Segundo driver mais impactante: correlação −0,50 com o NPS")

    # Cards com números de impacto
    def card(left, top, w, h, numero, descricao, cor_num):
        caixa = slide.shapes.add_shape(1, left, top, w, h)
        caixa.fill.solid()
        caixa.fill.fore_color.rgb = BRANCO
        caixa.line.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)

        adicionar_caixa(slide, left + Inches(0.1), top + Inches(0.1),
                        w - Inches(0.2), Inches(0.9),
                        numero, 38, cor_num, negrito=True,
                        alinhamento=PP_ALIGN.CENTER)
        adicionar_caixa(slide, left + Inches(0.1), top + Inches(1.0),
                        w - Inches(0.2), Inches(1.0),
                        descricao, 15, CINZA_TEXTO,
                        alinhamento=PP_ALIGN.CENTER)

    card(Inches(0.4), Inches(1.6), Inches(3.8), Inches(2.2),
         "69,6%", "dos clientes SEM reclamações\nrecompram em 30 dias",
         VERDE)

    card(Inches(4.5), Inches(1.6), Inches(3.8), Inches(2.2),
         "< 6%", "dos clientes com 4+\nreclamações recompram",
         VERMELHO)

    card(Inches(8.6), Inches(1.6), Inches(4.3), Inches(2.2),
         "9,01 vs 3,94", "NPS médio: quem recomprou\nvs. quem não recomprou",
         AZUL_CLARO)

    bullets = [
        ("Reclamação não é apenas insatisfação — é sinal de risco de churn", VERMELHO, 0),
        ("A recompra em 30 dias é o melhor indicador de fidelidade disponível nos dados", AZUL_CLARO, 0),
        ("Reduzir reclamações é o caminho mais direto para aumentar receita recorrente", VERDE, 0),
    ]
    adicionar_bullets(slide, bullets,
        left=Inches(0.5), top=Inches(4.1),
        width=Inches(12.5), height=Inches(3.0), tamanho=18)


def slide_achado3(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "Achado 3 — Contato com Suporte Sinaliza Problema",
                           "Correlação −0,38 com NPS: indicador de alerta antecipado")

    bullets = [
        ("Quanto mais o cliente aciona o suporte, menor é o NPS final", VERMELHO, 0),
        ("Isso indica que o contato é reativo — o cliente liga porque algo saiu errado", CINZA_TEXTO, 1),
        ("Não é o suporte que gera insatisfação: é o problema anterior a ele", CINZA_TEXTO, 1),

        ("Volume de contatos = termômetro de falhas operacionais", AMARELO, 0),
        ("Pico de chamados em determinados dias indica problemas sistêmicos", CINZA_TEXTO, 1),
        ("Times de operações podem usar esse indicador como alerta precoce", CINZA_TEXTO, 1),

        ("Resolução rápida atenua — mas não elimina — o impacto negativo", AZUL_CLARO, 0),
        ("A meta deve ser evitar o contato, não apenas resolver rapidamente", CINZA_TEXTO, 1),
    ]
    adicionar_bullets(slide, bullets,
        left=Inches(0.6), top=Inches(1.6),
        width=Inches(12), height=Inches(5.5))


def slide_nao_importa(prs, caminho_grafico):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "O que NÃO Move o NPS",
                           "Antes de investir, verifique: alguns fatores têm impacto próximo de zero")

    bullets = [
        ("Idade do cliente — correlação: 0,01", CINZA_TEXTO, 0),
        ("Jovens e idosos são igualmente insatisfeitos quando a entrega atrasa", CINZA_TEXTO, 1),

        ("Valor do pedido — correlação: 0,04", CINZA_TEXTO, 0),
        ("Compra de R$ 50 ou R$ 5.000: o que importa é cumprir o prazo", CINZA_TEXTO, 1),

        ("Região geográfica — diferença entre regiões: irrelevante", CINZA_TEXTO, 0),
        ("Não há região 'naturalmente mais difícil' de satisfazer", CINZA_TEXTO, 1),

        ("Tempo total de entrega (em dias absolutos) — correlação: 0,001", AMARELO, 0),
        ("O cliente tolera 10 dias de frete se foi o prazo prometido", CINZA_TEXTO, 1),
        ("Ele não tolera 2 dias de atraso mesmo que o frete total seja de 3 dias", CINZA_TEXTO, 1),
    ]
    adicionar_bullets(slide, bullets,
        left=Inches(0.5), top=Inches(1.6),
        width=Inches(6.5), height=Inches(5.5), tamanho=17)

    adicionar_imagem_se_existir(slide, caminho_grafico,
        left=Inches(7.1), top=Inches(1.5),
        width=Inches(5.8), height=Inches(5.7))


def slide_recomendacoes(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "3 Recomendações Práticas",
                           "Ações diretas para as áreas de Logística, Suporte e Produto")

    def bloco_rec(numero, titulo, descricao, cor, left, top):
        w, h = Inches(3.8), Inches(4.5)
        caixa = slide.shapes.add_shape(1, left, top, w, h)
        caixa.fill.solid()
        caixa.fill.fore_color.rgb = BRANCO
        caixa.line.color.rgb = cor

        # Faixa de cor no topo
        faixa = slide.shapes.add_shape(1, left, top, w, Inches(0.2))
        faixa.fill.solid()
        faixa.fill.fore_color.rgb = cor
        faixa.line.fill.background()

        adicionar_caixa(slide, left + Inches(0.15), top + Inches(0.3),
                        w - Inches(0.3), Inches(0.7),
                        numero, 36, cor, negrito=True,
                        alinhamento=PP_ALIGN.CENTER)
        adicionar_caixa(slide, left + Inches(0.15), top + Inches(1.0),
                        w - Inches(0.3), Inches(0.7),
                        titulo, 16, CINZA_TEXTO, negrito=True,
                        alinhamento=PP_ALIGN.CENTER)
        adicionar_caixa(slide, left + Inches(0.15), top + Inches(1.8),
                        w - Inches(0.3), Inches(2.5),
                        descricao, 14, CINZA_TEXTO,
                        alinhamento=PP_ALIGN.LEFT)

    bloco_rec("01", "Alertas automáticos de risco\n de atraso",
              "Logística deve notificar proativamente o cliente quando "
              "há risco de ultrapassar o prazo prometido. Comunicar antes "
              "reduz o impacto negativo — mesmo que o atraso ocorra.",
              VERMELHO, Inches(0.4), Inches(1.6))

    bloco_rec("02", "Meta de resolução\n no primeiro contato",
              "Suporte deve resolver na primeira ligação/chat. "
              "Cada retorno do cliente multiplica a insatisfação. "
              "Medir a taxa de 'First Contact Resolution' e incluir "
              "na meta da equipe.",
              AZUL_CLARO, Inches(4.6), Inches(1.6))

    bloco_rec("03", "Calibrar prazos prometidos\n no site",
              "Revisar os prazos exibidos no checkout para que "
              "sejam cumpridos em pelo menos 95% dos casos. "
              "Prometer menos e entregar no prazo gera mais "
              "satisfação do que prometer rápido e atrasar.",
              VERDE, Inches(8.8), Inches(1.6))


def slide_limitacoes(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, CINZA_FUNDO)
    adicionar_titulo_slide(slide, "Limitações da Análise",
                           "O que esses dados não conseguem explicar — e por quê isso importa")

    bullets = [
        ("Série histórica única — sem sazonalidade", AMARELO, 0),
        ("Não sabemos se o NPS é diferente na Black Friday, férias ou períodos de crise", CINZA_TEXTO, 1),
        ("Recomendamos repetir a análise com dados de ao menos 12 meses", CINZA_TEXTO, 1),

        ("Correlação não é causa — só campo para investigação", AMARELO, 0),
        ("Outros fatores não medidos (qualidade do produto, preço, concorrência) podem influenciar", CINZA_TEXTO, 1),
        ("Para confirmar causalidade, são necessários testes A/B controlados", CINZA_TEXTO, 1),

        ("O motivo da reclamação não está nos dados", AMARELO, 0),
        ("Sabemos que há reclamações, mas não sabemos por quê — enriquecimento qualitativo necessário", CINZA_TEXTO, 1),

        ("NPS medido apenas ao final da jornada", AMARELO, 0),
        ("O próximo passo é um modelo preditivo que antecipe o NPS durante a operação", CINZA_TEXTO, 1),
    ]
    adicionar_bullets(slide, bullets,
        left=Inches(0.6), top=Inches(1.6),
        width=Inches(12), height=Inches(5.5), tamanho=17)


def slide_encerramento(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fundo_solido(slide, AZUL_ESCURO)

    linha = slide.shapes.add_shape(1,
        Inches(0), Inches(3.6), SLIDE_W, Inches(0.06))
    linha.fill.solid()
    linha.fill.fore_color.rgb = VERDE
    linha.line.fill.background()

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(1.2),
        width=Inches(11), height=Inches(1.0),
        texto="Resumo Executivo",
        tamanho=18, cor_texto=RGBColor(0xAD, 0xC6, 0xE5),
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(2.1),
        width=Inches(11), height=Inches(1.3),
        texto="3 drivers. 3 recomendações. Uma meta: sair do NPS −80.",
        tamanho=28, cor_texto=BRANCO, negrito=True,
        alinhamento=PP_ALIGN.CENTER)

    adicionar_caixa(slide,
        left=Inches(1.5), top=Inches(3.9),
        width=Inches(10), height=Inches(2.2),
        texto=(
            "Atraso na entrega  →  alertas proativos de logística\n"
            "Reclamações crescentes  →  meta de resolução no 1.º contato\n"
            "Prazo prometido irreal  →  calibrar datas no checkout"
        ),
        tamanho=18, cor_texto=RGBColor(0xAD, 0xC6, 0xE5),
        alinhamento=PP_ALIGN.LEFT)

    adicionar_caixa(slide,
        left=Inches(1), top=Inches(6.3),
        width=Inches(11), height=Inches(0.5),
        texto="Tech Challenge Fase 1  |  PosTech FIAP  |  2026",
        tamanho=13, cor_texto=RGBColor(0x78, 0x9A, 0xBF),
        alinhamento=PP_ALIGN.CENTER)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    base = os.path.dirname(os.path.abspath(__file__))  # pasta reports/

    caminho_grafico_atraso   = os.path.join(base, "03_nps_por_atraso.png")
    caminho_grafico_ranking  = os.path.join(base, "05_ranking_correlacao_nps.png")

    prs = nova_apresentacao()

    slide_capa(prs)
    slide_contexto(prs)
    slide_pergunta(prs)
    slide_achado1(prs, caminho_grafico_atraso)
    slide_achado2(prs)
    slide_achado3(prs)
    slide_nao_importa(prs, caminho_grafico_ranking)
    slide_recomendacoes(prs)
    slide_limitacoes(prs)
    slide_encerramento(prs)

    saida = os.path.join(base, "apresentacao_nps.pptx")
    prs.save(saida)
    print(f"Apresentação salva em: {saida}")
    print(f"Total de slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()
