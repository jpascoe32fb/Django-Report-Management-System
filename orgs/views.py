from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.graphics.shapes import Rect
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO

from .models import *

#for safely returning instances from a model even if none exist | use model.objects.get for single instances
#ie. if a unit doesn't have any reports yet
#ex: reports = safe_get(Report, unit=unit)
def safe_get(model, **kwargs):
    try:
        return model.objects.filter(**kwargs)
    except model.DoesNotExist:
        return None

def get_unit_tree_data(request):
    units = Unit.objects.all()
    unit_data = []
    processed_names = set()
    processed_functions = set()
    processed_assets = set()
    processed_components = set()
    processed_plant_tags = set()

    for unit in units:
        if unit.name not in processed_names:
            processed_names.add(unit.name)
            name_units = Unit.objects.filter(name=unit.name)
            function_data = []
            processed_functions = set()
            for name_unit in name_units:
                if name_unit.function not in processed_functions:
                    processed_functions.add(name_unit.function)
                    function_units = Unit.objects.filter(name=unit.name, function=name_unit.function)
                    asset_data = []
                    processed_assets = set()
                    for function_unit in function_units:
                        if function_unit.asset not in processed_assets:
                            processed_assets.add(function_unit.asset)
                            asset_units = Unit.objects.filter(name=unit.name, function=name_unit.function, asset=function_unit.asset)
                            component_data = []
                            processed_components = set()
                            for asset_unit in asset_units:
                                if asset_unit.component not in processed_components:
                                    processed_components.add(asset_unit.component)
                                    component_units = Unit.objects.filter(name=unit.name, function=name_unit.function, asset=function_unit.asset, component=asset_unit.component)
                                    plant_tag_data = []
                                    processed_plant_tags = set()
                                    for component_unit in component_units:
                                        if component_unit.plant_tag not in processed_plant_tags:
                                            processed_plant_tags.add(component_unit.plant_tag)
                                            #plant_tag_data.append({'name': component_unit.plant_tag.name, 'text': component_unit.plant_tag.name})
                                    component_data.append({'name': asset_unit.component.name, 'children': plant_tag_data, 'text': asset_unit.component.name, 'id': asset_unit.id})
                            asset_data.append({'name': function_unit.asset.name, 'children': component_data, 'text': function_unit.asset.name})
                    function_data.append({'name': name_unit.function.name, 'children': asset_data, 'text': name_unit.function.name})
            unit_data.append({'name': unit.name.name, 'children': function_data, 'text': unit.name.name})

    return JsonResponse(unit_data, safe=False)


def home(request):
    units = Unit.objects.all()
    tree = []
    reports = Report.objects.all()

    #GetReports function ??
    #Report.objects.filter(name="PUREPOWER",component="switch") for example to get the distinct reports
    #create view function or template function that is called when querying specific reports in the html ->
    #   goes to separate form that loads the reports for main dashboard 

    context = {'units':units, 'reports':reports, 'tree':tree}
    return render(request, 'orgs/dashboard.html', context)

def about(request):
    return render(request, 'orgs/about.html')

