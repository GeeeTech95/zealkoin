from django.views.generic import CreateView,View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils import timezone
from django.conf import settings

from core.mail import Email
from wallet.models import Investment, Plan,Transaction,PendingDeposit,WithdrawalApplication
from Users.models import Notification
from .dashboard import AdminBase
import uuid



class CreatePlan(AdminBase,CreateView) :
    model = Plan
    success_url = reverse_lazy('plans-admin')
    template_name = 'form.html'
    fields = ['name','min_cost','max_cost','interest_rate','duration']

    def form_valid(self,form) :
        form.save(commit = False)
        form.instance.admin = self.request.user.user_admin
        form.save()
        return HttpResponseRedirect(self.success_url)


 
class AllPlans(AdminBase,ListView) :
    model  = Plan
    template_name = 'plan-list.html'    
    context_object_name = "plans"

    def get_queryset(self) :
        return self.model.objects.filter(admin = self.request.user.user_admin)    



class DepositNotice(AdminBase,ListView)   :
    model = PendingDeposit    
    template_name = 'deposit-notice.html'    
    context_object_name = "deposits" 

    def get_queryset(self) :
        return self.model.objects.filter(is_active = True)    


class ApproveDeposit(AdminBase,View) :
    model = PendingDeposit



    def on_approved_deposit(self,instance) :
        instance.on_approve()
       
        #notify user 
        msg = "Your ${} deposit has been approved.".format(instance.amount)
        Notification.objects.create(user = instance.user,message = msg)

        #create transaction
        transact = Transaction.objects.create(user = instance.user,
        status = "Approved",
        amount = instance.amount,
        transaction_type = 'DEPOSIT',
        coin = instance.payment_method,
        description = "Deposit Approved"
        )    
        mail = Email("alert")
        ctx = {
                'name' : instance.user.name,
                'text' : """
                <p>This is to inform you that your deposit of ${0} has been approved, and your {1} wallet has been credited.
                </p>
                <p>Find below the details  the transaction:</p>
                <strong>Amount : ${0}</strong><br>
                <strong>Payment Mode : {2}</strong><br>
                <strong>User : {3}</strong><br>
    
                <strong>Transaction Batch : {4}</strong><br>
                <p>Thanks For Choosing Zealkoin.ltd</p>
                <p></p><br>
                <a href="zealkoin.ltd">zealkoin.ltd</a><br>
                <span>©️ 2022 zealkoin.ltd Investment Platform .</span><br>
                <em>All Rights Reserved</em>
                """.format(
                instance.amount,
                settings.SITE_NAME,
                instance.payment_method,
                instance.user.username,
                str(uuid.uuid1()).replace("-","") +  str(uuid.uuid1()).replace("-","")
                #"usdguyfusfsdhsdusdusudyuysd"

             )
        }
        mail.send_html_email(
            [instance.user.email],
            subject = "Credit Transaction alert",
            ctx = ctx
        )
        
        return
        



    def get(self,request,*args,**kwargs) :
        feedback = {}
        pk = request.GET.get('pk',None)
        if not pk :
            feedback['error'] = "Incomplete request Parameters"
            return JsonResponse(feedback)
        try : 
            pd = self.model.objects.get(pk = pk)
            self.on_approved_deposit(pd)  
            feedback['success'] = True
         
            return JsonResponse(feedback)

        except self.model.DoesNotExist :
            feedback['error'] = "this deposit does no longer exist"
            return JsonResponse(feedback)



class DeclineDeposit(AdminBase,View)   :
    pass



class WithdrawalRequest(AdminBase,ListView) :
    model = WithdrawalApplication
    template_name = 'withdrawal_application.html'
    context_object_name = 'withdrawals'

    
    def get_queryset(self) :
        return self.model.objects.exclude(status = "APPROVED").order_by('-date')


