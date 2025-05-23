from cgitb import text
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import sys

def fix_special(s):  
  s = s.replace("\\textbf", "")
  s = s.replace("{", "")
  s = s.replace("}", "")

  s = s.replace("\\'a", "&aacute;")
  s = s.replace("\\'e", "&eacute;")
  s = s.replace("\\'i", "&iacute;")
  s = s.replace("\\'o", "&oacute;")
  s = s.replace("\\'u", "&uacute;")
  s = s.replace("\\'y", "&yacute;")
  
  s = s.replace("\\`a", "&agrave;")
  s = s.replace("\\`e", "&egrave;")
  s = s.replace("\\`i", "&igrave;")
  s = s.replace("\\`o", "&ograve;")
  s = s.replace("\\`u", "&ugrave;")

  s = s.replace("\\~a", "&atilde;")
  s = s.replace("\\~i", "&itilde;")
  s = s.replace("\\~o", "&otilde;")
  s = s.replace("\\~u", "&utilde;")
  s = s.replace("\\~n", "&ntilde;")

  s = s.replace("\\^a", "&acirc;")
  s = s.replace("\\^e", "&ecirc;")
  s = s.replace("\\^i", "&icirc;")
  s = s.replace("\\^o", "&ocirc;")
  s = s.replace("\\^u", "&ucirc;")

  s = s.replace("\\c c", "&ccedil;")
  s = s.replace("\\v e", "&ecaron;")
  s = s.replace("\\v c", "&ccaron;")
  s = s.replace("\\v s", "&scaron;")

  s = s.replace('\\"a', "&auml;")
  s = s.replace('\\"e', "&euml;")
  s = s.replace('\\"i', "&iuml;")
  s = s.replace('\\"o', "&ouml;")
  s = s.replace('\\"u', "&uuml;")
  
  s = s.replace('~', " ")
  
  s = s.replace('\\v r', "&rcaron;")
  s = s.replace('\\v C', "&Ccaron;")
  s = s.replace('\\v s', "&scaron;")
  
  s = s.replace('\\&', "&amp;")

  return s
  


if len(sys.argv) == 4:
  bibfile = sys.argv[1]
  template = sys.argv[2]
  outfile = sys.argv[3]
else:
  print("Usage: python parse_bib.py <input_bibtex_file> <template_html_file> <output_html_file>")
  bibfile = input("Name of the input bibtex file (probably zotero.bib): ")
  template = input("Name of the template HTML file (probably template.html): ")
  outfile = input("Name of the desired output HTML file (probably ../index.html): ")

with open(bibfile, 'r') as bibtex_file:
  bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtex_file)

sorted_bib_html = []
years = []

with open("../refs.bib", "w") as newbib:
  texwriter = BibTexWriter()
  texwriter.indent = "\t"
  newbib.write(texwriter.write(bib_database))


