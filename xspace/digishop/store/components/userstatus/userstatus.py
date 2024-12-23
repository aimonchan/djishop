from django_components import component

@component.register("userstatus")
class Userstatus(component.Component):
    template_name = "userstatus/template.html"

    # def get_context_data(self, title):
    #     return {
    #         "title": title
    #     }
    
    # class Media:
    #     # css = 'card/style.css'
        # js = ('userstatus/script.js',)