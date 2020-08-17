from django.shortcuts import render

# Create your views here.
def export_excel(request):
    book = Workbook(encoding='utf8')
    sheet = book.add_sheet('members')

    alignment = xlwt.Alignment()
    alignment.horz = Alignment.HORZ_LEFT
    alignment.vert = Alignment.VERT_TOP
    style = XFStyle()
    style.alignment = alignment

    header_font = Font()
    header_font.name = 'Trebuchet MS'
    header_font.height = 240
    header_font.width = 100
    header_font.color = 'black'
    header_font.bold = True

    header_style = XFStyle()
    header_style.font = header_font

    data_font = Font()
    data_font.height = 220
    data_font.name = 'Trebuchet MS'
    data_font.color = 'gray80'
    data_font.borders = 'bottom 3'
    data_font.width = 220

    data_style = XFStyle()
    data_style.font = data_font


    header = ['First Name', 'Last Name', "Member's ID", 'Email', 'Title', 'Middle Name', 'Marital Status', 'Gender', 'DOB', 'Phone', 'Address', 'State of Residence' ]
    for hcol, hcol_data in enumerate(header):
        sheet.write(0, hcol, hcol_data, header_style)

    data = ([member.user.first_name, member.user.last_name, member.member_id_number, member.user.email,
            member.get_title_display(), member.middle_name, member.get_marital_status_display(),
            member.get_gender_display(), member.birth_date, member.phone, member.address, unicode(member.state_of_residence)]
    for member in Member.objects.all())
    for row, row_data in enumerate(data, start=1):  # start from row no.1
        for col, col_data in enumerate(row_data):
            sheet.write(row, col, col_data, data_style)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=members.xls'
    book.save(response)
    return response
