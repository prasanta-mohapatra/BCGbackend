import pandas as pd
from insurance.models import Customer, Policy


def importCsvFile(data):
    dataset = pd.read_csv(data['file'])
    customer = dataset.loc[:][['Customer_id',
                               'Customer_Gender', 'Customer_Income group', 'Customer_Region', 'Customer_Marital_status']].drop_duplicates(subset='Customer_id', keep='first')
    customer_res = insertIntoCustomer(customer)
    if customer_res['status'] == 'success':
        return insertIntoPolicy(dataset)
    else:
        return {'status': 'error'}, 500


def insertIntoPolicy(data):
    data['Date of Purchase'] = pd.to_datetime(data['Date of Purchase'])
    data['Date of Purchase'] = data['Date of Purchase'].dt.strftime('%Y-%m-%d')
    for i, row in data.iterrows():
        if not len(Policy.objects.filter(policy_id=row['Policy_id'])):
            Policy(policy_id=row['Policy_id'],
                   date_of_purchase=row['Date of Purchase'],
                   customer_id=Customer.objects.get(pk=row['Customer_id']), fuel_type=row['Fuel'], vehicle_segment=row['VEHICLE_SEGMENT'], premium=row['Premium'], body_injury_liability=True if row['bodily injury liability'] else False, personal_injury_liability=True if row[' personal injury protection'] else False, property_injury_liability=True if row[' property damage liability'] else False, collision_liability=True if row[' collision'] else False, comprehensive_liability=True if row[' comprehensive'] else False).save()
    return {'status': 'success'}, 201


def insertIntoCustomer(data):
    for i, row in data.iterrows():
        if not len(Customer.objects.filter(id=row['Customer_id'])):
            Customer(id=row['Customer_id'],
                     gender=row['Customer_Gender'], income=row['Customer_Income group'], region=row['Customer_Region'], marital_status=True if row['Customer_Marital_status'] else False).save()
    return {'status': 'success'}
