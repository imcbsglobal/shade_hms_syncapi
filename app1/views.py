from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from app1.models import HmsDoctors, HmsDoctorstiming, Misel


# ─────────────────────────────────────────────
# hms_doctors
# ─────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class DoctorsBulkView(View):
    def post(self, request):
        try:
            records = json.loads(request.body)
            for item in records:
                HmsDoctors.objects.update_or_create(code=item['code'], defaults=item)
            return JsonResponse({'synced': len(records)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DoctorsListView(View):

    def get(self, request):
        qs = HmsDoctors.objects.all()
        client_id = request.GET.get('client_id')
        if client_id:
            qs = qs.filter(client_id=client_id)
        doctors = list(qs.values(
            'code', 'name', 'rate', 'department', 'avgcontime', 'qualification', 'client_id'
        ))
        return JsonResponse(doctors, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            records = data if isinstance(data, list) else [data]
            created = []
            for item in records:
                obj, _ = HmsDoctors.objects.update_or_create(
                    code=item['code'],
                    defaults=item,
                )
                created.append(obj.code)
            return JsonResponse({'created': created}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorsDetailView(View):

    def get(self, request, code):
        try:
            qs = HmsDoctors.objects.filter(code=code)
            client_id = request.GET.get('client_id')
            if client_id:
                qs = qs.filter(client_id=client_id)
            doctor = qs.values(
                'code', 'name', 'rate', 'department', 'avgcontime', 'qualification', 'client_id'
            ).get()
            return JsonResponse(doctor)
        except HmsDoctors.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

    def post(self, request, code):
        try:
            data = json.loads(request.body)
            obj, _ = HmsDoctors.objects.update_or_create(code=code, defaults=data)
            return JsonResponse({'code': obj.code}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, code):
        try:
            data = json.loads(request.body)
            obj, _ = HmsDoctors.objects.update_or_create(code=code, defaults=data)
            return JsonResponse({'code': obj.code})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, code):
        try:
            client_id = request.GET.get('client_id')
            qs = HmsDoctors.objects.filter(code=code)
            if client_id:
                qs = qs.filter(client_id=client_id)
            qs.get().delete()
            return JsonResponse({'deleted': code})
        except HmsDoctors.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)


# ─────────────────────────────────────────────
# hms_doctorstiming
# ─────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class DoctorsTimingBulkView(View):
    def post(self, request):
        try:
            records = json.loads(request.body)
            for item in records:
                HmsDoctorstiming.objects.update_or_create(slno=item['slno'], defaults=item)
            return JsonResponse({'synced': len(records)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class DoctorsTimingListView(View):

    def get(self, request):
        qs = HmsDoctorstiming.objects.all()
        client_id = request.GET.get('client_id')
        if client_id:
            qs = qs.filter(client_id=client_id)
        timings = list(qs.values('slno', 'code', 'time1', 'time2', 'client_id'))
        for t in timings:
            t['slno']  = str(t['slno'])
            t['time1'] = str(t['time1']) if t['time1'] else None
            t['time2'] = str(t['time2']) if t['time2'] else None
        return JsonResponse(timings, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            records = data if isinstance(data, list) else [data]
            created = []
            for item in records:
                obj, _ = HmsDoctorstiming.objects.update_or_create(
                    slno=item['slno'],
                    defaults=item,
                )
                created.append(str(obj.slno))
            return JsonResponse({'created': created}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class DoctorsTimingDetailView(View):

    def get(self, request, slno):
        try:
            qs = HmsDoctorstiming.objects.filter(slno=slno)
            client_id = request.GET.get('client_id')
            if client_id:
                qs = qs.filter(client_id=client_id)
            timing = qs.values('slno', 'code', 'time1', 'time2', 'client_id').get()
            timing['slno']  = str(timing['slno'])
            timing['time1'] = str(timing['time1']) if timing['time1'] else None
            timing['time2'] = str(timing['time2']) if timing['time2'] else None
            return JsonResponse(timing)
        except HmsDoctorstiming.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

    def post(self, request, slno):
        try:
            data = json.loads(request.body)
            obj, _ = HmsDoctorstiming.objects.update_or_create(slno=slno, defaults=data)
            return JsonResponse({'slno': str(obj.slno)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, slno):
        try:
            data = json.loads(request.body)
            obj, _ = HmsDoctorstiming.objects.update_or_create(slno=slno, defaults=data)
            return JsonResponse({'slno': str(obj.slno)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, slno):
        try:
            client_id = request.GET.get('client_id')
            qs = HmsDoctorstiming.objects.filter(slno=slno)
            if client_id:
                qs = qs.filter(client_id=client_id)
            qs.get().delete()
            return JsonResponse({'deleted': str(slno)})
        except HmsDoctorstiming.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)


# ─────────────────────────────────────────────
# misel
# ─────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class MiselBulkView(View):
    def post(self, request):
        try:
            records = json.loads(request.body)
            records = records if isinstance(records, list) else [records]
            for item in records:
                Misel.objects.update_or_create(misel_primary=item['misel_primary'], defaults=item)
            return JsonResponse({'synced': len(records)}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class MiselListView(View):

    def get(self, request):
        try:
            # case-insensitive lookup for misel_primary
            qs = Misel.objects.filter(misel_primary__iexact='a')
            client_id = request.GET.get('client_id')
            if client_id:
                qs = qs.filter(client_id=client_id)
            misel = qs.values(
                'misel_primary', 'firm_name', 'address', 'mobile',
                'address1', 'address2', 'address3', 'tinno', 'client_id'
            ).get()
            return JsonResponse(misel)
        except Misel.DoesNotExist:
            return JsonResponse({})

    def post(self, request):
        try:
            data = json.loads(request.body)
            misel_primary = data.get('misel_primary', 'a')

            # Always update — no conflict check, client_id updates freely
            obj, _ = Misel.objects.update_or_create(
                misel_primary=misel_primary,
                defaults=data,
            )
            return JsonResponse({'misel_primary': obj.misel_primary}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MiselDetailView(View):

    def get(self, request, misel_primary):
        try:
            qs = Misel.objects.filter(misel_primary__iexact=misel_primary)
            client_id = request.GET.get('client_id')
            if client_id:
                qs = qs.filter(client_id=client_id)
            misel = qs.values(
                'misel_primary', 'firm_name', 'address', 'mobile',
                'address1', 'address2', 'address3', 'tinno', 'client_id'
            ).get()
            return JsonResponse(misel)
        except Misel.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

    def post(self, request, misel_primary):
        try:
            data = json.loads(request.body)
            obj, _ = Misel.objects.update_or_create(
                misel_primary=misel_primary,
                defaults=data,
            )
            return JsonResponse({'misel_primary': obj.misel_primary}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, misel_primary):
        try:
            data = json.loads(request.body)
            obj, _ = Misel.objects.update_or_create(
                misel_primary=misel_primary,
                defaults=data,
            )
            return JsonResponse({'misel_primary': obj.misel_primary})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, misel_primary):
        try:
            client_id = request.GET.get('client_id')
            qs = Misel.objects.filter(misel_primary__iexact=misel_primary)
            if client_id:
                qs = qs.filter(client_id=client_id)
            qs.get().delete()
            return JsonResponse({'deleted': misel_primary})
        except Misel.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)