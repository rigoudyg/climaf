cepscrop : crop eps figures to their minimal size 
---------------------------------------------------

Remove empty margins, i.e. extra white space, of an input EPS
figure. The resulting output figure has the minimal size
needed for the content and is therefore suitable for inclusion as a
graphic. 

**References** :

- http://manpages.ubuntu.com/manpages/jaunty/man1/epstopdf.1.html ; 
- http://manpages.ubuntu.com/manpages/precise/man1/pdfcrop.1.html ;
- http://manpages.ubuntu.com/manpages/hardy/man1/pdftops.1.html

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any figure object (but only one)

**Mandatory arguments**: none

**Optional arguments**:
  - none

**Output** : the EPS cropped figure

**Climaf call example**::
 
  >>> cdef("frequency","monthly")
  >>> cdef("period","198001")
  >>> tas=ds(project="example", simulation="AMIPV6ALB2G", variable="tas") 
  >>> fig=plot(tas,title="title",format="eps")
  >>> cshow(fig)
  >>> cropped_fig=cepscrop(fig) # some figure object
  >>> cshow(cropped_fig)

**Side effects** : none

**Implementation** : This script first converts 'eps' figure in 'pdf'
figure using 'epstopdf', then crops extra white space using 'pdfcrop'
and finally converts this cropped 'pdf' figure in 'eps' file using
'pdftops'
