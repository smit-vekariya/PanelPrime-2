from django.shortcuts import render
from account.serializers import BondUserListSerializers
from qradmin.serializers import QRBatchSerializers, QRCodeSerializers, QRBatchListSerializers, QRCodeListSerializers
from account.models import BondUser
from manager.manager import HttpsAppResponse, Util
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from qradmin.models import QRBatch, QRCode
from django.conf import settings
from django.db import transaction
from manager import manager
from rest_framework import filters
import logging
from rest_framework.pagination import PageNumberPagination
from django.db.models import Case, Count, F, Q ,When, IntegerField ,CharField
from django.db.models.functions import Cast
from qrapp.models import BondUserWallet, Transaction
from qrapp.serializers import TransactionSerializers, UserWalletReportListSerializers
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse



# Create your views here.
class CompanyDashboard(viewsets.ViewSet):
    queryset  = QRCode.objects.all()
    user_queryset = BondUser.objects.all()

    def list(self, request):
        try:
            total_bond_user = self.user_queryset.count()
            dashboard = self.queryset.aggregate(
                total_qr_code = Count(F('id')),
                total_qr_batch = Count(F('batch'), distinct=True),
                total_used_qr = Count(Case(When(is_used=True, then=1),output_field=IntegerField())),
                total_remain_qr = Count(Case(When(is_used=False, then=1),output_field=IntegerField()))
            )
            used_in_percentage = (dashboard["total_used_qr"]) * 100 / dashboard["total_qr_code"]
            dashboard.update({"used_in_percentage":round(used_in_percentage,2)})
            dashboard.update({"total_bond_user":total_bond_user})
            return HttpsAppResponse.send(dashboard, 0, "Dashboard data get successfully")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param= "page_size"
    max_page_size = 1000

class UserList(generics.ListAPIView):
    queryset = BondUser.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    serializer_class = BondUserListSerializers
    search_fields =["full_name", "mobile"]
    pagination_class = CustomPagination


class QRBatchList(generics.ListAPIView):
    queryset = QRBatch.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    search_fields =["batch_number"]
    serializer_class = QRBatchListSerializers
    pagination_class = CustomPagination

class QRCodeList(generics.ListAPIView):
    queryset = QRCode.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    serializer_class = QRCodeListSerializers
    search_fields =["qr_number", "batch__batch_number"]
    pagination_class = CustomPagination

    def get_queryset(self):
        is_used = self.request.GET["is_used"]
        if is_used:
            queryset = self.queryset.filter(is_used=is_used)
            return queryset
        return super().get_queryset()


class CreateQRBatch(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data
                total_qr_code = data.get("total_qr_code")
                point_per_qr = data.get("point_per_qr")
                if point_per_qr > 0 and total_qr_code > 0:
                    batch_number = QRBatch.objects.values("batch_number").last()
                    batch_number = "BATCH-10000" if not batch_number else f"BATCH-{int(batch_number['batch_number'].split('-')[1])+1}"
                    point_per_amount = data.get("point_per_amount")
                    total_point = data.get("total_point")
                    total_amount = data.get("total_amount")
                    amount_per_qr = data.get("amount_per_qr")

                    batch_data={"batch_number":batch_number,"total_qr_code":total_qr_code,"total_amount":total_amount,
                                "point_per_amount":point_per_amount,"total_point":total_point,"point_per_qr":point_per_qr,
                                "amount_per_qr":amount_per_qr,"created_by_id":request.user,"expire_on":None}

                    serializer = QRBatchSerializers(data=batch_data)
                    if serializer.is_valid():
                        is_created = CreateQRCode.create_qr_code(batch_number,total_qr_code,point_per_qr)
                        if is_created:
                            qr_serializer = QRCodeSerializers(data=is_created, many=True)
                            if qr_serializer.is_valid():
                                serializer.save()
                                qr_serializer.save()
                                return HttpsAppResponse.send([], 1, "QR Batch has been create successfully.")
                            else:
                                return HttpsAppResponse.send([], 0, qr_serializer.errors)
                        else:
                            return HttpsAppResponse.send([], 0, "Something went wrong when create qr code")
                    else:
                        return HttpsAppResponse.send([], 0, serializer.errors)
                else:
                    return HttpsAppResponse.send([], 0, "Total QR Code and Point Per QR must be grater then 0.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class CreateQRCode(APIView):
    def create_qr_code(batch_number, quantity, point_per_qr):
        try:
            batch_number_ = batch_number.split('-')[1]
            bulk_qr = []
            qr_number_next = 10000
            for qty in range(quantity):
                qr_code = Util.create_unique_qr_code(batch_number_)
                qr_number_with_batch = f"QR-{batch_number_}-{qr_number_next}"
                bulk_qr.append({"qr_number":qr_number_with_batch,"qr_code":qr_code,"batch__batch_number":batch_number,"point":point_per_qr})
                qr_number_next = qr_number_next + 1
            return bulk_qr
        except Exception as e:
            logging.exception("Something went wrong.")
            manager.create_from_exception(e)
            return False

class UserWallet(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                user_id= request.data["id"]
                if BondUser.objects.filter(id=user_id).exists():
                    wallet= dict(BondUserWallet.objects.filter(user_id=user_id).values("id","user__mobile","user__full_name")
                                 .annotate(balance = Cast(F('balance'), CharField()),point = Cast(F('point'), CharField()),
                                           total_earning_amount = Cast(F('total_earning_amount'), CharField()),total_earning_point = Cast(F('total_earning_point'), CharField()),
                                            withdraw_balance= Cast(F('withdraw_balance'),CharField()),withdraw_point=Cast(F('withdraw_point'),CharField())).first())
                    wallet["transaction"] = TransactionSerializers(Transaction.objects.filter(wallet_id=wallet["id"]), many=True).data
                    return HttpsAppResponse.send([wallet], 1, "Data fetch successfully.")
                else:
                    msg = "User Does not match."
                return HttpsAppResponse.send([], 0, msg)
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class PrintBatch(APIView):
    template_name = "qr_batch.html"
    def post(self, request):
        try:
            data = request.data
            qr_code_list = list(QRCode.objects.filter(batch_id=data["batch_id"]).values_list("qr_code", flat=True))
            html_content =render_to_string(self.template_name, {"data":qr_code_list},request)
            result = BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html_content.encode("ISO-8859-1")), result)
            if not pdf.err:
                return HttpResponse(result.getvalue(),status=200, content_type='application/pdf')
            return HttpResponse(None, status=500)
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class UsersWalletReport(generics.ListAPIView):
    queryset = BondUserWallet.objects.all()
    filter_backends = [filters.SearchFilter]
    serializer_class = UserWalletReportListSerializers
    search_fields =["user__mobile"]
    pagination_class = CustomPagination

    def get_queryset(self):
        top = int(self.request.GET["top"])
        ordering = self.request.GET["ordering"]
        queryset = self.queryset.order_by(ordering)[:top] if top > 0 else self.queryset.order_by(ordering)
        return queryset

class DisableQRCode(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                qr_ids = request.data["selectedRowKeys"]
                status = request.data["status"]
                is_disabled = True if status == "disable" else False
                QRCode.objects.filter(id__in=qr_ids, used_on=None).update(is_disabled=is_disabled)
                return HttpsAppResponse.send([], 1, f"QR code {status} successfully.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))