import datetime

from django.db import models
from pygments import highlight
from pygments.lexers import *
from pygments.formatters import HtmlFormatter
from tagging.fields import TagField

# Create your models here.
class Language(models.Model):
  """ Defines a programming language """
  name                = models.CharField(max_length=200)
  slug                = models.SlugField()
  lexer               = models.CharField(max_length=200, blank=True, help_text='For best results, set the lexer equal to the short name of a <a href="http://pygments.org/docs/lexers/">Pygments lexer</a>.')

  def __unicode__(self):
    return self.name

class CodeSample(models.Model):
  """ Defines a snippet of code """
  title               = models.CharField(max_length=200)
  slug                = models.SlugField()
  description         = models.TextField(blank=True)
  code                = models.TextField()
  code_highlighted    = models.TextField(blank=True, editable=False)
  code_indented       = models.TextField(blank=True, editable=False)
  language            = models.ForeignKey(Language)
  
  date_published      = models.DateTimeField(help_text="Select the date and time this entry was posted.", default=datetime.datetime.now)
  date_created        = models.DateTimeField(editable=False, default=datetime.datetime.now)
  
  # Categorization
  tags                = TagField(help_text="Add tags for this code sample (space separated).")

  def __unicode__(self):
    return self.title
      
  def save(self, force_insert=False, force_update=False):
    """
    Runs the code sample thorough Pygments syntax highlighting, then saves it.
    """
    import StringIO
    code_lines = lines = self.code.split('\n')
    code_block = StringIO.StringIO()
    code_block.write('\n\n')
    for line in code_lines:
      code_block.write('')
      code_block.write(line)
      code_block.write('\n')
    code_block.write('\n\n')
    # Try to get the lexer by slug; if it can't be found, guess it.
    try:
      lexer = get_lexer_by_name(str(self.language.lexer), stripall=True)
    except:
      lexer = guess_lexer(self.code)
    self.code_indented = code_block.getvalue()
    self.code_highlighted = highlight(self.code, lexer, HtmlFormatter(nowrap=True))
    self.code_highlighted = '\n' + self.code_highlighted + '\n'
    
    super(CodeSample, self).save(force_insert=force_insert, force_update=force_update)
    
  class Meta:
    unique_together = (("language", "slug"),)
