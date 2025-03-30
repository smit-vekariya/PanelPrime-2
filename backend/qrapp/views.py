from django.shortcuts import render
from rest_framework.views import APIView, View
from manager.manager import HttpsAppResponse, Util
from manager import manager
from account.models import BondUser
from qradmin.models import QRBatch, QRCode
from qrapp.models import BondUserWallet, Transaction
from datetime import datetime
from django.db import transaction
from django.db.models import F, Q, CharField
from qrapp.serializers import TransactionSerializers
from django.db.models.functions import Cast
from django.utils import timezone


# Create your views here.

class ScanQRCode(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data
                mobile = data["mobile"]
                qr_code = data["qrcode"]
                user_id = request.user.id
                if data:
                    if BondUser.objects.filter(mobile=mobile, id=user_id).exists():
                        qr_details= QRCode.objects.filter(qr_code=qr_code, is_deleted=False, batch__is_deleted=False).all().first()
                        if qr_details:
                            if not qr_details.is_disabled:
                                if not qr_details.is_used:
                                    wallet_id = BondUserWallet.objects.filter(user_id=user_id).values("id").first()
                                    if wallet_id:
                                        point = qr_details.point
                                        qr_details.is_used = True
                                        qr_details.batch.total_used_qr_code += 1
                                        qr_details.used_on = timezone.now()
                                        qr_details.used_by_id = user_id
                                        qr_details.batch.save()
                                        qr_details.save()
                                        Transaction.objects.create(wallet_id=wallet_id["id"], description=f"Scan '{qr_code}'", tran_type="credit", point=point, tran_by_id=user_id)
                                        msg = f"Congratulations on successfully scanning the QR Code! You've earned {point} points. Well done!"
                                        return HttpsAppResponse.send([{"point":point}], 1, msg)
                                    else:
                                        msg = f"Your account wallet is not found."
                                else:
                                    msg = "This token has been used."
                            else:
                                return HttpsAppResponse.send([{"point":0}], 1, "We appreciate your effort! Better luck next time!")
                        else:
                            msg = "This token not found."
                    else:
                        msg = "User Does not found or match."
                    return HttpsAppResponse.send([], 0, msg)
                return HttpsAppResponse.send([], 0, "QRCode data not found.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))



class WithdrawAmount(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data
                mobile = data["mobile"]
                amount = data["amount"]
                if "." in str(amount):
                    return HttpsAppResponse.send([], 0, "The amount cannot contain decimal values.")
                user_id = request.user.id
                if data:
                    if BondUser.objects.filter(mobile=mobile, id=user_id).exists():
                        wallet = BondUserWallet.objects.filter(user_id=user_id).first()
                        if wallet:
                            if wallet.balance >= amount:
                                Transaction.objects.create(wallet_id=wallet.id, description=f"Withdrawal amount", tran_type="debit", amount=amount, tran_by_id=user_id)
                                msg = f"Congratulations on successfully Withdrawal the amount."
                                return HttpsAppResponse.send([{"amount":amount}], 1, msg)
                            else:
                                msg="Not enough balance to withdraw."
                        else:
                            msg="Your account wallet is not found."
                    else:
                        msg = "User Does not match."
                    return HttpsAppResponse.send([], 0, msg)
                return HttpsAppResponse.send([], 0, "Withdrawal data not found.")
        except Exception as e:
            return HttpsAppResponse.exception(str(e))


class WalletTransaction(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                mobile = request.data["mobile"]
                user_id= request.user.id
                if BondUser.objects.filter(mobile=mobile, id=user_id).exists():
                    wallet= dict(BondUserWallet.objects.filter(user_id=user_id).values("id").annotate(balance = Cast(F('balance'), CharField()),point = Cast(F('point'), CharField()), withdraw_balance= Cast(F('withdraw_balance'),CharField()),withdraw_point=Cast(F('withdraw_point'),CharField())).first())
                    wallet["transaction"] = TransactionSerializers(Transaction.objects.filter(wallet_id=wallet["id"]), many=True).data
                    return HttpsAppResponse.send([wallet], 1, "Data fetched successfully.")
                else:
                    msg = "User Does not match."
                return HttpsAppResponse.send([], 0, msg)
        except Exception as e:
            return HttpsAppResponse.exception(str(e))