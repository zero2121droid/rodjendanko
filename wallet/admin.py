from django.contrib import admin, messages
from wallet.models import CoinsWallet, CoinsTransaction
from django.utils import timezone

@admin.register(CoinsWallet)
class CoinsWalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','coins_balance', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__name', 'customer__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ["-created_at"] # sortiranje opadajuce po datumu kreiranja , koriscenje "-" ispred omogucava opadajuce sortiranje, bez njega je rastuce
    actions = ['add_10_coins', 'subtract_10_coins']

    def add_10_coins(self, request, queryset):
        for wallet in queryset:
            wallet.coins_balance += 10
            wallet.save()
            CoinsTransaction.objects.create(
                user=wallet.user,
                customer=wallet.customer,
                coins_amount=10,
                transaction_type='earn',
                description='Admin action: +10 coins',
                time_stamp=timezone.now()
            )
        self.message_user(request, "Dodato je 10 coina odabranim korisnicima/igraonicama.", messages.SUCCESS)
    add_10_coins.short_description = "Dodaj 10 coina"

    def subtract_10_coins(self, request, queryset):
        for wallet in queryset:
            if wallet.coins_balance >= 10:
                wallet.coins_balance -= 10
                wallet.save()
                CoinsTransaction.objects.create(
                    user=wallet.user,
                    customer=wallet.customer,
                    coins_amount=-10,
                    transaction_type='spend',
                    description='Admin action: -10 coins',
                    time_stamp=timezone.now()
                )
            else:
                self.message_user(request, f"{wallet} nema dovoljno coina za oduzimanje.", messages.WARNING)
        self.message_user(request, "Oduzeto je 10 coina odabranim korisnicima/igraonicama.", messages.SUCCESS)
    subtract_10_coins.short_description = "Oduzmi 10 coina"