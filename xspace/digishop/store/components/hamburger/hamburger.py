from django_components import component

@component.register("hamburger")
class Hamburger(component.Component):
    template_name = "hamburger/template.html"

    # def get_context_data(self, title):
    #     return {
    #         "title": title
    #     }
    
    # class Media:
    #     # css = 'card/style.css'
    #     # js = 'card/script.js'