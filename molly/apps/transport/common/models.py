from django.db import models

class Source(models.Model):
    """
    A source is used to denote the origin of a piece of information.
    
    Some artefacts can have multiple sources, e.g., a route which crosses
    county borders may exist in both PTEs data feeds.
    """
    
    source_url = models.CharField(max_length=128, help_text="""
        This field holds the URL of the file or archive which yielded this
        artefact""")
    
    source_file = models.CharField(max_length=128, null=True, help_text="""
        Some data sources consist of multiple files in an archive, this field
        identifies which file in the archive yielded this artefact""")
    
    source_id = models.CharField(max_length=128, help_text="""
        This uniquely identifies a particular datum within the source URL. Note
        that this could yield multiple artefacts.""")
    
    source_version = models.CharField(max_length=22, help_text="""
        The version (or datetime) of the source which yielded this artefact""")


class Notice(models.Model):
    """
    A notice relating to a stop or journey
    """

    text = models.TextField()
    
    valid_from = models.DateTimeField(null=True, blank=True,
        help_text="The date/time from which this notice applies")
    
    valid_to = models.DateTimeField(null=True, blank=True,
        help_text="The date/time which this notices expires")
    
    slug = models.SlugField(unique=True)
    source = models.ForeignKey(Source)
    
    # TODO: Notice type, e.g., disruption, general information, etc


class Identifier(models.Model):
    """
    An identifier is something which identifies a stop within a system. It
    could be a system-wide code like NaPTAN, or a human-readable identifier
    """
    
    NAMESPACES = (
        'human', # The human-readable name of this stop
        'atco',
        'naptan',
    )
    
    namespace = models.CharField(max_length=50,
        choices=zip(NAMESPACES, NAMESPACES),
        help_text="The namespace of this identifier")
    
    value = models.CharField(max_length=200)
    
    language = models.TextField(max_length=8, null=True, blank=True,
        help_text="""For human readable namespaces, some stops have different
        names in different languages, this can be used to indicate which
        language this identifier is in.""")
    
    def __unicode__(self):
        if self.language != None:
            return self.namespace + '(' + self.language + '): ' + self.value
        else:
            return self.namespace + ': ' + self.value


class Organisation(models.Model):
    
    TYPES = (
        'administrator',
        'operator',
    )
    
    type = models.CharField(max_length=50, choices=zip(TYPES, TYPES),
        help_text="What type of organisation this is (e.g., PTE, operator)")
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    source = models.ForeignKey(Source)
    
