import pandas as pd

def write_to_excel_file(obj):
  '''
  This takes in a list or a dictionary or a list
  filled with dictionairies and then uses pandas
  to put that data into rows and columns and saves it
  to an xls file in results.
  '''
  json = obj.values('person__first_name', 'person__last_name',
    'business_address_link__business__business',
    'business_address_link__address__city', 'business_address_link__address__country',
    'payment__amount', 'payment__nature_of_payment'
    )
  data_frame = pd.DataFrame(json)
  return data_frame.to_excel('payment/excel/results.xls')