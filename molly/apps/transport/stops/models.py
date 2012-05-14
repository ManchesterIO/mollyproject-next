from django.contrib.gis.db import models

from tch.common.models import Identifier, Notice, Organisation, Source

class LocalityManager(models.GeoManager):
    
    def get_by_source_id(self, source_url, source_file, source_id):
        return self.select_related(depth=1).get(sources__source_url=source_url,
                                                sources__source_file=source_file,
                                                sources__source_id=source_id)


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
    

class FacilityType(models.Model):
    """
    A type of facility is something which a stop may have, such as a ticket
    office, or toilets, etc
    """
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    slug = models.SlugField(unique=True)
    sources = models.ManyToManyField(Source)


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


class Type(models.Model):
    """
    A type indicates what type of stop this is
    """
    
    type = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Interchange(models.Model):
    """
    An interchange is a collection of stops where users can reasonably transfer
    from one point to another by foot - it may be a bus station, a collection
    of stops in one location, or a collection of platforms at a tram station.
    """
    
    centre = models.PointField(help_text="The centre of this interchange")
    area = models.PolygonField(help_text="The area which this interchange covers")
    
    administrator = models.ForeignKey(Organisation,
        related_name="administered_interchanges")
    operator = models.ForeignKey(Organisation,
        related_name="operated_interchanges")
    
    notices = models.ManyToManyField(Notice)
    
    type = models.ForeignKey(Type)
    facilities = models.ManyToManyField(Facility)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)

    objects = models.GeoManager()


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
    
    location = models.PointField(help_text="The location of this stop")
    
    common_name = models.CharField(max_length=200, help_text="""
        The human readable identifier for this stop""")
    
    identifier = models.CharField(max_length=200, null=True, blank=True,
        help_text="""An identifier which can help differentiate a stop in a
        group of stops (e.g., Stop A6 or 'Towards Manchester')""")
    
    type = models.ForeignKey(Type)
    facilities = models.ManyToManyField(Facility)
    
    primary_locality = models.ForeignKey(Locality, related_name="+")
    localities = models.ManyToManyField(Locality)
    interchanges = models.ManyToManyField(Interchange)
    
    administrator = models.ForeignKey(Organisation,
        related_name="administered_stops")
    operator = models.ForeignKey(Organisation,
        related_name="operated_stops")
    
    notices = models.ManyToManyField(Notice)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)

    objects = models.GeoManager()


class Platform(models.Model):
    """
    This is a platform, or berth, or similar, 'sub-stop' within a stop
    """
    
    location = models.PointField(help_text="The location of this platform")
    
    common_name = models.CharField(max_length=200,
        help_text="The human readable identifier for this stop")
    
    stop = models.ForeignKey(Stop)
    
    type = models.ForeignKey(Type)
    facilities = models.ManyToManyField(Facility)
    notices = models.ManyToManyField(Notice)
    
    slug = models.SlugField(unique=True)
    identifiers = models.ManyToManyField(Identifier)
    sources = models.ManyToManyField(Source)

    objects = models.GeoManager()