class ApproveWithdrawal(AdminBase,View) :
    model = WithdrawalApplication


    def on_approved_withdrawal(self,instance) :
        instance.on_approve()
        #notify user 
        msg = "Your ${} withdrawal has been processed successfully.".format(instance.amount)
        Notification.objects.create(user = instance.user,message = msg)

        #create transaction
        transact = Transaction.objects.create(
            user = instance.user,
        status = "Approved",
        amount = instance.amount,
        transaction_type = 'WITHDRAWAL',
        coin =  instance.user.withdrawal_wallet_name,
        description = "Withdrawal Approved"
       
        )    
        mail = Email("alert")
        ctx = {
                'name' : instance.user.name,
                'text' : """
                <p>This is to inform you that {0} worth of ${1} has been sent to your wallet successfully
                </p>
                <p>Find below the details  the transaction:</p>
                <strong>Amount : ${1}</strong><br>
                <strong>Payment Mode : {0}</strong><br>
                <strong>User : {2}</strong><br>
                <strong>Bitcoin Address :{3} </strong><br>
                <strong>Transaction Batch : {4}</strong><br>
                <p>Thanks For Choosing Zealkoin.ltd</p>
                <p></p><br>
                <a href="zealkoin.ltd">zealkoin.ltd</a><br>
                <span>©️ 2022 zealkoin.ltd Investment Platform .</span><br>
                <em>All Rights Reserved</em>
                """.format(
                instance.user._wallet_name,
                instance.amount,
                instance.user.username,
                instance.user._wallet_address,
                str(uuid.uuid1()).replace("-","") +  str(uuid.uuid1()).replace("-","")
                #"usdguyfusfsdhsdusdusudyuysd"

             )
        }
        
        mail.send_html_email(
            [instance.user.email],
            subject = "Debit Transaction alert",
            ctx = ctx
        )
        return
        
    def get(self,request,*args,**kwargs) :
        feedback = {}
        pk = request.GET.get('pk',None)
        if not pk :
            feedback['error'] = "Incomplete request Parameters"
            return JsonResponse(feedback)
        try : 
            withdrawal_application = self.model.objects.get(pk = pk)
            if withdrawal_application.status == "APPROVED" :
                feedback['error'] = "This transaction has already been processed"
                return JsonResponse(feedback)

            self.on_approved_withdrawal(withdrawal_application)  
            feedback['success'] = True
         
            return JsonResponse(feedback)

        except self.model.DoesNotExist :
            feedback['error'] = "this withdrawal request no longer exist"
            return JsonResponse(feedback)




class InvestmentNotice(AdminBase,ListView) :
    model = Investment
    template_name = 'investment-notice.html'
    context_object_name = 'investments'

    
    def get_queryset(self) :
        return self.model.objects.exclude(is_approved = True).order_by('-date')



class ApproveInvestment(View) :
    model = Investment
    
    def on_approved_investment(self) :
        instance = self.pending_investment
        instance.on_approve()
        #notify user 
        msg = "Your ${} investment has been processed successfully.".format(instance.amount)
        Notification.objects.create(user = instance.user,message = msg)
  
        mail = Email("alert")
        ctx = {}
        ctx['name'] = instance.user.name
        ctx['text'] = msg
        subject = "Investment processed"
        mail.send_html_email([instance.user.email],subject = subject,ctx=ctx)
        return
        
    def get(self,request,*args,**kwargs) :
        feedback = {}
        pk = request.GET.get('pk',None)
        if not pk :
            feedback['error'] = "Incomplete request Parameters"
            return JsonResponse(feedback)
        try : 
            pending_investment = self.model.objects.get(pk = pk)
            if pending_investment.is_approved :
                feedback['error'] = "This transaction has already been processed"
                return JsonResponse(feedback)
            self.pending_investment  = pending_investment
            self.on_approved_investment()
            feedback['success'] = True
         
            return JsonResponse(feedback)

        except self.model.DoesNotExist :
            feedback['error'] = "this investment no longer exist"
            return JsonResponse(feedback)




