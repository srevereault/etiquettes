# coding: utf8
# This file is part of pylabels, a Python library to create PDFs for printing
# labels.
# Copyright (C) 2012, 2013, 2014 Blair Bonnett
#
# pylabels is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pylabels is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pylabels.  If not, see <http://www.gnu.org/licenses/>.

import labels
import qrcode
import csv
import argparse
from reportlab.graphics import shapes
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont, stringWidth

# On attend en entrée le nom d'un cvs

parser = argparse.ArgumentParser(description='Generateur d\'etiquettes')
parser.add_argument('-i','--input', help='fichier csv en entree',required=True)
args = parser.parse_args()

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = labels.Specification(210, 297, 2, 6, 99, 42.3, top_margin=21.5, row_gap=0)

# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    Prenom = obj[0]
    Nom = obj[1]
    Entreprise = obj[2]
    Email = obj[3]
    Tel = obj[4]

    # Measure the width of the first name and shrink the font size until it fits.
    prenom_font_size = 14
    text_width = width - 90
    prenom_width = stringWidth(Prenom, "Helvetica", prenom_font_size)
    while prenom_width > text_width:
        prenom_font_size *= 0.8
        prenom_width = stringWidth(Prenom, "Helvetica", prenom_font_size)

    label.add(shapes.String(10, 90, Prenom.decode('utf-8').title(), fontName="Helvetica-Bold", fontSize=prenom_font_size))

    # Measure the width of the last name and shrink the font size until it fits.
    nom_font_size = 14
    text_width = width - 90
    nom_width = stringWidth(Nom, "Helvetica", nom_font_size)
    while nom_width > text_width:
        nom_font_size *= 0.8
        nom_width = stringWidth(Nom, "Helvetica", nom_font_size)

    label.add(shapes.String(10, 60, Nom.decode('utf-8').upper(), fontName="Helvetica-Bold", fontSize=nom_font_size))

    # Measure the width of the entreprise and shrink the font size until it fits.
    entreprise_font_size = 14
    text_width = width - 5
    Entreprise_width = stringWidth(Entreprise, "Helvetica", entreprise_font_size)
    while Entreprise_width > text_width:
        entreprise_font_size *= 0.8
        Entreprise_width = stringWidth(Entreprise, "Helvetica", entreprise_font_size)

    label.add(shapes.String(10, 20, Entreprise, fontName="Helvetica", fontSize=entreprise_font_size))

    # Insertion du QRCode
    NomComplet= Prenom + " " + Nom
    vcard="BEGIN:VCARD\nN:" + NomComplet + "\nORG:" + Entreprise + "\nEMAIL:" + Email + "\nTEL;TYPE=WORK:" + Tel + "\nEND:VCARD"
    img = qrcode.make(vcard)
    label.add(shapes.Image(190,35,80,80,img))

# Create the sheet.
sheet = labels.Sheet(specs, draw_label, border=False)

# Add a couple of labels.
with open(args.input, 'rb') as csvfile:
  reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
  for row in reader:
      donnees = (row['Prénom'], row['Nom'], row['Entreprise'], row['E-mail'], row['Téléphone professionnel'])
      sheet.add_label(donnees)

# Save the file and we are done.
sheet.save('basic.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))
