# -*- coding: utf-8 -*-
"""Maquetador comun para los dos documentos."""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import os

W, H = A4
M = 42
AZUL = colors.HexColor("#1F4E79")
AZUL_CLARO = colors.HexColor("#DCE6F1")
AMBAR = colors.HexColor("#FFF4CE")
BORDE = colors.HexColor("#D0A000")
VERDE = colors.HexColor("#E2EFDA")
BORDE_V = colors.HexColor("#548235")
GRIS = colors.HexColor("#8C8C8C")


class Doc:
    def __init__(self, fichero, titulo, pie_corto, carpeta_img="rec/"):
        self.c = canvas.Canvas(fichero, pagesize=A4)
        self.c.setTitle(titulo)
        self.c.setAuthor("Futura Admin")
        self.pie_corto = pie_corto
        self.img = carpeta_img
        self.n = 0

    # ---------- utilidades ----------
    def _wrap(self, texto, tam, ancho, fuente="Helvetica"):
        lineas, act = [], ""
        for p in texto.split(" "):
            prueba = (act + " " + p).strip()
            if self.c.stringWidth(prueba, fuente, tam) <= ancho:
                act = prueba
            else:
                if act:
                    lineas.append(act)
                act = p
        if act:
            lineas.append(act)
        return lineas or [""]

    def _pie(self):
        self.c.setFillColor(GRIS)
        self.c.setFont("Helvetica", 8.5)
        self.c.drawRightString(W - M, 22, self.pie_corto)
        if self.n:
            self.c.drawString(M, 22, str(self.n))
        self.c.setFillColor(colors.black)

    def _caja(self, y, lineas, fondo, borde, titulo_negrita=True):
        lns = []
        for i, t in enumerate(lineas):
            f = "Helvetica-Bold" if (i == 0 and titulo_negrita) else "Helvetica"
            lns += [(l, f) for l in self._wrap(t, 11.5, W - 2 * M - 28, f)]
        h = 22 + 16 * len(lns)
        yb = max(46, y - h)
        self.c.setFillColor(fondo)
        self.c.setStrokeColor(borde)
        self.c.setLineWidth(1.2)
        self.c.roundRect(M, yb, W - 2 * M, h, 7, fill=1, stroke=1)
        self.c.setFillColor(colors.black)
        yy = yb + h - 17
        for ln, f in lns:
            self.c.setFont(f, 11.5)
            self.c.drawString(M + 14, yy, ln)
            yy -= 16
        return yb - 10

    def _alto_caja(self, lineas, titulo_negrita=True):
        if not lineas:
            return 0
        n = 0
        for i, t in enumerate(lineas):
            f = "Helvetica-Bold" if (i == 0 and titulo_negrita) else "Helvetica"
            n += len(self._wrap(t, 11.5, W - 2 * M - 28, f))
        return 22 + 16 * n + 10

    # ---------- paginas ----------
    def portada(self, titulo, subtitulo, intro, caja, pie):
        c = self.c
        c.setFillColor(AZUL)
        c.rect(0, H - 250, W, 250, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 33)
        c.drawCentredString(W / 2, H - 128, titulo)
        c.setFont("Helvetica", 18)
        c.drawCentredString(W / 2, H - 165, subtitulo)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 14.5)
        y = H - 335
        for t in intro:
            c.drawCentredString(W / 2, y, t)
            y -= 25
        if caja:
            c.setFillColor(AMBAR)
            c.setStrokeColor(BORDE)
            c.setLineWidth(1.2)
            alto = 34 + 22 * (len(caja) - 1)
            c.roundRect(M + 25, 260, W - 2 * M - 50, alto, 8, fill=1, stroke=1)
            c.setFillColor(colors.black)
            yy = 260 + alto - 24
            for i, t in enumerate(caja):
                c.setFont("Helvetica-Bold" if i == 0 else "Helvetica", 13.5 if i == 0 else 11.5)
                c.drawCentredString(W / 2, yy, t)
                yy -= 22
        c.setFont("Helvetica", 10.5)
        c.setFillColor(GRIS)
        yy = 112
        for t in pie:
            c.drawCentredString(W / 2, yy, t)
            yy -= 17
        c.setFillColor(colors.black)
        c.showPage()

    def indice(self, titulo, entradas):
        c = self.c
        c.setFillColor(AZUL)
        c.rect(0, H - 78, W, 78, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(M, H - 50, titulo)
        c.setFillColor(colors.black)
        y = H - 115
        for e in entradas:
            if isinstance(e, tuple):
                num, txt = e
                c.setFont("Helvetica", 12)
                c.drawString(M + 8, y, str(num) + ".")
                c.drawString(M + 38, y, txt)
                y -= 19
            else:
                y -= 8
                c.setFillColor(AZUL)
                c.setFont("Helvetica-Bold", 12.5)
                c.drawString(M, y, e)
                c.setFillColor(colors.black)
                y -= 21
        self._pie()
        c.showPage()

    def separador(self, parte, titulo, resumen):
        c = self.c
        c.setFillColor(AZUL)
        c.rect(0, H / 2 - 90, W, 180, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica", 15)
        c.drawCentredString(W / 2, H / 2 + 42, parte)
        c.setFont("Helvetica-Bold", 27)
        c.drawCentredString(W / 2, H / 2 - 2, titulo)
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12.5)
        y = H / 2 - 135
        for t in resumen:
            c.drawCentredString(W / 2, y, t)
            y -= 20
        self._pie()
        c.showPage()

    def pagina(self, num, titulo, bloques, imagen=None, ojo=None, truco=None):
        """bloques: lista de str. Prefijos: '# ' subtitulo, '> ' paso, '* ' vineta.
        Un bloque que empieza por espacios es continuacion del anterior."""
        unidos = []
        for b in bloques:
            if b.startswith(" ") and b.strip() and unidos:
                unidos[-1] = unidos[-1].rstrip() + " " + b.strip()
            else:
                unidos.append(b)
        bloques = unidos
        c = self.c
        self.n = num if isinstance(num, int) else self.n
        c.setFillColor(AZUL)
        c.rect(0, H - 78, W, 78, fill=1, stroke=0)
        c.setFillColor(colors.white)
        if isinstance(num, int):
            c.setFont("Helvetica-Bold", 29)
            c.drawString(M, H - 55, str(num))
            x0 = M + 44
        else:
            x0 = M
        c.setFont("Helvetica-Bold", 17)
        for ln in self._wrap(titulo, 17, W - x0 - M, "Helvetica-Bold")[:2]:
            c.drawString(x0, H - 51, ln)
            break
        c.setFillColor(colors.black)

        y = H - 104
        for b in bloques:
            if b == "":
                y -= 8
            elif b.startswith("# "):
                y -= 4
                c.setFillColor(AZUL)
                c.setFont("Helvetica-Bold", 13)
                for ln in self._wrap(b[2:], 13, W - 2 * M, "Helvetica-Bold"):
                    c.drawString(M, y, ln)
                    y -= 18
                c.setFillColor(colors.black)
                y -= 3
            elif b.startswith("> "):
                c.setFont("Helvetica", 12.5)
                lns = self._wrap(b[2:], 12.5, W - 2 * M - 22)
                for i, ln in enumerate(lns):
                    c.drawString(M + (0 if i == 0 else 22), y, ln)
                    y -= 17.5
            elif b.startswith("* "):
                c.setFont("Helvetica", 12.5)
                c.drawString(M + 6, y, "•")
                lns = self._wrap(b[2:], 12.5, W - 2 * M - 22)
                for i, ln in enumerate(lns):
                    c.drawString(M + 20, y, ln)
                    y -= 17.5
            else:
                c.setFont("Helvetica", 12.5)
                for ln in self._wrap(b, 12.5, W - 2 * M):
                    c.drawString(M, y, ln)
                    y -= 17.5
        y -= 6

        reserva = 46 + self._alto_caja(ojo) + self._alto_caja(truco)
        if imagen:
            ruta = self.img + imagen + ".png"
            if os.path.exists(ruta):
                im = ImageReader(ruta)
                iw, ih = im.getSize()
                dw = W - 2 * M
                dh = dw * ih / iw
                maxh = y - reserva - 8
                if dh > maxh:
                    dh = maxh
                    dw = dh * iw / ih
                if dh > 40:
                    x = (W - dw) / 2
                    c.drawImage(im, x, y - dh, width=dw, height=dh)
                    c.setStrokeColor(GRIS)
                    c.setLineWidth(0.8)
                    c.rect(x, y - dh, dw, dh, fill=0, stroke=1)
                    y = y - dh - 14
        if truco:
            y = self._caja(y, truco, VERDE, BORDE_V)
        if ojo:
            y = self._caja(y, ojo, AMBAR, BORDE)
        self._pie()
        c.showPage()

    def guardar(self):
        self.c.save()