def generate_pdf(request, report_ids):
    report_ids = report_ids.split(',')
    reports = Report.objects.filter(id__in=report_ids)

    PAGE_WIDTH, PAGE_HEIGHT = letter

    # Create a new PDF object
    response = HttpResponse(content_type='application/pdf')
    fname = str(reports.first())
    response['Content-Disposition'] = 'attachment; filename=' + fname + '.pdf'
    #Might change ^ and get rid of attachment
    
    # Create a canvas object with the response object
    p = canvas.Canvas(response)
    
    #Page 1
    # Add logo to the center of the page
    p.drawImage('./static/img/logo.PNG', x=130, y=550, width=None, height=None)
    p.setFont(psfontname='Helvetica', size=18)
    p.drawString(x=130, y=425, text="Condition Assessment Assignment Report")

    
    #Page 2
    # Add general statistics to the next page
    p.showPage()
    p.drawString(x=0, y=0, text="General Statistics")
    sev_buffer = BytesIO()
    severeties = [report.condition.severity for report in reports]
    severity_counts = Counter(severeties)
    # Create pie chart
    sev_labels = severity_counts.keys()
    sev_counts = severity_counts.values()
    plt.pie(sev_counts, labels=sev_labels, autopct='%1.1f%%', radius=0.8)
    plt.title('Condition Entry Summary')
    plt.savefig(sev_buffer, format='png')
    sev_buffer.seek(0)
    sev_pie = ImageReader(sev_buffer)
    p.drawImage(sev_pie, x=2, y=420, width=420, height=350)

    #Page 3
    #Condition Entry Tables Summary
    p.showPage()
    p.setFont(psfontname='Helvetica', size=15)
    p.drawString(x=15, y=805, text="Condition Entry Summary")
    col_widths = [90, 125, 105, 125, 115]
    scale_factor = 1.0
    col_widths_scaled = [width * scale_factor for width in col_widths]
    entry_data = [['Level', 'Unit', 'Function', 'Asset', 'Component']]
    for report in reports:
        row = [report.condition.severity.name, report.unit.name.name, report.unit.function.name, report.unit.asset.name, report.unit.component.name]
        entry_data.append(row)
    entry_tables = Table(entry_data, colWidths=col_widths_scaled)
    table_style = TableStyle([
    # Set the background color of the header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),

    # Set the font size and alignment of the header row
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

    # Set the font size of the data rows
    ('FONTSIZE', (0, 1), (-1, -1), 12),

    # Set the alternating background color of the data rows
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('BACKGROUND', (0, 1), (-1, -2), colors.white),

    #Grid
    ('GRID', (0,0), (-1, -1), 1, colors.black),

    #Grid Padding
    ('TOPPADDING', (0, 1), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ])
    entry_tables.setStyle(table_style)
    entry_tables.wrapOn(p, PAGE_WIDTH, PAGE_HEIGHT)
    entry_tables.wrap(0,0)
    entry_tables.drawOn(p, 10, 760)
    
    #Page 4+ Condition Entry Details
    # Loop through the modal data and add information to the PDF
    # *** May need to limit size of text to put in each ***
    for i, report in enumerate(reports):
        p.showPage()
        #titles
        p.setFont(psfontname='Helvetica', size=14)
        p.drawString(x=45, y=795, text="Condition Entry Details")
        p.drawString(x=330, y=795, text="Severity: " + report.condition.severity.name)
        p.setFont(psfontname='Helvetica-Bold', size=11)
        p.drawString(x=30, y=650, text="Faults")
        p.drawString(x=30, y=580, text="Comments")
        p.drawString(x=30, y=480, text="Recommendations")
        #Rectangle 1, Fault, Comment, Recommend
        p.setFillColorRGB(0.5, 0.5, 0.5, alpha=0.1)
            #1
        p.rect(x=30, y=675, width=530, height=95, fill=True)
            #Fault
        p.rect(x=30, y=605, width=530, height=40, fill=True)
            #Comment
        p.rect(x=30, y=505, width=530, height=70, fill=True)
            #Recommendation
        p.rect(x=30, y=415, width=530, height=60, fill=True)
        #Rect 1 Text
        p.setFillColor(colors.black)
        p.setFont(psfontname='Helvetica', size=10)
        p.drawString(x=70, y=750, text="Unit:  " + report.unit.name.name)
        p.drawString(x=50, y=735, text="Function:  " + report.unit.function.name)
        p.drawString(x=62, y=720, text="Asset:  " + report.unit.asset.name)
        p.drawString(x=45, y=705, text="Component:  " + report.unit.component.name)
        p.drawString(x=50, y=690, text="Plant Tag:  None")
        #Fault Text
            #p.drawString(x=31, y=625, text=report.fault)
        text = report.fault + " :test test test test test test test test test test"
        if len(text) > 125:
            text = text[:120] + '\n' + text[120:]
            #if len(text) > 250: delete after 250 so it doesn't overrun the box
        t_string = p.beginText(x=31, y=635)
        t_string.setFont("Helvetica", 10)
        t_string.setLeading(14)
        lines = text.split("\n", maxsplit=1)
        for line in lines: # maybe change this to only do 2 lines
            t_string.textLine(line)
        p.drawText(t_string)
        #Comment Text
        text = report.comment + " :test test test test test test test test test test test test test test test test test test test test test test test test test"
        if len(text) > 125:
            text = text[:120] + '\n' + text[120:]
            #if len(text) > 250: delete after 250 so it doesn't overrun the box
        t_string = p.beginText(x=31, y=565)
        t_string.setFont("Helvetica", 10)
        t_string.setLeading(17)
        lines = text.split("\n", maxsplit=1)
        for line in lines: # maybe change this to only do 2 lines
            t_string.textLine(line)
        p.drawText(t_string)
        #Recommend Text
        text = report.recommendation + " :test test test test test test test test test test test test test test test test test test test test test test test test"
        if len(text) > 125:
            text = text[:120] + '\n' + text[120:]
            #if len(text) > 250: delete after 250 so it doesn't overrun the box
        t_string = p.beginText(x=31, y=465)
        t_string.setFont("Helvetica", 10)
        t_string.setLeading(14)
        lines = text.split("\n", maxsplit=1)
        for line in lines: # maybe change this to only do 2 lines
            t_string.textLine(line)
        p.drawText(t_string)

    
    # Save the PDF and return it as a response
    p.save()
    return response

def detailed_condition(request, report_id):
    report = Report.objects.get(id=report_id)

    context = {'report': report}
    return render(request, 'orgs/detailed_condition.html', context)

def company_view(request):
    return

def function_view(request):
    return

def asset_view(request):
    return

def component_view(request):
    return

def unit(request, node_id):
    if request.method == 'POST':
        techID = request.POST['technology']
        analystID = request.POST['analysts']
        sevID = request.POST['severity']
        entry = request.POST['entryDate']
        req = request.POST['workReq']
        order = request.POST['workOrder']
        fault = request.POST['faults']
        rec = request.POST['recommendations']
        comm = request.POST['comments']

        if Technology.objects.filter(name=techID).exists():
            tech = Technology.objects.get(name=techID)
        else:
            tech = Technology(name=techID)
            #tech.save()
        if Analyst.objects.filter(name=analystID).exists():
            anal = Analyst.objects.get(name=analystID)
        else:
            anal = Analyst(name=analystID)
            #anal.save()
        #if Severity.objects.filter(name=sevID).exists():
            #sev = Severity.objects.get(name=sevID)
        #else:
            #sev = Severity(name=sevID)
            #tech.save()
        cond = Condition(severityLevel=sevID, technology=tech, analyst=anal, entry_date=entry, work_req=req, work_order=order)
        cond.save()
        unitObj = Unit.objects.get(id=node_id)
        new_report = Report(condition=cond, unit=unitObj, fault=fault, comment=comm, recommendation=rec)
        new_report.save()

        return redirect(reverse('unit', args=[node_id]))

    unit = Unit.objects.get(id=node_id)
    reports = safe_get(Report, unit=unit)
    severities = {'GOOD','MISSED','LOW', 'MEDIUM','HIGH','MED-HIGH'}
    technology = Technology.objects.all()
    analysts = Analyst.objects.all()
    #severity = Severity.objects.all()

    pie_data = [report.condition.severityLevel for report in reports]
    pie_data = Counter(pie_data)
    severity_labels = []
    severity_data = []
    for data in pie_data:
        severity_labels.append(data)
        temp = pie_data[data]
        severity_data.append(temp)

    context = {'unit': unit, 'reports': reports, 'severities': severities, 'technology': technology, 'analysts': analysts, 'severity_data': severity_data, 'severity_labels': severity_labels}
    return render(request, 'orgs/unit.html', context)



def create_report(request, node_id):
    context = {}
    return render(request, 'orgs/unit.html', context)

def report(request):
    return render(request, 'orgs/report.html')
