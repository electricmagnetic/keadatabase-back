from django.contrib import admin

from .models import Band, BandCombo
from .forms import BandComboForm


class BandAdmin(admin.ModelAdmin):
    """ Defines the fieldsets for the Band model admin """
    fieldsets = [
        ('Band combo', {'fields':[
            'band_combo',
        ]}),
        ('Common', {'fields':[
            'primary', ('style', 'size'), 'identifier', ('colour', 'position', 'leg',),
        ]}),
        ('Letter (New)', {'fields':[
            ('symbol_colour', 'symbol',)
        ]}),
    ]

    list_display = ('__str__', 'band_type', 'primary', 'band_combo', 'get_bird_display',)
    list_filter = ('band_type', 'style', 'primary',)
    ordering = ('-band_combo', '-primary',)


class BandInline(admin.TabularInline):
    model = Band
    extra = 3


class BandComboAdmin(admin.ModelAdmin):
    """ Defines the fieldsets for the BandCombo model admin """
    form = BandComboForm
    inlines = [BandInline]

    #readonly_fields = ('__str__',)
    list_display = ('__str__', 'combo_type', 'area_location',)
    list_filter = ('combo_type', 'area_location',)


admin.site.register(Band, BandAdmin)
admin.site.register(BandCombo, BandComboAdmin)
