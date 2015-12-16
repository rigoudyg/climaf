cpdfcrop : crop pdf figures to their minimal size by preserving metadata
-------------------------------------------------------------------------

Remove empty margins, i.e. white extra space, of an input PDF figure
and also update metadata. The resulting output figure occupies the
minimal paper size needed for the content and is therefore suitable
for inclusion as a graphic. 

**References** : http://manpages.ubuntu.com/manpages/precise/man1/pdfcrop.1.html

**Provider / contact** : climaf at meteo dot fr

**Inputs** : any figure object (but only one)

**Mandatory arguments**: none

**Optional arguments**:
  - none

**Output** :

**Climaf call example**::
 
  >>> cdef("frequency","monthly")
  >>> cdef("period","198001")
  >>> tas=ds(project="example", simulation="AMIPV6ALB2G", variable="tas") 
  >>> fig=plot(tas,title="title",format="pdf")
  >>> cshow(fig)
  >>> cropped_fig=cpdfcrop(fig) # some figure object
  >>> cshow(cropped_fig)

**Side effects** : none

**Implementation** : standard 'pdfcrop' utility to remove empty
margins and standard 'pdftk' utility to preserve metadata

