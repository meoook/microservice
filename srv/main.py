from src.services.emcd.api import EmcdApi

api_key = '57f4b7e6-77a9-4eef-ae3c-1715624ed05c'
api = EmcdApi()


user = api.get_user(api_key)
if not user:
    print(f'No user for key {api_key}')
else:
    print(user)

workers = api.get_workers(api_key, 'btc')
if not workers:
    print(f'No workers for key {api_key}')
else:
    print(workers)
    print(workers.list[0])

incomes = api.get_incomes(api_key)
if not incomes:
    print(f'No incomes for key {api_key}')
else:
    print(incomes[0])


payouts = api.get_payouts(api_key)
if not payouts:
    print(f'No incomes for key {api_key}')
else:
    print(payouts[0])


