from django.db.models import Sum

from accounts.models import Expenditure, Revenue


class CommonFunctions:
    def get_individual_total_expenditure(self,user):
        try:
            total_expenses=Expenditure.objects.filter(donor=user).aggregate(Sum('amount_spent'))
            expenses=total_expenses['amount_spent__sum']
        except Expenditure.DoesNotExist:
            expenses=0.00
        return expenses
    def get_individual_total_income(self,user):
        try:

            total_revenue = Revenue.objects.filter(receiver=user).aggregate(Sum('amount_received'))
            t_income=total_revenue['amount_received__sum']
        except Revenue.DoesNotExist:
            t_income=0.00
        return t_income
