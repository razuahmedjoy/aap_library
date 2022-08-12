# from io import BytesIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa
# import datetime
# from django.http import HttpResponse
# from django.conf import settings

# def generate_pdf(orders):

#     # context = {'orders': orders}
#     # template = get_template("bookstore/partials/order_report.html")
#     # html = template.render(context)

#     # response = BytesIO()
#     # pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),response)
#     # filename = "order_report"

#     # try:
#     #     with open(str(settings.BASE_DIR) + f"/files/{filename}.pdf","wb+") as output:
#     #         pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),output)
#     #         print("done pdf")
#     #         print(pdf)
#     # except Exception as e:
#     #     print(e)
#     # print("done")
#     # if pdf.err:
#     #     return '',False

#     # return pdf
    
#     template_path = 'bookstore/partials/order_report.html'
#     context = {'orders': orders}
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')

#     filename = str(datetime.date.today())

#     response['Content-Disposition'] = f'inline; attachment; filename="{filename}.pdf"'
#     # response['Content-Disposition'] = 'filename="report.pdf"'

#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#        html, dest=response,encoding='UTF-8')
#     # if error then show some funny view
#     if pisa_status.err:
#        return HttpResponse('We had some errors <pre>' + html + '</pre>')
  
#     return response