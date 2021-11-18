from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import path
from django.shortcuts import redirect, render
from .forms import CsvImportForm, RESTApiImportForm
from elections.models import Election, Nomination

# Register your models here. 
  
class NominationAdmin(admin.ModelAdmin): 
    change_list_template = "custom_admin/change_list.html"
 
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
     
            path('import_csv/', self.import_csv),
            path('import_from_url/', self.import_from_rest_api)
        ]
        return my_urls + urls
         
    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                except ValidationError as e:
                    messages.error(request, message='\n'.join(e.messages))
                    return redirect("..")
                messages.success(request, "Your csv file has been imported")
                return redirect("..")
 
        form = CsvImportForm()
        payload = {"form": form}
         
        return render(request, "custom_admin/csv_form.html", payload)

    def import_from_rest_api(self, request):
        form = RESTApiImportForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except ValidationError as e:
                messages.error(request, message='\n'.join(e.messages))
                return redirect("..")
            messages.success(request, "Data has been imported successfully!")
            return redirect("..")

        form = RESTApiImportForm()
        payload = {"form": form}
        return render(request, "custom_admin/rest_api_form.html", payload)


admin.site.register(Election)
admin.site.register(Nomination, NominationAdmin)
