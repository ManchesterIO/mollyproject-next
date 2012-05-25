from django.contrib.gis.db import models

from tch.common.models import Identifier, Notice, Organisation, Source, FetchableByIdentifier

class FetchableBySource():
    
    def get_by_source_id(self, source_url, source_file, source_id):
        return self.select_related(depth=1).get(sources__source_url=source_url,
                                                sources__source_file=source_file,
                                                sources__source_id=source_id)
    
    def get_by_source(self, source):
        return self.select_related(depth=1).get(sources=source)


class SlugCachingManager():
    
    def get_by_slug(self, slug):
        if not hasattr(self, '_cache'):
            self._cache = {}
        
        if slug not in self._cache:
            self._cache[slug] = self.get(slug=slug)
        return self._cache[slug]


class LocalityManager(models.GeoManager, FetchableBySource, FetchableByIdentifier):
    pass


class Locality(models.Model):
    """
    A locality is an area or region which stops or interchanges belong to,
    and which users may want to travel to.
    """
    
    centre = models.PointField(help_text="The centre of this locality",
                               null=True)
    area = models.PolygonField(help_text="The area which this locality covers",
                               null=True)
    parent = models.ForeignKey("self", null=True)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)
    
    objects = LocalityManager()
    
    def __unicode__(self):
        return self.slug


class FacilityTypeManager(SlugCachingManager, models.Manager):
    pass


class FacilityType(models.Model):
    """
    A type of facility is something which a stop may have, such as a ticket
    office, or toilets, etc
    """
    
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    
    slug = models.SlugField(unique=True)
    sources = models.ManyToManyField(Source)
    
    objects = FacilityTypeManager()


class Facility(models.Model):
    """
    A facility is something a stop may have, including details specific to that
    stop.
    
    To do: Capture requirements like opening times, specific locations, etc
    """
    
    location = models.PointField(help_text="The location of this facility")
    
    type = models.ForeignKey(FacilityType)
    notices = models.ManyToManyField(Notice)
    
    slug = models.SlugField(unique=True)
    sources = models.ManyToManyField(Source)
    objects = models.GeoManager()


class TypeManager(SlugCachingManager, models.Manager):
    
    def get_or_create(self, slug, type):
        try:
            return self.get_by_slug(slug), False
        except Type.DoesNotExist:
            self._cache[slug] = self.create(slug=slug, type=type)
            return self.get_by_slug(slug), True


class Type(models.Model):
    """
    A type indicates what type of stop this is
    """
    
    type = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    
    objects = TypeManager()


class InterchangeManager(models.GeoManager, FetchableBySource):
    pass


class Interchange(models.Model):
    """
    An interchange is a collection of stops where users can reasonably transfer
    from one point to another by foot - it may be a bus station, a collection
    of stops in one location, or a collection of platforms at a tram station.
    """
    
    centre = models.PointField(help_text="The centre of this interchange",
                               null=True)
    area = models.PolygonField(
        help_text="The area which this interchange covers", null=True)
    
    administrator = models.ForeignKey(Organisation, null=True,
        related_name="administered_interchanges")
    operator = models.ForeignKey(Organisation, null=True,
        related_name="operated_interchanges")
    
    notices = models.ManyToManyField(Notice)
    
    type = models.ForeignKey(Type)
    facilities = models.ManyToManyField(Facility)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)

    objects = InterchangeManager()


class StopManager(models.GeoManager, FetchableBySource):
    pass


class Stop(models.Model):
    """
    This is a stop, or a station, or a port, or some other logical place where
    public transport services call. This may consist of multiple physical places
    where services call (such as platforms), but is always considered by a PT
    user to be one discrete location. Stops are single-modal (modal transfers
    take place at interchanges). Bus stations are typically modelled as
    interchanges, rather than one Stop with multiple Platforms. If a stop has
    no platforms, then it is considered to be a simple stop and is a physical
    as well as logical artefact.
    """
    
    location = models.PointField(help_text="The location of this stop", null=True)
    
    type = models.ForeignKey(Type)
    facilities = models.ManyToManyField(Facility)
    
    primary_locality = models.ForeignKey(Locality, related_name="+", null=True)
    localities = models.ManyToManyField(Locality)
    interchanges = models.ManyToManyField(Interchange)
    
    administrator = models.ForeignKey(Organisation, null=True,
        related_name="administered_stops")
    operator = models.ForeignKey(Organisation, null=True,
        related_name="operated_stops")
    
    notices = models.ManyToManyField(Notice)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)

    objects = StopManager()


class CallingPointManager(models.GeoManager, FetchableBySource):
    pass


class CallingPoint(models.Model):
    """
    This is a platform, or berth, or similar, 'sub-stop' within a stop
    """
    
    location = models.PointField(help_text="The location of this platform",
                                 null=True)
    
    stop = models.ForeignKey(Stop, null=True)
    
    type = models.ForeignKey(Type)
    facilities = models.ManyToManyField(Facility)
    notices = models.ManyToManyField(Notice)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)

    objects = CallingPointManager()
