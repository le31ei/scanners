from django.shortcuts import render, HttpResponse, get_object_or_404, Http404
from django.views.generic import View, ListView, DetailView
from django.http import JsonResponse
from .forms import addItemForm
from .models import ScanItems, IPResult, PortResult
from scanclient.scantasks import start_scan

import ipaddress
import xlwt
from io import StringIO, BytesIO


# Create your views here.
class IndexView(View):
    """
    首页
    """
    def get(self, request):
        return render(request, 'dashboard.html')


class DashboardView(View):
    def get(self, request):
        return HttpResponse('123')


class ScanListView(ListView):
    template_name = 'scanners/list_scan.html'
    paginate_by = 10
    model = ScanItems
    context_object_name = 'scanitems'


class DetailListView(ListView):
    template_name = 'scanners/detail_scan.html'
    context_object_name = 'details'

    def get_queryset(self):
        self.scanitem = get_object_or_404(ScanItems, itemid=self.kwargs['uuid'])
        self.ipresult = IPResult.objects.get(scannitem=self.scanitem)
        return get_object_or_404(PortResult, ip=self.ipresult)


class AddScanView(View):
    def get(self, request):
        return render(request, 'scanners/add_scan.html')

    def post(self, request):
        add_form = addItemForm(request.POST)
        if add_form.is_valid():
            itemname = request.POST.get('itemname')
            ips = request.POST.get('ip')
            try:
                ipaddress.ip_network(ips, strict=False)
                scanitem = ScanItems(scanIP=ips, scanname=itemname)  #TODO：取多个重复值
                scanitem.save()
                start_scan.delay(scanitem.itemid)
                # return render(request, 'scanners/add_scan.html', {'msg': True})
                return JsonResponse({'msg': '提交成功', 'code': '1'})
            except Exception as e:
                print(e)
                return JsonResponse({'msg': '请输入正确的IP地址'})
        else:
            return JsonResponse({'msg': '请输入正确的数值'})


class ExportExcelView(View):
    """
    获取uuid参数，
    """
    def get(self, request, uuid):
        ws = self.export_excel(uuid)
        output = BytesIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=result.xls'
        response.write(output.getvalue())
        return response

    def export_excel(self, uuid):
        scanitem = ScanItems.objects.get(itemid=uuid)
        ipresult = IPResult.objects.filter(scannitem=scanitem)
        if ipresult.exists():
            ws = xlwt.Workbook(encoding='utf-8')
            sheet = ws.add_sheet('port列表')
            sheet.write(0, 0, 'IP')
            sheet.write(0, 1, '端口')
            sheet.write(0, 2, '服务')
            sheet.write(0, 3, 'title')
            row = 1
            for ip in ipresult:
                portresult = PortResult.objects.filter(ip=ip)
                print(portresult)
                if portresult.exists():
                    for port in portresult:
                        sheet.write(row, 0, ip.ip)
                        sheet.write(row, 1, port.port)
                        sheet.write(row, 2, port.service)
                        sheet.write(row, 3, port.title)
                        row = row + 1
                else:
                    continue
            return ws

        else:
            raise Http404()