with open(outfile, 'w') as new:
  with open(template, 'r') as templ:
    for line in templ:
      if "$CITATIONS" in line:
        break
      new.write(line)
  for bib in bib_database.entries:
    _id = bib['ID']  
    _title = bib["title"]
    try:
      _year = bib["year"]
    except:
      _year = "unknown year"
      print("YEAR EXCEPTION___"*100)
    if _year not in years:
      years.append(_year)
      years.sort()
    if "journal" in bib.keys():
      _pub = bib["journal"]
    elif "booktitle" in bib.keys():
      _pub = bib["booktitle"]
    elif "howpublished" in bib.keys():
      _pub = bib["howpublished"]
    elif "series" in bib.keys():
      _pub = bib["series"]
    else:
      _pub = "PUB EXCEPTION___"*100
    if "author" in bib.keys():
      _authors = bib["author"]
      autharr = _authors.split(" and ")
      fixedauth = []
      for author in autharr:
        if "," in author:
          namearr = author.split(", ")
          fname = namearr[1]
          lname = namearr[0]
        else:
          namearr = author.split(" ")
          fname = namearr[0]
          lname = namearr[1]
        fixedauth.append(str(fname) + " " + str(lname))
      _authors = ""
      if len(fixedauth) == 1:
        _authors = fixedauth[0]
      elif len(fixedauth) == 2:
        _authors = fixedauth[0] + " and " + fixedauth[1]
      else:
        for i in range(len(fixedauth)):
          if i == 0:
            _authors = _authors + fixedauth[i]
          elif i == len(fixedauth) - 1:
            _authors = _authors + ", and " + fixedauth[i]
          else:
            _authors = _authors + ", " + fixedauth[i]
    else:
      _authors = ""
    if "url" in bib.keys():
      _url = bib["url"]
      _url = '<a href="' + _url + '" target="_blank">View Paper&nbsp;<i class="fas fa-external-link-alt"></i></a>&nbsp;'
    elif "doi" in bib.keys():
      _url = "https://doi.org/" + bib["doi"]
      _url = '<a href="' + _url + '" target="_blank">View Paper&nbsp;<i class="fas fa-external-link-alt"></i></a>&nbsp;'
    else:
      _url = "&nbsp;&nbsp;Link Unavailable&nbsp;&nbsp;"
    _annotationLink = ""
    if "annotation" in bib.keys():
      _annotation = bib["annotation"]
      annotationSplit = _annotation.split(" ")
      for i in range(len(annotationSplit)-1):
        if "Artifact:" in annotationSplit[i]:
          artifactLink = annotationSplit[i+1]
          _annotationLink = '<a href="' + artifactLink + '" target="_blank">View Artifact&nbsp;<i class="fas fa-external-link-alt"></i></a>&nbsp;'
          _url = _url + "\n\t\t\t\t\t" + _annotationLink
          break
    _authors = fix_special(_authors)
    _pub = fix_special(_pub)
    _title = fix_special(_title)
    bib.pop("date-modified", None)
    bib.pop("date-added", None)
    bib.pop("keywords", None)

    db = BibDatabase()
    db.entries = [bib]
    texwriter = BibTexWriter()
    texwriter.indent = "\t"
    # newbib.write(texwriter.write(db))
    _tex = texwriter.write(db).replace("\n\n","").strip()
    # _tex = str(bib).replace("', ", "',\n\t\t\t\t\t\t").replace("}}", "}\n\t\t\t\t\t}")
    with open("parse.html", 'r') as orig:
      x = ""
      for line in orig:
        x = x + line.replace("$ID", _id).replace("$YEAR", _year).replace("$TITLE", _title).replace("$PUB", _pub).replace("$AUTHORS", _authors).replace("$URL", _url).replace("$TEX", _tex)
      this_bib = {}
      this_bib["year"] = int(_year)
      this_bib["key"] = _id
      this_bib["title"] = _title
      this_bib["html"] = x
      sorted_bib_html.append(this_bib)
    print("completed " + _id)
  # sorted_bib_html = sorted(sorted_bib_html, key=lambda k: k['key'].lower())
  sorted_bib_html = sorted(sorted_bib_html, key=lambda k: k['title'].lower())
  sorted_bib_html.reverse()
  sorted_bib_html = sorted(sorted_bib_html, key=lambda k: k['year'])
  sorted_bib_html.reverse()

  new.write('\t\t\t\t<p>\n')
  new.write('\t\t\t\t\tYou can <a href="refs.bib" download="refs.bib">download a BibTeX file</a> that contains references to all of these papers.\n')
  new.write('\t\t\t\t</p>\n\n')

  new.write('\t\t\t\t<p id="years">\n')
  years.reverse()
  print("Years: " + str(years))
  for yr in years:
    new.write('\t\t\t\t\t<a href="#' + str(yr) + '">' + str(yr) + '</a>\n')
  new.write("\t\t\t\t</p>\n\n")

  current_year = 0
  for item in sorted_bib_html: # I Reverse to get newest articles on top
    yr = item["year"]
    year = str(yr)
    if yr != current_year:
      current_year = yr
      new.write('\t\t\t\t<h3 id="' + year + '">' + year + '</h3><a href="#publications" class="pubtop"><i class="fas fa-chevron-up"></i></a>\n\n')
    new.write(item["html"] + "\n\n")
  
  with open(template, 'r') as templ:
    cango = False
    for line in templ:
      if cango:
        new.write(line)
      if "$CITATIONS" in line:
        cango = True    

