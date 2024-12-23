from django_components import component

@component.register("card")
class Card(component.Component):
    template_name = "card/template.html"

    def get_context_data(self, title):
        return {
            "title": title
        }
    
    # class Media:
    #     # css = 'card/style.css'
    #     # js = 'card/script.js'