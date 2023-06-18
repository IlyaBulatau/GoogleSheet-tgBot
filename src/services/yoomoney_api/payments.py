from glQiwiApi import YooMoneyAPI

from config import config


class YoomoneyClient:

    def __init__(self):
        self.client = YooMoneyAPI(api_access_token=config.YOOMONEY_TOKEN)


    async def get_payment_url(self, amount, label):
        url = self.client.create_pay_form(
            receiver=config.YOOMONEY_ID,
            quick_pay_form='small',
            targets='donat',
            payment_type='PC',
            amount=amount,
            label=label,
            success_url=config.BOT_URL,

        )
        return url
    
    async def check_payments_verification(self, label):
        async with self.client:
            payment = await self.client.check_if_operation_exists(check_fn=[label])
            if payment:
                return True
            return False

api = YoomoneyClient()